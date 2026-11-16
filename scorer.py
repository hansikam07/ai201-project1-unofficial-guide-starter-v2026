"""
The scorer: did the generated answer contain what the question expects?

`run_eval.py` finds this file automatically and calls `judge` once per answer,
so the Run columns carry verdicts instead of blanks.

    python scorer.py results/run_2026-09-30_0002_before.md

The second form re-scores a log that is already committed, without calling the
model, so every number in the README can be traced to a file and a command.

What counts as a pass: the `expects` phrase from questions.py appears in the
answer as a whole word or phrase, ignoring case. "RA" does not match inside
"parking" and "normal" does not match "abnormal". A refusal never passes: if
the gate refused a question that should have been answered, that is a failure,
not a quiet success.
"""

import re
import sys
from pathlib import Path

REFUSAL_PREFIX = "I don't have enough information"


def judge(question: str, expects: str, answer: str, results) -> bool:
    """Deterministic pass/fail for one answer. `question` and `results` are
    accepted because run_eval.py passes them; this scorer only needs the other two."""
    expects = (expects or "").strip()
    if not expects:
        raise ValueError(f"No `expects` phrase for question: {question!r}")
    answer = (answer or "").strip()
    if not answer or answer.startswith(REFUSAL_PREFIX):
        return False
    pattern = rf"(?<!\w){re.escape(expects)}(?!\w)"
    return re.search(pattern, answer, re.IGNORECASE) is not None


def score_log(path: str) -> None:
    """Re-score a run log written by run_eval.py, per question and in total."""
    import questions as qs

    text = Path(path).read_text(encoding="utf-8")
    expected = {q["question"]: q["expects"] for q in qs.answered()}
    hits: dict[str, list[bool]] = {q: [] for q in expected}

    for block in re.split(r"\n### ", text)[1:]:
        heading = block.split("\n", 1)[0]
        question = heading.rsplit(" — run ", 1)[0]
        if question not in expected or "```" not in block:
            continue
        answer = block.split("```")[1].strip()
        hits[question].append(judge(question, expected[question], answer, None))

    total = passed = 0
    print(f"Scored {path}\n")
    print(f"{'expects':<12} {'hits':<6} question")
    for question, runs in hits.items():
        total += len(runs)
        passed += sum(runs)
        print(f"{expected[question]:<12} {sum(runs)}/{len(runs):<4} {question}")
    print(f"\nTotal: {passed}/{total} answers contained their expected phrase")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python scorer.py results/<run log>.md")
    score_log(sys.argv[1])
