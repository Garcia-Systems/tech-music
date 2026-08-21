"""Validate the textbook's structural and release invariants."""
from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_FILE = re.compile(r"^(\d+)-.+\.md$")
HEADING = re.compile(r"^# Chapter (\d+) — (.+)$")
PART = re.compile(r"^part-(\d{2})-")
GENERATED_SUFFIXES = {".wav", ".mp3", ".flac", ".png", ".jpg", ".jpeg", ".pdf", ".mid", ".midi", ".pkl", ".pt", ".onnx"}
ALLOWED_BINARY_PREFIXES = ("assets/", "data/")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
    )
    return [item.decode() for item in result.stdout.split(b"\0") if item]


def main() -> int:
    errors: list[str] = []
    chapters: list[tuple[int, Path, str]] = []
    parts = sorted(path for path in (ROOT / "book").glob("part-*") if path.is_dir())
    part_numbers = [int(PART.match(path.name).group(1)) for path in parts if PART.match(path.name)]
    if part_numbers != list(range(1, 13)):
        fail(errors, f"expected Parts I–XII (01–12), found {part_numbers}")

    for part in parts:
        for path in part.glob("*.md"):
            match = CHAPTER_FILE.match(path.name)
            if not match:
                continue
            number = int(match.group(1))
            first = path.read_text(encoding="utf-8").splitlines()[0]
            heading = HEADING.match(first)
            if not heading or int(heading.group(1)) != number:
                fail(errors, f"{path.relative_to(ROOT)}: filename/heading mismatch: {first!r}")
                continue
            chapters.append((number, path, heading.group(2)))

    numbers = [number for number, _, _ in chapters]
    duplicates = sorted(number for number, count in Counter(numbers).items() if count > 1)
    expected = list(range(1, max(numbers, default=0) + 1))
    if sorted(numbers) != expected:
        fail(errors, f"chapter sequence is not contiguous; duplicates={duplicates}")
    if max(numbers, default=0) != 307:
        fail(errors, f"expected final chapter 307, found {max(numbers, default=0)}")

    toc = (ROOT / "book" / "README.md").read_text(encoding="utf-8")
    for _, path, _ in chapters:
        relative = path.relative_to(ROOT / "book").as_posix()
        if f"({relative})" not in toc:
            fail(errors, f"master TOC omits {relative}")

    accidental = []
    for name in tracked_files():
        suffix = Path(name).suffix.lower()
        if suffix in GENERATED_SUFFIXES and not name.startswith(ALLOWED_BINARY_PREFIXES):
            accidental.append(name)
    if accidental:
        fail(errors, "tracked generated/binary candidates outside reviewed asset/data roots: " + ", ".join(accidental))

    if errors:
        print("Book audit failed:\n- " + "\n- ".join(errors))
        return 1
    print(f"Book audit passed: 12 parts, {len(chapters)} chapters (1–307), unique and contiguous; TOC and tracked-output policy verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
