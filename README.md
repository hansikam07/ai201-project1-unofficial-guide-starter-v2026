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

I picked the advice threads corpus about student life such as laundry, parking, roomates, office hours, and pass/fail. The model retrieves the relevent reply chunks based on the question. It gets the replies only from the sources and also names the used sources. If the question doesn't have any relevent information in the sources it doesn't answer instead. 

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

Since the original chunker was juts fixed to 800chars, it didn't properly reply. Based on milestone 1 I saw the the replies were already complete and variable so spliting them by char wasn't effective. instead I changed the chunkingt to be based of the --- reply N (votes) --- marking instead and it resulted in proper chunks that were decently sized. 

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

When I ran my questions the best distances were between 0.15-0.28 and the out of scope ones were between 0.82-0.91 since there is alrge gap with no overlap I chose 0.5 since it was between the high end of the best and low end of the out of scope.

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
A moment I used AI is for the chunker which I then split bny reply markers rather than the char count. Th AI came back with a working regex-based splitter. I ran python app.py --corpus advice_threads index and then did  chunks -n 5 to check for my self and using that I confirmed for myself. 

**2.**
I used AI to help set the relevence cut off after running eveyrthing my self I put in the results into AI to do the math on the numbers for the ranges and the overlaps. Then I checked the suggested cut off and decided it was appropriate and implemented it. 

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

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

## Run Log — Before

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

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
