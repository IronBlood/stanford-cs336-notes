from pathlib import Path
import sys


def find_longest_line(path: Path) -> tuple[int, int, str]:
    longest_line_number = 0
    longest_value = ""

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            value = line.rstrip("\r\n")
            if len(value) > len(longest_value):
                longest_line_number = line_number
                longest_value = value

    return longest_line_number, len(longest_value), longest_value


def main() -> None:
    if len(sys.argv) != 2:
        raise ValueError(f"usage: {sys.argv[0]} <file_path>")

    path = Path(sys.argv[1]).resolve(strict=True)
    line_number, length, value = find_longest_line(path)

    print(f"line: {line_number}")
    print(f"length: {length}")
    print(f"value: {value}")


if __name__ == "__main__":
    main()
