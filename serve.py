#!/usr/bin/env python3
"""
The Unofficial Guide — the same pipeline, over HTTP.

    python serve.py                          run it locally on port 5000
    gunicorn serve:app                       run it the way a host runs it

Nothing new happens in this file. It is a wrapper: a request comes in, it
hands the question to `app.py::ask_pipeline` — the exact function the command
line uses — and hands the answer back as JSON. Retrieval, the relevance gate
and the grounded prompt all still live where they lived. If you change how
your system answers, you change it in those files and this one follows.

Two routes:

    POST /ask       {"question": "..."} in, the answer and its sources out
    GET  /health    is the service up, and is there an index to search

Why this exists: `app.py` runs once and exits, which is fine on your laptop
and impossible to deploy. A hosted service has to stay up and wait for
requests. This is the smallest thing that does that.

Every /ask request is logged, whatever its outcome. One JSON object per line
is appended to logs/requests.jsonl (override the path with AI201_LOG_PATH):
timestamp, request_id, the question, status ("ok", "refused", "rejected" for a
400, or "error" for a 500), the HTTP status, the answer, sources and gate
numbers, per-stage timings (retrieve_ms, gate_ms, generate_ms), the whole
handler's duration_ms, token counts, whether the answer came from the cache,
peak memory, and the error text on a failure. /health is not logged. The
writing lives in observe.py and can never break a request.
"""

import os
import time
import uuid

from flask import Flask, jsonify, request

import config
import observe

app = Flask(__name__)


@app.get("/health")
def health():
    """Is the service up, and is there an index to search?

    Two different questions, and the second one is the one that bites. A
    freshly deployed service answers this route happily while every /ask
    returns "no index" — hosts give you no disk that survives a restart, so
    the index has to be built as part of getting the service up. Checking
    here means you find that out in one request instead of five.
    """
    from store import index_exists

    ready = index_exists(config.CORPUS)
    return jsonify(
        {
            "status": "ok",
            "corpus": config.CORPUS,
            "index_ready": ready,
            "detail": (
                "ready"
                if ready
                else "no index for this corpus — run `python app.py index`"
            ),
        }
    )


@app.post("/ask")
def ask():
    """One question in, one grounded answer out.

    A refused question is a 200, not an error. The gate refusing is your
    system working — it is an answer, and the JSON says so with
    `"refused": true` so whatever calls this can tell the two apart.
    """
    from app import ask_pipeline
    import generate

    started = time.perf_counter()
    timings: dict = {}
    # NOTE: the token and cache numbers below are deltas of process-wide
    # counters in generate.py. They are only accurate with one worker handling
    # one request at a time; with concurrent requests or several workers they
    # can include other requests' calls.
    tokens_before = generate.token_counts()
    cache_hits_before = generate._cache_hits

    record = {
        "timestamp": observe.now_iso(),
        "request_id": uuid.uuid4().hex,
        "endpoint": "/ask",
        "question": None,
        "status": None,
        "http_status": None,
        "answer": None,
        "refused": None,
        "sources": None,
        "best_distance": None,
        "threshold": None,
        "corpus": config.CORPUS,
        "model": config.MODEL,
        "top_k": config.TOP_K,
        "duration_ms": None,
        "retrieve_ms": None,
        "gate_ms": None,
        "generate_ms": None,
        "prompt_tokens": None,
        "output_tokens": None,
        "cache_hit": None,
        "max_rss_mb": None,
        "error": None,
    }

    try:
        payload = request.get_json(silent=True) or {}
        question = (payload.get("question") or "").strip()
        record["question"] = question or None

        if not question:
            record["status"] = "rejected"
            record["http_status"] = 400
            record["error"] = "missing question or invalid JSON"
            return (
                jsonify(
                    {
                        "error": "Send JSON with a question in it, like "
                        '{"question": "is the housing lottery random?"}'
                    }
                ),
                400,
            )

        try:
            outcome = ask_pipeline(question, corpus=config.CORPUS, timings=timings)
        except Exception as exc:  # noqa: BLE001 — a reader gets this, not a traceback
            record["status"] = "error"
            record["http_status"] = 500
            record["error"] = f"{type(exc).__name__}: {exc}"
            return jsonify({"error": f"{type(exc).__name__}: {exc}"}), 500

        record["status"] = "refused" if outcome["refused"] else "ok"
        record["http_status"] = 200
        record["answer"] = outcome["answer"]
        record["refused"] = outcome["refused"]
        record["sources"] = outcome["sources"]
        record["best_distance"] = round(outcome["best_distance"], 4)
        record["threshold"] = outcome["threshold"]

        return jsonify(
            {
                "question": question,
                "answer": outcome["answer"],
                "refused": outcome["refused"],
                "sources": outcome["sources"],
                "best_distance": round(outcome["best_distance"], 4),
                "threshold": outcome["threshold"],
                "corpus": config.CORPUS,
            }
        )
    finally:
        # Runs on every path, including the 400 and the 500. Wrapped so that
        # nothing here can change what the client receives.
        try:
            tokens_after = generate.token_counts()
            record["duration_ms"] = round((time.perf_counter() - started) * 1000, 1)
            record["retrieve_ms"] = timings.get("retrieve_ms")
            record["gate_ms"] = timings.get("gate_ms")
            record["generate_ms"] = timings.get("generate_ms")
            if record["status"] == "error":
                # The failing stage never finished, so 0.0 would be misleading.
                record["generate_ms"] = None
            record["prompt_tokens"] = tokens_after["prompt"] - tokens_before["prompt"]
            record["output_tokens"] = tokens_after["output"] - tokens_before["output"]
            record["cache_hit"] = (generate._cache_hits - cache_hits_before) > 0
            record["max_rss_mb"] = observe.max_rss_mb()
        except Exception as exc:  # noqa: BLE001
            import sys

            print(f"[observe] could not build request record: {exc}", file=sys.stderr)
        observe.log_request(record)


def main():
    # Hosts tell you which port to listen on through PORT, and they expect you
    # on 0.0.0.0. Binding 127.0.0.1 instead works perfectly on your laptop and
    # then answers nothing at all once deployed, because the host's router
    # can't reach a socket that only accepts connections from inside the
    # container. It is the single most common way a first deploy "succeeds"
    # and is unreachable.
    port = int(os.getenv("PORT", "5000"))

    # Debug mode reloads on save, which is handy, and prints a console that
    # runs arbitrary code, which is not something to leave switched on where
    # strangers can reach it. Off unless you ask for it.
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    print(f"Serving The Unofficial Guide on http://localhost:{port}")
    print(f"Corpus: {config.CORPUS}    (Ctrl-C to stop)\n")
    print("Try it from another terminal:\n")
    print(f"  curl http://localhost:{port}/health")
    print(
        f"  curl -X POST http://localhost:{port}/ask \\\n"
        f"    -H 'Content-Type: application/json' \\\n"
        f"    -d '{{\"question\": \"is the housing lottery random?\"}}'\n"
    )

    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
