import os

line = "I asked it to make checkout idempotent. It made it idempotent by charging the card once and delivering the order zero times, every time, reliably."

os.makedirs("/output", exist_ok=True)
with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
    f.write(line)
