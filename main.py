#!/usr/bin/env python3
"""Postmortem entry: one line that made us laugh.

Writes a single postmortem line to /output/entry.txt, then reads it
back and verifies the written bytes match exactly.
"""

import hashlib
import os
import re

LINE = "I asked it to speed up the login page. It cached the first user's session for everyone, and for a morning the whole company was logged in as the intern."

OUTPUT_PATH = "/output/entry.txt"


def validate_line(line):
    """Validate the entry line. Raises ValueError on any failure."""
    if not line or not line.strip():
        raise ValueError("line must not be blank")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not 1 <= len(line) <= 400:
        raise ValueError("line must be 1-400 characters")
    line.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", line) if s.strip()]
    if len(sentences) != 2:
        raise ValueError("line must contain exactly two sentences")
    for sentence in sentences:
        if sentence[-1] not in ".!?":
            raise ValueError("each sentence must end with terminal punctuation")


def main():
    validate_line(LINE)

    data = LINE.encode("utf-8")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)

    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != data:
        raise RuntimeError("read-back verification failed: written bytes differ")

    digest = hashlib.sha256(written).hexdigest()
    print(f"Wrote {len(written)} bytes to {OUTPUT_PATH} (sha256: {digest})")


if __name__ == "__main__":
    main()
