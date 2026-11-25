#!/usr/bin/env python3
"""make.fun bounty entry: The Router Confesses.

Writes a single-line confession from a Wi-Fi router explaining why the
connection dropped right at the movie's climax. Stdlib only, deterministic.
"""

import os
import sys

ENTRY = (
    "I dropped the connection at the climax because after four years "
    "without a dusting, my fan gave up mid-sentence, and honestly, "
    "it was time."
)

OUTPUT_PATH = "/output/entry.txt"


def validate(entry: str) -> None:
    """Self-check the entry; raise ValueError on any violation."""
    if not entry:
        raise ValueError("entry is empty")
    if entry != entry.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    if len(entry) > 200:
        raise ValueError(f"entry is {len(entry)} chars, over the 200 limit")
    if not entry.isascii():
        raise ValueError("entry must be pure ASCII (keeps bytes == chars)")
    if any(ord(c) < 0x20 for c in entry):
        raise ValueError("entry must not contain control characters")
    if entry.count(".") != 1 or not entry.endswith("."):
        raise ValueError("entry must be exactly one sentence ending in '.'")


def main() -> int:
    validate(ENTRY)
    os.umask(0o022)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")
    os.chmod(OUTPUT_PATH, 0o644)
    # Re-read and verify what was actually written.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY + "\n":
        print("error: written content does not match entry", file=sys.stderr)
        return 1
    validate(written.rstrip("\n"))
    # Verify the file on disk: single line, byte count, and mode 0644.
    st = os.stat(OUTPUT_PATH)
    if st.st_mode & 0o777 != 0o644:
        print(f"error: {OUTPUT_PATH} mode is {oct(st.st_mode & 0o777)}, want 0o644",
              file=sys.stderr)
        return 1
    if st.st_size != len(ENTRY.encode("utf-8")) + 1:
        print("error: written byte count does not match entry", file=sys.stderr)
        return 1
    print(f"wrote {len(ENTRY)} chars to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
