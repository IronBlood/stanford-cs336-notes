import argparse
import json
import torch
from copy import deepcopy
from transformers import pipeline, TextGenerationPipeline, GenerationConfig
from pathlib import Path
from typing import Optional, TypedDict, cast
from .drgrpo_grader import r1_zero_reward_fn, question_only_reward_fn

class GSMItem(TypedDict):
    question: str
    answer: str

class GradingResult(TypedDict):
    format_reward: float
    answer_reward: float
    reward: float

class EvaluationResult(TypedDict):
    prompt: str
    response: str
    ground_truth: str
    grading: GradingResult

class CLIArgs(argparse.Namespace):
    data: str
    prompt: str
    device: str

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--device", type=str, default="cpu")

    args = CLIArgs()
    parser.parse_args(namespace=args)

    return args

def load_dataset(path: str, limit: Optional[int]) -> list[GSMItem]:
    with open(path, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    if limit is not None:
        lines = lines[:limit]
    return [json.loads(line) for line in lines]

def load_template(path: str):
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
    return text

def prepare_prompt(template: str, question: str):
    return template.replace("{question}", question)

def parse_answer(s: str):
    return s.split("####")[1].strip()

def evaluate(
    generator: TextGenerationPipeline,
    generation_config: GenerationConfig,
    template: str,
    data: GSMItem,
    is_question_only: bool,
) -> EvaluationResult:
    prompt = prepare_prompt(template, data["question"])
    parsed_answer = parse_answer(data["answer"])
    response = generator(
        prompt,
        generation_config=generation_config,
        tokenizer=generator.tokenizer,
        return_full_text=False,
        clean_up_tokenization_spaces=False,
    )[0]["generated_text"]
    if is_question_only:
        result = question_only_reward_fn(response, parsed_answer)
    else:
        result = r1_zero_reward_fn(response, parsed_answer)

    return {
        "prompt": prompt,
        "response": response,
        "ground_truth": parsed_answer,
        "grading": cast(GradingResult, result),
    }

if __name__ == "__main__":
    args = parse_args()

    device = torch.device(args.device)
    data = load_dataset(args.data, 1)
    template = load_template(args.prompt)
    is_question_only = "\\boxed{{}}" in template

    generator = pipeline(
        task="text-generation",
        model="allenai/OLMo-2-0425-1B",
        device=device,
    )
    generation_config: GenerationConfig = deepcopy(generator.generation_config)
    generation_config.update(
        do_sample=True,
        temperature=1.0,
        top_p=1.0,
        top_k=0,
        max_new_tokens=512,
        max_length=None,
        stop_strings=None if is_question_only else ["</answer>"],
    )
    for item in data:
        result = evaluate(
            generator=generator,
            generation_config=generation_config,
            template=template,
            data=item,
            is_question_only=is_question_only,
        )
        print(result)
