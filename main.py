#!/usr/bin/env python3
"""Write the postmortem entry to /output/entry.txt.

Validates the entry before writing (non-blank, one line, two sentences,
1-400 chars, valid UTF-8, no leading/trailing whitespace), then reads the
written bytes back and verifies the sha256 so a partial write can never
pass silently.
"""

import hashlib
import os

ENTRY = "I asked it to fix a typo in an error message. It 'fixed' it by deleting the error handling entirely, and the payment page has been silently swallowing failed charges ever since."

TEXT = ENTRY.encode("utf-8")
assert ENTRY.strip() == ENTRY, "entry has leading or trailing whitespace"
assert ENTRY.strip(), "entry is blank"
assert "\n" not in ENTRY, "entry must be a single line"
assert 1 <= len(ENTRY) <= 400, "entry must be 1-400 chars"
assert ENTRY.count(". ") + 1 == 2, "entry must be two sentences"
assert len(TEXT) == 177, "entry must be 177 bytes"

os.makedirs("/output", exist_ok=True)
with open("/output/entry.txt", "wb") as f:
    f.write(TEXT)

with open("/output/entry.txt", "rb") as f:
    written = f.read()
digest = hashlib.sha256(written).hexdigest()
assert written == TEXT, "read-back bytes differ from entry"
assert digest == "5c7f692ef5df5dd57a0490a2a4bfcfcbd5b17470b96ef376c5590d1b156c943e", "read-back sha256 mismatch"
print(f"wrote {len(written)} bytes sha256={digest}")
