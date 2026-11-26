#!/usr/bin/env python3
"""Make the Judge Laugh in One Line (u-email-baru-make-the-judge-laugh-in-one-line-791ccb21).

Writes exactly one funny line to /output/entry.txt (or $OUTPUT_DIR/entry.txt
for local runs). The line is a concrete 3-beat scene: a plant bought as proof
of responsibility turns the tables and sues for custody of the cat — the
punch (a houseplant winning custody) is stranger than the premise.

Gate self-check mirrors the scorer: UTF-8 text, 1-200 characters,
not only whitespace.
"""

import os
import sys

LINE = "I bought a plant to prove I could keep something alive; it just filed for custody of the cat \u2014 and won weekends."


def gate(text: str) -> None:
    """Mirror the sealed scorer's gate: 1-200 chars, non-whitespace, valid UTF-8.

    Also rejects leading/trailing whitespace, which the scorer counts
    toward the 200-char cap and which would muddle a clean read-aloud.
    """
    if not isinstance(text, str):
        raise SystemExit("gate failed: entry is not text")
    if not (1 <= len(text) <= 200):
        raise SystemExit(f"gate failed: {len(text)} chars, must be 1-200")
    if not text.strip():
        raise SystemExit("gate failed: entry is only whitespace")
    if text != text.strip():
        raise SystemExit("gate failed: leading/trailing whitespace")
    text.encode("utf-8")  # raises on invalid content


def main() -> None:
    gate(LINE)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")
    # Read-back verification: re-gate the bytes actually on disk, so a
    # write error can never ship an entry the scorer would refuse.
    with open(path, "rb") as f:
        on_disk = f.read().decode("utf-8")
    gate(on_disk.rstrip("\n"))
    if on_disk.rstrip("\n") != LINE:
        raise SystemExit("verification failed: entry.txt differs from LINE")
    print(f"wrote {path} ({len(LINE)} chars)")


if __name__ == "__main__":
    main()
