"""Generate and grade prompting baselines using an existing vLLM HTTP server."""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-url", required=True, help="Server URL, e.g. http://gpu-host:8000")
    parser.add_argument("--model", default="allenai/OLMo-2-0425-1B")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error("--batch-size must be positive")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    if args.output.exists():
        parser.error(f"output already exists: {args.output}")

    from .baseline_utils import load_dataset, load_template, parse_answer, prepare_prompt
    from .drgrpo_grader import question_only_reward_fn, r1_zero_reward_fn
    from .vllm_utils import generate_completions

    # The helper appends /v1/completions; accept either the server root or /v1.
    base_url = args.base_url.rstrip("/").removesuffix("/v1")
    data = load_dataset(args.data, args.limit)
    template = load_template(args.prompt)
    is_question_only = "\\boxed{{}}" in template
    reward_fn = question_only_reward_fn if is_question_only else r1_zero_reward_fn
    sampling_params = {
        "temperature": 1.0,
        "top_p": 1.0,
        "top_k": 0,
        "max_tokens": 512,
        "n": 1,
        "seed": args.seed,
    }
    if not is_question_only:
        sampling_params.update(stop=["</answer>"], include_stop_str_in_output=True)
    metadata = {
        "model": args.model,
        "backend": "vllm",
        "base_url": base_url,
        "data_file": str(args.data),
        "prompt_file": str(args.prompt),
        "batch_size": args.batch_size,
        "seed": args.seed,
        "generation_settings": sampling_params,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as output:
        for start in range(0, len(data), args.batch_size):
            batch = data[start : start + args.batch_size]
            prompts = [prepare_prompt(template, item["question"]) for item in batch]
            completions = generate_completions(
                vllm_base_url=base_url,
                model_id=args.model,
                prompts=prompts,
                sampling_params=sampling_params,
            )
            if len(completions) != len(batch):
                raise RuntimeError(
                    f"Expected {len(batch)} completions, received {len(completions)}"
                )
            for offset, (item, prompt, completion) in enumerate(zip(batch, prompts, completions)):
                ground_truth = parse_answer(item["answer"])
                grading = reward_fn(completion.text, ground_truth)
                record = {
                    "index": start + offset,
                    "question": item["question"],
                    "prompt": prompt,
                    "response": completion.text,
                    "ground_truth": ground_truth,
                    "grading": grading,
                    "token_ids": completion.token_ids,
                    "finish_reason": completion.finish_reason,
                    "metadata": metadata,
                }
                output.write(json.dumps(record, ensure_ascii=False) + "\n")
                output.flush()
                print(f"Saved {start + offset + 1}/{len(data)}: {grading}", flush=True)


if __name__ == "__main__":
    main()
