"""
Observability helpers for the web service: a structured request log.

One JSON object per line (JSONL) is appended to LOG_PATH. serve.py builds the
record for each /ask request and hands it to `log_request`. Nothing in here may
ever break a request, so every failure is swallowed and reported on stderr.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import config

LOG_PATH = Path(os.getenv("AI201_LOG_PATH") or (config.ROOT / "logs" / "requests.jsonl"))


def log_request(record: dict) -> None:
    """Append one record to the log. Never raises."""
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as exc:  # noqa: BLE001 — logging must never break a request
        print(f"[observe] could not write request log: {type(exc).__name__}: {exc}", file=sys.stderr)


def now_iso() -> str:
    """Current UTC time as ISO-8601 with milliseconds and a Z."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def max_rss_mb() -> float | None:
    """Peak resident memory of this process in MB, or None where unavailable."""
    try:
        import resource  # not available on Windows
    except ImportError:
        return None
    try:
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except Exception:  # noqa: BLE001
        return None
    # macOS reports bytes, Linux reports kilobytes.
    divisor = 1024 * 1024 if sys.platform == "darwin" else 1024
    return round(peak / divisor, 1)
