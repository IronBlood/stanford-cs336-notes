"""Count baseline result categories, or inspect saved category 2 or 3 examples."""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--category", type=int, choices=(2, 3))
    parser.add_argument("--count", type=int, default=10)
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be positive")

    categories = {(1.0, 1.0): 1, (1.0, 0.0): 2, (0.0, 0.0): 3}
    counts = {1: 0, 2: 0, 3: 0}
    examples = []
    with args.results.open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                grading = record["grading"]
                category = categories[
                    (grading["format_reward"], grading["answer_reward"])
                ]
            except (ValueError, KeyError, TypeError) as error:
                parser.error(f"invalid result on line {line_number}: {error}")
            counts[category] += 1
            if category == args.category and len(examples) < args.count:
                examples.append(record)

    if args.category is None:
        print(f"Total: {sum(counts.values())}")
        print(f"Category 1 (format 1, answer 1): {counts[1]}")
        print(f"Category 2 (format 1, answer 0): {counts[2]}")
        print(f"Category 3 (format 0, answer 0): {counts[3]}")
        return

    print(
        f"Category {args.category}: showing {len(examples)} "
        f"of {counts[args.category]} results"
    )
    for number, record in enumerate(examples, start=1):
        print(f"\n--- Example {number} ---")
        print(f"Prompt:\n{record['prompt']}")
        print(f"\nResponse:\n{record['response']}")
        print(f"\nGround truth: {record['ground_truth']}")
        print(f"Rewards: {record['grading']}")


if __name__ == "__main__":
    main()
