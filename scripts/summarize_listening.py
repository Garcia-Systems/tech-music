"""Validate and summarize a personal listening-observation CSV."""
from __future__ import annotations
import argparse, csv, statistics
from collections import defaultdict
from pathlib import Path
RATINGS = ("concentration", "distraction", "enjoyment", "fatigue", "urge_to_change", "music_awareness", "task_difficulty", "desire_to_continue")

def summarize(path: Path) -> dict[str, dict[str, float]]:
    groups: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        missing = {"condition", *RATINGS} - set(reader.fieldnames or ())
        if missing: raise ValueError("missing columns: " + ", ".join(sorted(missing)))
        for line, row in enumerate(reader, 2):
            condition = row["condition"].strip()
            if not condition: raise ValueError(f"line {line}: condition is empty")
            for field in RATINGS:
                try: value = int(row[field])
                except ValueError as error: raise ValueError(f"line {line}: {field} must be an integer") from error
                if not 1 <= value <= 5: raise ValueError(f"line {line}: {field} must be 1–5")
                groups[condition][field].append(value)
    if not groups: raise ValueError("CSV contains no observations")
    return {condition: {field: statistics.fmean(values) for field, values in fields.items()} for condition, fields in groups.items()}

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("csv", type=Path); args=parser.parse_args()
    for condition, fields in summarize(args.csv).items():
        print(condition)
        print("  " + ", ".join(f"{field}={value:.2f}" for field,value in fields.items()))
if __name__ == "__main__": main()
