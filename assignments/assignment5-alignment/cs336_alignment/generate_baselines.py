"""Generate and grade one prompting baseline, saving one result per JSONL line."""

import argparse
from copy import deepcopy
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    if args.output.exists():
        parser.error(f"output already exists: {args.output}")

    import torch
    from transformers import pipeline, set_seed

    from .baseline_utils import evaluate, load_dataset, load_template

    data = load_dataset(args.data, args.limit)
    template = load_template(args.prompt)
    is_question_only = "\\boxed{{}}" in template
    model_id = "allenai/OLMo-2-0425-1B"
    set_seed(args.seed)
    generator = pipeline(
        task="text-generation", model=model_id, device=torch.device(args.device)
    )
    generation_settings = {
        "do_sample": True,
        "temperature": 1.0,
        "top_p": 1.0,
        "top_k": 0,
        "max_new_tokens": 512,
        "max_length": None,
        "stop_strings": None if is_question_only else ["</answer>"],
    }
    generation_config = deepcopy(generator.generation_config)
    generation_config.update(**generation_settings)
    metadata = {
        "model": model_id,
        "data_file": str(args.data),
        "prompt_file": str(args.prompt),
        "device": args.device,
        "seed": args.seed,
        "generation_settings": generation_settings,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as output:
        for index, item in enumerate(data):
            result = evaluate(
                generator, generation_config, template, item, is_question_only
            )
            record = {
                "index": index,
                "question": item["question"],
                **result,
                "metadata": metadata,
            }
            output.write(json.dumps(record, ensure_ascii=False) + "\n")
            output.flush()
            print(f"Saved {index + 1}/{len(data)}: {result['grading']}", flush=True)


if __name__ == "__main__":
    main()
