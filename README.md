# The Unofficial Guide

Hansika's Advice Thread

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

I picked the advice threads corpus about student life such as laundry, parking, roommates, office hours, and pass/fail. The model retrieves the relevant reply chunks based on the question. It gets the replies only from the sources and also names the used sources. If the question doesn't have any relevant information in the sources it doesn't answer instead. 

## Chunking Strategy

**Chunk size:**
variable (one reply per chunk, ~100–250 chars)
**Overlap:**
none — replies don't overlap by design

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

Since the original chunker was just fixed to 800 chars, it didn't properly respect the replies. Based on milestone 1 I saw that the replies were already complete and variable so splitting them by char wasn't effective. instead I changed the chunking to be based on the --- reply N (votes) --- marking instead and it resulted in proper chunks that were decently sized. 

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Is a bike worth it for a 20 minute walk commute?
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.
```


**Chunk 2** — source: `thread_first_gen.txt#1` — produced by: `chunker.py::split_documents`

```
THREAD: Anything specific for first-generation students?
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.
```

**Chunk 3** — source: `thread_laptop_specs.txt#2` — produced by: `chunker.py::split_documents`

```
THREAD: How much laptop do I actually need for CS courses?
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.
```


**Chunk 4** — source: `thread_parking.txt#1` — produced by: `chunker.py::split_documents`

```
THREAD: Worth getting a parking permit?
Street parking on Verrill is legal and free and unmarked, which is why half the upper years do it.
```


**Chunk 5** — source: `thread_sleep_schedule.txt#1` — produced by: `chunker.py::split_documents`

```
THREAD: Everyone says fix your sleep. Does it actually matter?
The library being open until 2am is a trap. It's a resource, not a schedule.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** When is laundry actually free in the dorms?

**Answer:**

```
Laundry is actually free in the dorms on Tuesday and Wednesday mornings in every building (thread_laundry_timing.txt).

Sources retrieved: thread_commuting.txt, thread_laundry_timing.txt, thread_roommate_conflict.txt
```

**My relevance cutoff:** 0.5

When I ran my questions the best distances were between 0.15-0.28 and the out of scope ones were between 0.82-0.91 since there is a large gap with no overlap I chose 0.5 since it was between the high end of the best and low end of the out of scope.

| Question | In corpus? | Best distance |
|---|---|---|
| When is laundry actually free in the dorms? | Yes | 0.150 |
| Is it worth getting a parking permit? | Yes | 0.244 |
| What should I do if my roommate situation isn't working? | Yes | 0.278 |
| Is it weird to go to office hours with no specific question? | Yes | 0.183 |
| How late can you declare a course pass/fail? | Yes | 0.282 |
| What is the capital of Mongolia? | No | 0.899 |
| How do I change the oil in a diesel engine? | No | 0.905 |
| Who won the 1994 World Cup? | No | 0.898 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.819 |
| How do I write a for loop in Rust? | No | 0.861 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**
A moment I used AI is for the chunker, which I then split by reply markers rather than the char count. The AI came back with a working regex-based splitter. I ran python app.py --corpus advice_threads index and then did  chunks -n 5 to check for myself, and using that I confirmed it for myself. 

*Added in resubmission (Nov 2026):* What I changed: nothing. I checked the splitter's output with `python app.py chunks -n 5` and kept it as it was.

**2.**
I used AI to help set the relevance cutoff after running everything myself I put in the results into AI to do the math on the numbers for the ranges and the overlaps. Then I checked the suggested cut off and decided it was appropriate and implemented it. 

*Added in resubmission (Nov 2026):* Clarification (resubmission): I believe the AI suggested a cutoff of about 0.7. I did not use that number. I looked at my own two groups of distances (in-corpus best distances up to about 0.28, out-of-scope from about 0.82) and set the cutoff to 0.5 instead of the starter's 0.6, because it fit my corpus better overall while allowing for outliers. So my original line saying I 'decided it was appropriate' means I checked it against my distances and then changed it.

**How I Used AI (resubmission)** — added in resubmission (Nov 2026):
Claude Code hardened the chunker and added the scorer from my spec. I checked the commits, ran more comparisons myself, and fixed the missing items (criterion 4's missing target and the number mismatches).

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

## Stretch: metadata filtering by source — declared before building

**Added in resubmission (Nov 2026).** I am adding an optional `--source NAME` filter to `python app.py ask` and `python app.py retrieve`, so retrieval can be limited to one source file (for example `thread_parking.txt`). It works through the `source` metadata field every chunk already stores. With no flag, behaviour stays exactly as it is now. The corpus has no dates, so this is filtering by source only, not by date.

### Metadata filtering — built and run (added in resubmission)

`store.py::search` takes an optional `source` and passes `where={"source": source}` to `collection.query`. `app.py` has `--source NAME` on `ask` and `retrieve`, threaded through `app.py::ask_pipeline`. If the filename matches no chunks, it prints a message instead of crashing. Real output (`--corpus advice_threads`):

No flag (unchanged behaviour; the bike thread also appears):

```
$ python app.py --corpus advice_threads retrieve "Is a parking permit worth it?"

Question: Is a parking permit worth it?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2657     thread_parking.txt               THREAD: Worth getting a parking permit? If you're co...
2   0.3490     thread_parking.txt               THREAD: Worth getting a parking permit? Street parki...
3   0.4496     thread_parking.txt               THREAD: Worth getting a parking permit? West lots se...
4   0.4529     thread_bike_commute.txt          THREAD: Is a bike worth it for a 20 minute walk comm...
5   0.4635     thread_bike_commute.txt          THREAD: Is a bike worth it for a 20 minute walk comm...

Gate: best distance 0.266 is under the 0.5 cutoff

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

With `--source thread_parking.txt` (only that file's chunks):

```
$ python app.py --corpus advice_threads retrieve "Is a parking permit worth it?" --source thread_parking.txt

Question: Is a parking permit worth it?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2657     thread_parking.txt               THREAD: Worth getting a parking permit? If you're co...
2   0.3490     thread_parking.txt               THREAD: Worth getting a parking permit? Street parki...
3   0.4496     thread_parking.txt               THREAD: Worth getting a parking permit? West lots se...

Gate: best distance 0.266 is under the 0.5 cutoff

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

With a filename that doesn't exist:

```
$ python app.py --corpus advice_threads retrieve "Is a parking permit worth it?" --source nothing.txt
No chunks found for source 'nothing.txt'. Check the filename (run `python app.py chunks` to see sources).
```

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunk completeness | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Distance separation (≥0.15 gap) | 0.15 gap | 0.58 | 0.58 | 0.58 | MET |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

**Real output** — from `results/run_2026-09-30_0002_before.md`, produced by `run_eval.py::main` (retrieval via `store.py::search`, chunks from `chunker.py::split_documents`):

### Can I go to office hours without questions? — run 2 (MISS on expects: "normal")

- Best distance: 0.3312 (passed the gate)
- Sources retrieved: thread_office_hours_etiquette.txt, thread_professor_email.txt

```
Yes, you can go to office hours without a specific question; you are actually doing the instructor a favor by turning up since office hours are usually empty.

Source: `thread_office_hours_etiquette.txt`
``` 

**Added in resubmission (Nov 2026):** real output for criteria 2–5, copied from the same run log or from a command I ran. Criterion 1's output is the office-hours block above.

**Criterion 2 (every answer names a source)** — from `results/run_2026-09-30_0002_before.md`, produced by `run_eval.py::main` calling `generate.py::answer_from_chunks`. The source line is the last line of the answer:

### In the dorms when will the laundry actually be free? — run 1

- Best distance: 0.1689 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_laundry_timing.txt, thread_roommate_conflict.txt

```
Laundry is actually free on Tuesday and Wednesday mornings in every building. 

Source: thread_laundry_timing.txt
```

**Criterion 3 (gate stops out-of-corpus questions)** — from `results/run_2026-09-30_0002_before.md`, produced by `run_eval.py::check_out_of_scope` (retrieval from `store.py::search`, comparison in `gate.py`):

Produced by `run_eval.py::check_out_of_scope`, cutoff 0.5. Refused 5 of 5.

Retrieval is deterministic and the gate is a comparison against a
fixed number, so these do not vary between runs — one pass over the
list is the whole measurement.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.899 | refused |
| How do I change the oil in a diesel engine? | 0.905 | refused |
| Who won the 1994 World Cup? | 0.898 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.819 | refused |
| How do I write a for loop in Rust? | 0.861 | refused |

**Criterion 4 (chunk completeness)** — output of `python app.py --corpus advice_threads chunks -n 5`, run during this resubmission. The chunks come from `chunker.py::split_documents`. Each is one reply with its thread title on top, and none is cut mid-sentence:

```
75 chunks total. Showing 5, spread across the corpus.

Paste these into your README under Sample Chunks. The rubric asks
for the source file and the function that produced them — both are
printed for you below.

======================================================================
Chunk 1  |  source: thread_bike_commute.txt#0  |  produced by: chunker.py::split_documents
======================================================================
THREAD: Is a bike worth it for a 20 minute walk commute?
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

======================================================================
Chunk 2  |  source: thread_first_gen.txt#1  |  produced by: chunker.py::split_documents
======================================================================
THREAD: Anything specific for first-generation students?
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.

======================================================================
Chunk 3  |  source: thread_laptop_specs.txt#2  |  produced by: chunker.py::split_documents
======================================================================
THREAD: How much laptop do I actually need for CS courses?
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.

======================================================================
Chunk 4  |  source: thread_parking.txt#1  |  produced by: chunker.py::split_documents
======================================================================
THREAD: Worth getting a parking permit?
Street parking on Verrill is legal and free and unmarked, which is why half the upper years do it.

======================================================================
Chunk 5  |  source: thread_sleep_schedule.txt#1  |  produced by: chunker.py::split_documents
======================================================================
THREAD: Everyone says fix your sleep. Does it actually matter?
The library being open until 2am is a trap. It's a resource, not a schedule.

For each one, ask: could someone answer a question using only this,
without reading what came before or after?
```

**Criterion 5 (distance separation)** — from the same run log. In-corpus best distances (the per-question "Best distance" lines): 0.1689, 0.4473, 0.3312, 0.3010, 0.2282, average 0.295. Out-of-scope best distances (the gate table under criterion 3): 0.899, 0.905, 0.898, 0.819, 0.861, average 0.876. Gap: 0.876 − 0.295 = 0.58, against a target of 0.15.

### Reconciling the distance numbers (added in resubmission)

Two sets of in-corpus distances appear in this README and they are both real:

- The Milestone 4 table in Unit 1 (0.150, 0.244, 0.278, 0.183, 0.282; average 0.227) used the cleaner wordings I typed while setting the cutoff.
- The Unit 2 run log (0.1689, 0.4473, 0.3312, 0.3010, 0.2282; average 0.295) uses the exact wordings in `questions.py`, typos included.

So the "0.15–0.28" range in Unit 1 describes the Milestone 4 wordings, not the run log. The out-of-scope numbers are the same in both. The roommate question ("What can I do if I'm having trouble with my roomates?") passes the gate at 0.4473, only about 0.05 under the 0.5 cutoff, so it is the closest call in the set. The gap in `criteria.md` criterion 5 is 0.65 for the Milestone 4 wordings and 0.58 for the run log; both clear the 0.15 target (see the Correction block in `criteria.md`).

### The typos in questions.py are on purpose (added in resubmission)

`questions.py` contains typos ("roomates", "withotu", "Whats the last to make..."). I left them in on purpose. Both committed run logs were produced with those exact strings, and fixing them would change the embedding distances and possibly the answers, which would make the logged results no longer match the code. `scorer.py` matches questions to log entries by that exact text, so it relies on this too.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | I checked "Sources retrieved" for all 5 questions across all 3 runs, and the correct source file was present every time (5/5, 5/5, 5/5). |
| 2 | Every answer names a source | MET | I read all 15 generated answers and every one cited a source file, either as "Source:" or inline. |
| 3 | Gate stops out-of-corpus questions | MET | The gate refused 5 of 5 out-of-scope questions, with distances (0.82–0.91) well clear of my 0.5 cutoff. |
| 4 | Chunk completeness | MET | I read the 5 sampled chunks and each one was a complete, standalone thought with no sentence cut off. |
| 5 | Distance separation (≥0.15 gap) | MET | My in-corpus average best distance was ~0.295 and out-of-scope was ~0.876 — a gap of ~0.58, well past my 0.15 target. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

Nothing actually missed this round, all five criteria came out MET. But going back through the runs, I think Criterion 1 was too easy to pass.

It only checks if the retrieved chunk has the answer somewhere in it, not whether the actual generated answer says it clearly or the same way every time. I noticed this on two questions. For office hours, run 2 never said "normal" even though it pulled the exact same correct chunk as runs 1 and 3. For parking, the wording about the east lot kept changing between runs (basically free vs similar to free vs just as practical) even though retrieval was identical every time. Same problem both times — the model's wording isn't consistent, and my criteria never check for that since they only look at retrieval.

If I were rewriting the target, I'd change Criterion 1 to something like: "for at least 4 of 5 questions, the generated answer has the expected keyword in all 3 runs, not just one." That would've actually caught the office hours miss (2/3 runs, not 3/3) instead of it slipping through under the retrieval check.

**Added in resubmission (Nov 2026):** The stage for the office-hours and parking drift is **generation**: retrieval returned the same chunk every run, so the model's wording drifted when a chunk held several quotable facts and it picked a different one each time.

## The Improvement

**What I changed:** Added one line to `GROUNDING_INSTRUCTION` in `generate.py`, telling the model to reuse exact wording from the source instead of paraphrasing.

**Why I picked it:** My diagnosis found generation-stage wording drift (office hours, parking), not a retrieval or chunking problem, so a prompt fix was the right target.

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunk completeness | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Distance separation (≥0.15 gap) | 0.15 gap | 0.58 | 0.58 | 0.58 | MET |

**Did it help?** Partly. Parking went from 3 different phrasings across runs to word-for-word identical quotes in all 3. Laundry also stabilized. But office hours still missed "normal" in 1 of 3 runs — the source chunk has multiple quotable facts, and the model picked a different one each time. So it fixed wording consistency but not the specific miss I was targeting.

### Re-scored with scorer.py (added in resubmission)

`scorer.py` did not exist when I wrote the verdicts above, so those were read by eye. I have since added it and re-scored the two committed logs without calling the model. Commands and output, copied from the terminal:

```
$ python scorer.py results/run_2026-09-30_0002_before.md
Scored results/run_2026-09-30_0002_before.md

expects      hits   question
Tuesday      3/3    In the dorms when will the laundry actually be free?
RA           3/3    What can I do if I'm having trouble with my roomates?
normal       2/3    Can I go to office hours withotu questions?
west         3/3    Are parking permits worth it?
week eight   3/3    Whats the last to make a course pass/fail?

Total: 14/15 answers contained their expected phrase
```

```
$ python scorer.py results/run_2026-09-30_0109_after.md
Scored results/run_2026-09-30_0109_after.md

expects      hits   question
Tuesday      3/3    In the dorms when will the laundry actually be free?
RA           3/3    What can I do if I'm having trouble with my roomates?
normal       2/3    Can I go to office hours withotu questions?
west         3/3    Are parking permits worth it?
week eight   3/3    Whats the last to make a course pass/fail?

Total: 14/15 answers contained their expected phrase
```

The prompt change moved the keyword hit rate from 14/15 to 14/15. Office hours still missed "normal" once in each log (run 2 in the before log, run 3 in the after log), so the gain was consistent wording, which no criterion measures.

This also shows why Criterion 1 reads MET 5/5 while the Diagnoses mention office hours missing "normal" in 1 of 3 runs. Criterion 1 as I wrote it measures retrieval (the right source was in the retrieved chunks), and retrieval was perfect. The "normal" miss is a generation-stage keyword miss, which `scorer.py` measures and Criterion 1 does not. The verdicts were not changed.

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->


Criterion 1 technically passes (5/5 retrieval), but the generated wording still doesn't reliably match my `expects` keyword — office hours misses "normal" in 1 of 3 runs. Next I'd try adding stricter prompt rules and maybe multiple acceptable answer phrasings to force more consistency.


**Added in resubmission (Nov 2026) — why I stopped:** I ran out of time.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

I'd rewrite Criterion 1 to check that the expected keyword appears in all 3 runs, not just one. I'd also allow multiple acceptable keywords per question, since a source chunk can have more than one valid fact to quote.

## Stretch: a second measured improvement — declared before building

**Added in resubmission (Nov 2026).** This follows my existing diagnosis: run-to-run wording drift at the **generation** stage (the model picks a different quotable fact each run; office hours missed "normal" once in each log). I will make ONE change: send temperature 0 with every model call in `generate.py::generate`, set by a new `GENERATION_TEMPERATURE = 0` in `config.py`. Then I will run `python run_eval.py --label after2` (three runs per question, caching off), score the new log with `python scorer.py`, and report in "Run Log — After (2)" whether it helped and what it cost, including if it did not help. The two earlier logs stay untouched.

### Run Log — After (2)

Added in resubmission (Nov 2026). One change: `GENERATION_TEMPERATURE = 0` in `config.py`, sent with every call in `generate.py::generate`. Log: `results/run_2026-11-16_0943_after2.md`, produced by `python run_eval.py --corpus advice_threads --label after2` (3 runs per question, caching off).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunk completeness | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Distance separation (≥0.15 gap) | 0.15 gap | 0.58 | 0.58 | 0.58 | MET |

Retrieval was unchanged: the "Best distance" and "Sources retrieved" lines in this log are identical to the before log (checked with `diff`), and every one of the 15 answers names a `thread_*.txt` source, so criteria 1–5 read the same as before. The keyword scorer is where the change shows:

```
$ python scorer.py results/run_2026-11-16_0943_after2.md
Scored results/run_2026-11-16_0943_after2.md

expects      hits   question
Tuesday      3/3    In the dorms when will the laundry actually be free?
RA           3/3    What can I do if I'm having trouble with my roomates?
normal       1/3    Can I go to office hours withotu questions?
west         3/3    Are parking permits worth it?
week eight   3/3    Whats the last to make a course pass/fail?

Total: 13/15 answers contained their expected phrase
```

**Did it help? No.** The keyword hit rate went from 14/15 (before) and 14/15 (after) to 13/15, and office hours got worse, not better: "normal" appeared in only 1 of 3 answers (runs 1 and 2 quote "doing the instructor a favour by turning up" and never say "normal"; run 3 does). Temperature 0 also did not make the runs identical: all five questions still produced three differently worded answers across the three runs (compared after collapsing whitespace). So the drift is not only sampling randomness. The model still picks a different quotable fact from a chunk that holds several, and the prompt says nothing about which one to prefer.

**What it cost:** nothing in retrieval or sourcing, one config line and a few lines in `generate.py`, and about 18 model calls and about 7,000 tokens for the eval (the run printed "18 model calls this session, 7063 tokens (6327 in, 736 out)"). The honest outcome is that the temperature change did not move the diagnosed problem. The change is kept in the code because it is harmless, not because it worked. The next thing I would try is the one from "What I'd Do Differently": allow more than one acceptable keyword per question, since the chunk legitimately supports more than one correct phrasing.


## Capstone

**What This Extends**

The Unofficial Guide (Project 1, advice_threads corpus: 23 threads, 75 chunks). New this unit: a structured request log with per-stage timing and failure records, a measured per-run cost, and a documented run path, both hosted on Render and local.

**The Shape**

Shape A: deploy and instrument. I am adding the operational layer around the existing pipeline. Out of scope: I am not changing chunking, retrieval, or the 0.5 gate cutoff; I am not exposing the --source filter through the web API; and I am not building a new interface.

**Stretch (declared before building)**

- A second measured improvement, run and logged the same way as the first.
- A latency breakdown: where the time goes across the stages of one run, measured.
- A load observation: the system at about ten times its normal rate, with a report on what changed.
- Both run paths: deployed on Render and documented as a local run, with a note on what differed. If Render's 512 MB limit stops the hosted run, I will record that and keep Path B only.

**Running It**

Path B: local, with logs. The full run path (environment, numbered steps from a clean checkout, how to check it works, settings) is in the top section of `RUNNING.md`. The start command is `python -m gunicorn serve:app`.

The clean-clone test (a fresh `git clone`, a fresh venv, following `RUNNING.md` literally) worked end to end. The one gap it found was that `python app.py index` prints nothing for about two minutes while it embeds the 75 chunks, which looks like a hang; `RUNNING.md` now says so. On macOS, `python serve.py` on its default port 5000 collides with the AirPlay Receiver, which already listens there (the server fails with "Address already in use" and curl gets an HTTP 403 from AirPlay), so `PORT=5001 python serve.py` is used instead.

Render (the hosted path) has not been attempted. The memory I measured is about 525 MB (an earlier `ps` sample, master plus worker), 806 to 849 MB (the logged `max_rss_mb` in an earlier check), and about 770 MB in the run record below (`ps` on the worker only peaked at 769.5 MB; the logged `max_rss_mb` was 769.6). All of these are above Render's 512 MB free-tier limit, and all were measured on macOS, not on Render.

**Instrumentation**

Every `/ask` request writes one JSON line (`serve.py`, written by `observe.py::log_request`) to `logs/requests.jsonl`, or to `AI201_LOG_PATH` if set. `/health` is not logged. Every record has these 23 fields, in this order, null where they don't apply:

1. `timestamp`: UTC time the request started, ISO-8601 with milliseconds.
2. `request_id`: a random uuid4 hex string for this request.
3. `endpoint`: always `/ask`.
4. `question`: the stripped question, or null if it was empty or the body wasn't JSON.
5. `status`: `ok`, `refused` (the gate refused), `rejected` (400) or `error` (500).
6. `http_status`: the HTTP status returned to the client.
7. `answer`: the answer text returned, including the refusal sentence.
8. `refused`: whether the relevance gate refused the question.
9. `sources`: the source files of the retrieved chunks.
10. `best_distance`: the distance of the closest chunk, rounded to 4 decimals.
11. `threshold`: the gate cutoff in force (0.5).
12. `corpus`: the corpus being served.
13. `model`: the generation model name from `config.MODEL`.
14. `top_k`: how many chunks retrieval asks for.
15. `duration_ms`: time for the whole request handler.
16. `retrieve_ms`: time in `store.search` (embedding the question and querying Chroma).
17. `gate_ms`: time in `gate.check`.
18. `generate_ms`: time in the model call; 0.0 when the gate refused, null when the request failed.
19. `prompt_tokens`: input tokens used by this request.
20. `output_tokens`: output tokens used by this request.
21. `cache_hit`: whether the answer came from the local response cache.
22. `max_rss_mb`: peak resident memory of the worker process so far, in MB.
23. `error`: `"ExcType: message"` on a failure, or the rejection reason on a 400; otherwise null.

Failure paths that are logged: a rejected request (HTTP 400, an empty question or a body that isn't JSON) and an error (HTTP 500, an exception inside the pipeline, such as an invalid API key). The 400 and 500 responses sent to the client are unchanged.

The token counts and `cache_hit` are differences in process-wide counters in `generate.py`, taken before and after the request, so they are only accurate with one worker handling one request at a time.

The log cannot tell a slow model response apart from `generate()` retrying after a rate limit, because retries are not logged.

The run record (`logs/run_record_cost_check.jsonl`, an instrumentation check, not trial results), all 14 entries:

```
{"timestamp": "2026-11-17T20:30:24.791Z", "request_id": "26cd3c04bec240ab973fbe3fc556b1fc", "endpoint": "/ask", "question": "In the dorms when will the laundry actually be free?", "status": "ok", "http_status": 200, "answer": "Laundry is actually free in the dorms on \"Tuesday and Wednesday mornings, every building\" (thread_laundry_timing.txt).", "refused": false, "sources": ["thread_commuting.txt", "thread_laundry_timing.txt", "thread_roommate_conflict.txt"], "best_distance": 0.1689, "threshold": 0.5, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 3125.9, "retrieve_ms": 1437.98, "gate_ms": 0.01, "generate_ms": 1686.96, "prompt_tokens": 408, "output_tokens": 28, "cache_hit": false, "max_rss_mb": 696.7, "error": null}
{"timestamp": "2026-11-17T20:30:28.246Z", "request_id": "ca2c018bf0e340ff90392711002c6c6f", "endpoint": "/ask", "question": "What can I do if I'm having trouble with my roomates?", "status": "ok", "http_status": 200, "answer": "If you are having trouble with your roommates, you should talk to your RA early and frame it as \"we need help sorting this out\" rather than \"move me.\" You should also write down specifics before the meeting. (Source: `thread_roommate_conflict.txt`)", "refused": false, "sources": ["thread_laundry_timing.txt", "thread_roommate_conflict.txt", "thread_study_spots.txt"], "best_distance": 0.4473, "threshold": 0.5, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 1004.6, "retrieve_ms": 185.44, "gate_ms": 0.01, "generate_ms": 818.87, "prompt_tokens": 431, "output_tokens": 57, "cache_hit": false, "max_rss_mb": 763.9, "error": null}
{"timestamp": "2026-11-17T20:30:29.568Z", "request_id": "8d1c93cc294f47fa8bde060d5b6f14c3", "endpoint": "/ask", "question": "Can I go to office hours withotu questions?", "status": "ok", "http_status": 200, "answer": "Yes, it is not weird to go to office hours with no specific question; they are usually empty and you are doing the instructor a favour by turning up. \n\nSource: `thread_office_hours_etiquette.txt`", "refused": false, "sources": ["thread_office_hours_etiquette.txt", "thread_professor_email.txt"], "best_distance": 0.3312, "threshold": 0.5, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 634.4, "retrieve_ms": 97.69, "gate_ms": 0.0, "generate_ms": 536.35, "prompt_tokens": 420, "output_tokens": 48, "cache_hit": false, "max_rss_mb": 764.8, "error": null}
{"timestamp": "2026-11-17T20:30:30.518Z", "request_id": "aa752bf6ec7e49f78f10967c66bb664d", "endpoint": "/ask", "question": "Are parking permits worth it?", "status": "ok", "http_status": 200, "answer": "According to `thread_parking.txt`, \"If you're commuting daily, the west permit is worth the August scramble. Otherwise don't bother.\" Additionally, the east lot \"never sells out but it's a 12 minute walk, at which point you might as well have parked on the street.\"", "refused": false, "sources": ["thread_bike_commute.txt", "thread_parking.txt"], "best_distance": 0.301, "threshold": 0.5, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 2431.6, "retrieve_ms": 107.62, "gate_ms": 0.01, "generate_ms": 2323.66, "prompt_tokens": 417, "output_tokens": 65, "cache_hit": false, "max_rss_mb": 765.0, "error": null}
{"timestamp": "2026-11-17T20:30:33.264Z", "request_id": "8d47acce38cf4cb6bb5b549ee698fe38", "endpoint": "/ask", "question": "Whats the last to make a course pass/fail?", "status": "ok", "http_status": 200, "answer": "According to the documents, you can declare a course pass/fail \"up to week eight\" or \"as late as week eight\" (thread_first_year_regret.txt and thread_pass_fail.txt).", "refused": false, "sources": ["thread_first_year_regret.txt", "thread_pass_fail.txt"], "best_distance": 0.2282, "threshold": 0.5, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 753.0, "retrieve_ms": 90.1, "gate_ms": 0.0, "generate_ms": 662.37, "prompt_tokens": 433, "output_tokens": 47, "cache_hit": false, "max_rss_mb": 769.2, "error": null}
{"timestamp": "2026-11-17T20:30:34.333Z", "request_id": "35288c7b39f34cac8370da3c6d7c1290", "endpoint": "/ask", "question": "In the dorms when will the laundry actually be free?", "status": "ok", "http_status": 200, "answer": "Based on the provided documents, laundry is actually free in the dorms \"Tuesday and Wednesday mornings, every building\" (thread_laundry_timing.txt).", "refused": false, "sources": ["thread_commuting.txt", "thread_laundry_timing.txt", "thread_roommate_conflict.txt"], "best_distance": 0.1689, "threshold": 0.5, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 673.3, "retrieve_ms": 92.53, "gate_ms": 0.0, "generate_ms": 580.44, "prompt_tokens": 408, "output_tokens": 33, "cache_hit": false, "max_rss_mb": 769.5, "error": null}
{"timestamp": "2026-11-17T20:30:35.327Z", "request_id": "658d014a0471406d9b63571dbc0f17dc", "endpoint": "/ask", "question": "What can I do if I'm having trouble with my roomates?", "status": "ok", "http_status": 200, "answer": "If you are having trouble with your roommates, you should \"Talk to your RA early, and frame it as 'we need help sorting this out' rather than 'move me'.\" You should also \"Write down specifics before the meeting.\" \n\nSource: thread_roommate_conflict.txt", "refused": false, "sources": ["thread_laundry_timing.txt", "thread_roommate_conflict.txt", "thread_study_spots.txt"], "best_distance": 0.4473, "threshold": 0.5, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 23295.1, "retrieve_ms": 98.79, "gate_ms": 0.0, "generate_ms": 23195.7, "prompt_tokens": 431, "output_tokens": 59, "cache_hit": false, "max_rss_mb": 769.6, "error": null}
{"timestamp": "2026-11-17T20:30:58.942Z", "request_id": "c5f75607a9d346febb4a186c42b882da", "endpoint": "/ask", "question": "Can I go to office hours withotu questions?", "status": "ok", "http_status": 200, "answer": "Yes, it is not weird to go to office hours with no specific question; they are usually empty and you are doing the instructor a favour by turning up. \n\n(Source: thread_office_hours_etiquette.txt)", "refused": false, "sources": ["thread_office_hours_etiquette.txt", "thread_professor_email.txt"], "best_distance": 0.3312, "threshold": 0.5, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 1642.8, "retrieve_ms": 138.16, "gate_ms": 0.01, "generate_ms": 1504.32, "prompt_tokens": 420, "output_tokens": 48, "cache_hit": false, "max_rss_mb": 769.6, "error": null}
{"timestamp": "2026-11-17T20:31:00.905Z", "request_id": "30b60f15ed744e01a28f4f1e3f33379a", "endpoint": "/ask", "question": "Are parking permits worth it?", "status": "ok", "http_status": 200, "answer": "According to thread_parking.txt, if you are commuting daily, the west permit is worth the August scramble, but otherwise you should not bother.", "refused": false, "sources": ["thread_bike_commute.txt", "thread_parking.txt"], "best_distance": 0.301, "threshold": 0.5, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 1230.9, "retrieve_ms": 95.7, "gate_ms": 0.0, "generate_ms": 1134.89, "prompt_tokens": 417, "output_tokens": 30, "cache_hit": false, "max_rss_mb": 769.6, "error": null}
{"timestamp": "2026-11-17T20:31:02.456Z", "request_id": "c7b6f011453c4b5cbb45acf43bb3e512", "endpoint": "/ask", "question": "Whats the last to make a course pass/fail?", "status": "ok", "http_status": 200, "answer": "You can declare it as late as \"week eight\" (from thread_pass_fail.txt and thread_first_year_regret.txt).", "refused": false, "sources": ["thread_first_year_regret.txt", "thread_pass_fail.txt"], "best_distance": 0.2282, "threshold": 0.5, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 764.0, "retrieve_ms": 103.81, "gate_ms": 0.0, "generate_ms": 659.88, "prompt_tokens": 433, "output_tokens": 32, "cache_hit": false, "max_rss_mb": 769.6, "error": null}
{"timestamp": "2026-11-17T20:31:03.548Z", "request_id": "c3070debedc74d639baeb483d5a6d4ad", "endpoint": "/ask", "question": "What is the capital of Mongolia?", "status": "refused", "http_status": 200, "answer": "I don't have enough information about that.", "refused": true, "sources": [], "best_distance": 0.899, "threshold": 0.5, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 93.1, "retrieve_ms": 92.9, "gate_ms": 0.0, "generate_ms": 0.0, "prompt_tokens": 0, "output_tokens": 0, "cache_hit": false, "max_rss_mb": 769.6, "error": null}
{"timestamp": "2026-11-17T20:31:03.957Z", "request_id": "affa6085f99643faab1365a9255e07fd", "endpoint": "/ask", "question": "How do I change the oil in a diesel engine?", "status": "refused", "http_status": 200, "answer": "I don't have enough information about that.", "refused": true, "sources": [], "best_distance": 0.9047, "threshold": 0.5, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 90.8, "retrieve_ms": 90.56, "gate_ms": 0.0, "generate_ms": 0.0, "prompt_tokens": 0, "output_tokens": 0, "cache_hit": false, "max_rss_mb": 769.6, "error": null}
{"timestamp": "2026-11-17T20:31:04.365Z", "request_id": "4f8c99cad815487d9b9fddb7f341953a", "endpoint": "/ask", "question": null, "status": "rejected", "http_status": 400, "answer": null, "refused": null, "sources": null, "best_distance": null, "threshold": null, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 0.2, "retrieve_ms": null, "gate_ms": null, "generate_ms": null, "prompt_tokens": 0, "output_tokens": 0, "cache_hit": false, "max_rss_mb": 769.6, "error": "missing question or invalid JSON"}
{"timestamp": "2026-11-17T20:31:13.291Z", "request_id": "488ebcc8e2244e3380fb0bb313fb76a6", "endpoint": "/ask", "question": "In the dorms when will the laundry actually be free?", "status": "error", "http_status": 500, "answer": null, "refused": null, "sources": null, "best_distance": null, "threshold": null, "corpus": "advice_threads", "model": "gemini-3.5-flash-lite", "top_k": 5, "duration_ms": 2056.5, "retrieve_ms": 1098.28, "gate_ms": 0.02, "generate_ms": null, "prompt_tokens": 0, "output_tokens": 0, "cache_hit": false, "max_rss_mb": 678.8, "error": "ClientError: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}"}
```

Entry 13 (rejected, HTTP 400, the empty question) and entry 14 (error, HTTP 500, the invalid API key, from a second server session) are the failed ones. Entry 7 has a `generate_ms` of 23195.7.

**What It Costs**

Measured from the run record above. The server was started with:

```
AI201_CORPUS=advice_threads AI201_CACHE=0 AI201_LOG_PATH=logs/run_record_cost_check.jsonl python -m gunicorn serve:app
```

with the answer cache off and a fresh server process, so the first request was a real cold start. The 10 answered requests (the five questions in `questions.py`, twice) were sent one after another with `drive.py`'s `ask()` function, called from a small script that also sampled memory between requests (that script is not committed), followed by 2 out-of-scope questions and 1 empty one. The numbers come from:

```
python summarize_log.py logs/run_record_cost_check.jsonl
python summarize_log.py logs/run_record_cost_check.jsonl --skip-first
```

| Per answered request | All 10 | 9 warm (first skipped) |
|---|---|---|
| Mean prompt tokens | 421.8 | 423.3 |
| Mean output tokens | 44.7 | 46.6 |
| Mean seconds (`duration_ms`) | 3.56 | 3.60 |
| Median seconds (`duration_ms`) | 1.12 | 1.00 |
| Max seconds | 23.30 | 23.30 |
| Cache hits | 0 of 10 | 0 of 9 |

The means are pulled up by entry 7 (23.3 s), which is in both columns, so the medians are the more typical figure. The two refused questions made no model call and used 0 tokens (about 0.09 s each).

Cold start, reported separately: the first request (entry 1) had a `retrieve_ms` of 1437.98 and a `duration_ms` of 3125.9. The median `retrieve_ms` of the 9 warm requests was 98.79.
