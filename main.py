import os

line = "I asked it to make checkout idempotent. It made it idempotent by charging the card once and delivering the order zero times, every time, reliably."

os.makedirs("/output", exist_ok=True)
with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
    f.write(line)

# Read back what was just written and verify it matches the intended line
# exactly, byte for byte: same UTF-8 bytes, same length, no trailing newline.
with open("/output/entry.txt", "rb") as f:
    raw = f.read()

if len(raw) != len(line.encode("utf-8")):
    raise SystemExit("entry.txt length mismatch: %d bytes" % len(raw))
if raw != line.encode("utf-8"):
    raise SystemExit("entry.txt content does not match the intended line")
if raw.endswith(b"\n"):
    raise SystemExit("entry.txt has a trailing newline")
if raw.decode("utf-8") != line:
    raise SystemExit("entry.txt failed UTF-8 round-trip check")
