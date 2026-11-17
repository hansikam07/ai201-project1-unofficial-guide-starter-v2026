#!/usr/bin/env python3
"""
Summarise a request log written by serve.py.

    python summarize_log.py logs/run_record_cost_check.jsonl
    python summarize_log.py logs/run_record_cost_check.jsonl --skip-first

Prints how many records there are by status, then for the "ok" records the
mean, median and max of each timing field, the mean token counts, and how many
answers came from the cache. --skip-first drops the first record in the file,
so a cold start can be looked at separately from the warm requests.

Standard library only.
"""

import argparse
import json
import statistics
from collections import Counter

TIMINGS = ["duration_ms", "retrieve_ms", "gate_ms", "generate_ms"]
TOKENS = ["prompt_tokens", "output_tokens"]


def load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def numbers(records: list[dict], field: str) -> list[float]:
    return [r[field] for r in records if isinstance(r.get(field), (int, float))]


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarise a serve.py request log.")
    parser.add_argument("log", help="path to a .jsonl request log")
    parser.add_argument("--skip-first", action="store_true",
                        help="drop the first record (the cold start)")
    args = parser.parse_args()

    records = load(args.log)
    if args.skip_first:
        records = records[1:]

    print(f"{args.log}{'  (first record skipped)' if args.skip_first else ''}")
    print(f"{len(records)} records\n")

    print("By status:")
    for status, count in sorted(Counter(r.get("status") for r in records).items(), key=str):
        print(f"  {status:<10} {count}")

    ok = [r for r in records if r.get("status") == "ok"]
    print(f"\n\"ok\" records: {len(ok)}")
    if not ok:
        return

    print(f"\n  {'field':<14} {'mean':>10} {'median':>10} {'max':>10}")
    for field in TIMINGS:
        values = numbers(ok, field)
        if values:
            print(f"  {field:<14} {statistics.mean(values):>10.2f} "
                  f"{statistics.median(values):>10.2f} {max(values):>10.2f}")
        else:
            print(f"  {field:<14} {'n/a':>10}")

    print()
    for field in TOKENS:
        values = numbers(ok, field)
        mean = f"{statistics.mean(values):.1f}" if values else "n/a"
        print(f"  mean {field:<14} {mean}")

    hits = sum(1 for r in ok if r.get("cache_hit") is True)
    print(f"\n  cache hits: {hits} of {len(ok)}")


if __name__ == "__main__":
    main()
