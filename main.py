#!/usr/bin/env python3
"""Postmortem entry: the silliest/most fatal time an AI coding agent
wrecked the code it was given.

Writes one short account, exactly two sentences, to /output/entry.txt
and verifies the written bytes byte-for-byte.
"""

import hashlib
import os
import re

ENTRY = (
    "I told it to clean up the old feature flags. "
    "It removed the flag that kept the paywall on, "
    "and the app was free for six hours before finance called."
)

EXPECTED_SHA256 = "c95a13910a79afc5a484ed47d00973bb3bc0e1fc5eb429bdb93f125c726a0a7e"
OUTPUT_PATH = "/output/entry.txt"


def validate(text: str) -> bytes:
    assert text, "entry must not be empty"
    assert text == text.strip(), "entry must have no leading or trailing whitespace"
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    data = text.encode("utf-8")
    assert 1 <= len(data) <= 400, f"entry must be 1-400 characters, got {len(data)}"
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text) if s]
    assert len(sentences) == 2, f"entry must be exactly two sentences, got {len(sentences)}"
    return data


def main() -> None:
    data = validate(ENTRY)
    assert hashlib.sha256(data).hexdigest() == EXPECTED_SHA256, "entry digest mismatch"
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    assert written == data, "written bytes differ from entry bytes"
    digest = hashlib.sha256(written).hexdigest()
    assert digest == EXPECTED_SHA256, "written digest mismatch"
    print(f"wrote {len(written)} bytes to {OUTPUT_PATH}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
