#!/usr/bin/env python3
"""The Postmortem That Made Us Laugh — entry writer.

Writes the single postmortem line to /output/entry.txt, validates it,
then reads it back and verifies the written bytes match exactly.
Standard library only.
"""

import hashlib
import os
import re
import sys

LINE = "I asked it to speed up the login page. It cached the first user's session for everyone, and for a morning the whole company was logged in as the intern."

OUTPUT_PATH = "/output/entry.txt"


def validate(line: str) -> None:
    if not line or not line.strip():
        raise ValueError("entry must not be blank")
    if line != line.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not 1 <= len(line) <= 400:
        raise ValueError(f"entry must be 1-400 chars, got {len(line)}")
    line.encode("utf-8")  # raises if not valid UTF-8-encodable
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", line.strip()) if s]
    if len(sentences) != 2:
        raise ValueError(f"entry must be exactly two sentences, got {len(sentences)}")
    for s in sentences:
        if not s.endswith((".", "!", "?")):
            raise ValueError(f"sentence does not end with terminal punctuation: {s!r}")


def main() -> int:
    validate(LINE)
    data = LINE.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("read-back mismatch: written bytes differ from entry")
    digest = hashlib.sha256(written).hexdigest()
    expected = hashlib.sha256(data).hexdigest()
    if digest != expected:
        raise ValueError("sha256 mismatch on read-back verification")
    print(f"wrote {OUTPUT_PATH} ({len(written)} bytes)")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
