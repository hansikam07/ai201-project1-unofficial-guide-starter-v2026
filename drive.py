#!/usr/bin/env python3
"""
Send questions to a running serve.py: one at a time, several at once, or at a
fixed arrival rate.

    python drive.py --url http://127.0.0.1:8000 --n 10
    python drive.py --n 2 --out-of-scope
    python drive.py --n 1 --empty
    python drive.py --n 6 --concurrency 3
    python drive.py --n 10 --rate 2

Options:
  --url URL          server to send to (default http://127.0.0.1:8000)
  --n N              how many requests to send (default 10)
  --out-of-scope     cycle through OUT_OF_SCOPE in questions.py instead of the
                     answered questions
  --empty            send an empty question (the server answers 400)
  --concurrency C    closed loop: keep C requests in flight at once, each
                     thread starting its next request when the last one ends.
                     Default 1, which sends one after another.
  --rate R           open loop: start a new request every 1/R seconds whether
                     or not earlier ones have finished, which is what a real
                     arrival rate looks like. Cannot be combined with
                     --concurrency.
  --max-inflight M   in --rate mode, never more than M requests in flight
                     (default 50). A start that has to wait for a free slot is
                     counted as a "delayed start" in the summary.
  --timeout S        per-request client timeout in seconds (default 60).
  --json-out PATH    also write one JSON line per request to PATH: index,
                     scheduled_start and actual_start (seconds from the start
                     of the run; scheduled_start is null outside --rate mode),
                     http_status or error, elapsed_s, question. Nothing is
                     written unless this is given.
  --max-requests K   refuse to run if --n is more than K (default 100).
  --allow-large      allow --n above --max-requests.

Without --out-of-scope or --empty it cycles through the answered questions in
questions.py. It prints one line per request (HTTP status, or "timeout" or
"connection error", and elapsed seconds), then a summary: requests sent,
counts by outcome, latency min / median / p95 / max, achieved throughput,
wall-clock total and delayed starts. Latency figures cover only the requests
that got an HTTP response.

Hazards:
  * This calls the real model through the server. Every answered request is a
    real model call (unless the server's answer cache is on) and counts
    against the free-tier quota.
  * generate.py stops a server process after 300 model calls
    (SESSION_REQUEST_BUDGET in config.py); after that every answered request
    fails. Restart the server between runs.

ask() sends one question and returns (HTTP status, elapsed seconds); it is
unchanged and other scripts may import it. Standard library only.
"""

import argparse
import json
import queue
import socket
import statistics
import threading
import time
import urllib.error
import urllib.request
from collections import Counter

import questions as qs

TIMEOUT = "timeout"
CONNECTION_ERROR = "connection error"


def _request(url: str, question: str) -> urllib.request.Request:
    body = json.dumps({"question": question}).encode("utf-8")
    return urllib.request.Request(
        url.rstrip("/") + "/ask",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )


def ask(url: str, question: str) -> tuple[int, float]:
    """POST one question to /ask. Returns (HTTP status, elapsed seconds)."""
    req = _request(url, question)
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            resp.read()
            status = resp.status
    except urllib.error.HTTPError as exc:
        exc.read()
        status = exc.code
    return status, time.perf_counter() - start


def attempt(url: str, question: str, timeout: float) -> tuple[int | str, float]:
    """Like ask(), but never raises for network trouble.

    Returns (outcome, elapsed seconds), where outcome is the HTTP status, or
    "timeout" or "connection error".
    """
    req = _request(url, question)
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp.read()
            outcome: int | str = resp.status
    except urllib.error.HTTPError as exc:
        try:
            exc.read()
        except Exception:
            pass
        outcome = exc.code
    except (TimeoutError, socket.timeout):
        outcome = TIMEOUT
    except urllib.error.URLError as exc:
        reason = exc.reason
        outcome = TIMEOUT if isinstance(reason, (TimeoutError, socket.timeout)) else CONNECTION_ERROR
    except (ConnectionError, OSError):
        outcome = CONNECTION_ERROR
    return outcome, time.perf_counter() - start


class Run:
    """Shared state for one run: results, printing and the clock."""

    def __init__(self, url: str, pool: list[str], timeout: float, show_start: bool):
        self.url = url
        self.pool = pool
        self.timeout = timeout
        self.show_start = show_start
        self.t0 = time.perf_counter()
        self.lock = threading.Lock()
        self.results: list[dict] = []
        self.delayed_starts = 0

    def question(self, i: int) -> str:
        return self.pool[i % len(self.pool)]

    def one(self, i: int, scheduled: float | None) -> None:
        question = self.question(i)
        started = time.perf_counter() - self.t0
        outcome, elapsed = attempt(self.url, question, self.timeout)
        record = {
            "index": i + 1,
            "scheduled_start": None if scheduled is None else round(scheduled, 3),
            "actual_start": round(started, 3),
            "outcome": outcome,
            "elapsed_s": round(elapsed, 3),
            "question": question,
        }
        with self.lock:
            self.results.append(record)
            start_col = f"  start +{started:6.2f}s" if self.show_start else ""
            print(f"{i + 1:>3}  {outcome}  {elapsed:7.2f}s{start_col}  "
                  f"{question or '(empty)'}", flush=True)


def run_closed(run: Run, n: int, concurrency: int) -> None:
    """C worker threads, each sending its next request when the last ends."""
    if concurrency == 1:
        for i in range(n):
            run.one(i, None)
        return

    todo: queue.Queue[int] = queue.Queue()
    for i in range(n):
        todo.put(i)

    def worker() -> None:
        while True:
            try:
                i = todo.get_nowait()
            except queue.Empty:
                return
            run.one(i, None)

    threads = [threading.Thread(target=worker) for _ in range(min(concurrency, n))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def run_open(run: Run, n: int, rate: float, max_inflight: int) -> None:
    """Start request i at t0 + i/rate, never more than max_inflight at once."""
    slots = threading.BoundedSemaphore(max_inflight)
    threads = []

    def go(i: int, scheduled: float) -> None:
        try:
            run.one(i, scheduled)
        finally:
            slots.release()

    for i in range(n):
        scheduled = i / rate
        wait = run.t0 + scheduled - time.perf_counter()
        if wait > 0:
            time.sleep(wait)
        if not slots.acquire(blocking=False):
            with run.lock:
                run.delayed_starts += 1
            slots.acquire()
        t = threading.Thread(target=go, args=(i, scheduled))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


def p95(values: list[float]) -> float:
    if len(values) == 1:
        return values[0]
    return statistics.quantiles(values, n=20, method="inclusive")[18]


def summarise(run: Run, wall: float) -> None:
    results = run.results
    counts = Counter(r["outcome"] for r in results)
    answered = [r["elapsed_s"] for r in results if isinstance(r["outcome"], int)]

    print("\nSummary")
    print(f"  requests sent       {len(results)}")
    for outcome in sorted(counts, key=lambda o: (isinstance(o, str), str(o))):
        label = f"HTTP {outcome}" if isinstance(outcome, int) else outcome
        print(f"  {label:<19} {counts[outcome]}")
    if answered:
        print(f"  latency (s, {len(answered)} with an HTTP response)")
        print(f"    min {min(answered):.2f}  median {statistics.median(answered):.2f}  "
              f"p95 {p95(answered):.2f}  max {max(answered):.2f}")
    else:
        print("  latency             n/a (no HTTP responses)")
    throughput = len(results) / wall if wall > 0 else 0.0
    print(f"  throughput          {throughput:.2f} requests/s")
    print(f"  wall-clock total    {wall:.2f}s")
    print(f"  delayed starts      {run.delayed_starts}")


def write_json(run: Run, path: str) -> None:
    """One JSON line per request, in request order."""
    with open(path, "w", encoding="utf-8") as f:
        for r in sorted(run.results, key=lambda r: r["index"]):
            outcome = r["outcome"]
            line = {
                "index": r["index"],
                "scheduled_start": r["scheduled_start"],
                "actual_start": r["actual_start"],
                "http_status": outcome if isinstance(outcome, int) else None,
                "error": None if isinstance(outcome, int) else outcome,
                "elapsed_s": r["elapsed_s"],
                "question": r["question"],
            }
            f.write(json.dumps(line) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Send questions to serve.py.")
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--n", type=int, default=10, help="how many requests")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--out-of-scope", action="store_true",
                       help="use OUT_OF_SCOPE instead of the answered questions")
    group.add_argument("--empty", action="store_true", help="send an empty question")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--concurrency", type=int, default=1,
                      help="closed loop: requests in flight at once (default 1)")
    mode.add_argument("--rate", type=float, default=None,
                      help="open loop: start a request every 1/RATE seconds")
    parser.add_argument("--max-inflight", type=int, default=50,
                        help="in --rate mode, the most requests in flight (default 50)")
    parser.add_argument("--timeout", type=float, default=60.0,
                        help="per-request client timeout in seconds (default 60)")
    parser.add_argument("--json-out", metavar="PATH", default=None,
                        help="write one JSON line per request to PATH")
    parser.add_argument("--max-requests", type=int, default=100,
                        help="refuse --n above this unless --allow-large (default 100)")
    parser.add_argument("--allow-large", action="store_true",
                        help="allow --n above --max-requests")
    args = parser.parse_args()

    if args.n > args.max_requests and not args.allow_large:
        parser.exit(2, f"drive.py: refusing to send {args.n} requests, which is more "
                       f"than --max-requests ({args.max_requests}). Nothing was sent.\n"
                       f"Each answered request is a real model call, and the server "
                       f"stops after 300 of them. Add --allow-large to send that many.\n")

    if args.n < 1:
        parser.error("--n must be at least 1")
    if args.concurrency < 1:
        parser.error("--concurrency must be at least 1")
    if args.rate is not None and args.rate <= 0:
        parser.error("--rate must be greater than 0")
    if args.max_inflight < 1:
        parser.error("--max-inflight must be at least 1")

    if args.empty:
        pool = [""]
    elif args.out_of_scope:
        pool = list(qs.OUT_OF_SCOPE)
    else:
        pool = [q["question"] for q in qs.answered()]

    show_start = args.rate is not None or args.concurrency > 1
    run = Run(args.url, pool, args.timeout, show_start)
    if args.rate is not None:
        run_open(run, args.n, args.rate, args.max_inflight)
    else:
        run_closed(run, args.n, args.concurrency)
    summarise(run, time.perf_counter() - run.t0)
    if args.json_out:
        write_json(run, args.json_out)
        print(f"\nWrote {len(run.results)} lines to {args.json_out}")


if __name__ == "__main__":
    main()
