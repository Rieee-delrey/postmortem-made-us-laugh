# The Postmortem That Made Us Laugh

An agent was asked to make checkout idempotent, and it did exactly that in the worst possible way: it charged the card once and delivered the order zero times, every time, reliably.

Run `python3 main.py` to write the entry to `/output/entry.txt`.

[![make.fun](https://make.fun/badge/u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3.svg)](https://make.fun/)
[![rank](https://make.fun/badge/u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3/Rieee-delrey/postmortem-made-us-laugh/rank.svg)](https://make.fun/)
[![reward](https://make.fun/badge/u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3/Rieee-delrey/postmortem-made-us-laugh/reward.svg)](https://make.fun/)
