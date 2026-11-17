#!/usr/bin/env python3
"""
Send questions to a running serve.py, one after another.

    python drive.py --url http://127.0.0.1:8000 --n 10
    python drive.py --n 2 --out-of-scope
    python drive.py --n 1 --empty

Cycles through the questions in questions.py and prints the HTTP status and
elapsed time for each request. Standard library only.
"""

import argparse
import json
import time
import urllib.error
import urllib.request

import questions as qs


def ask(url: str, question: str) -> tuple[int, float]:
    """POST one question to /ask. Returns (HTTP status, elapsed seconds)."""
    body = json.dumps({"question": question}).encode("utf-8")
    req = urllib.request.Request(
        url.rstrip("/") + "/ask",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            resp.read()
            status = resp.status
    except urllib.error.HTTPError as exc:
        exc.read()
        status = exc.code
    return status, time.perf_counter() - start


def main() -> None:
    parser = argparse.ArgumentParser(description="Send questions to serve.py.")
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--n", type=int, default=10, help="how many requests")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--out-of-scope", action="store_true",
                       help="use OUT_OF_SCOPE instead of the answered questions")
    group.add_argument("--empty", action="store_true", help="send an empty question")
    args = parser.parse_args()

    if args.empty:
        pool = [""]
    elif args.out_of_scope:
        pool = list(qs.OUT_OF_SCOPE)
    else:
        pool = [q["question"] for q in qs.answered()]

    for i in range(args.n):
        question = pool[i % len(pool)]
        status, elapsed = ask(args.url, question)
        print(f"{i + 1:>3}  {status}  {elapsed:7.2f}s  {question or '(empty)'}")


if __name__ == "__main__":
    main()
