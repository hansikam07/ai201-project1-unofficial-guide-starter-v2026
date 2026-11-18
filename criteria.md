# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
The question about the roomate troubles has three replies so it might not have a single retrieved chunk. 
---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->

This is to make sure that each answer is actually from teh sources so we need all five and thsi will test is the model works or not.
> **Revised reason (resubmission):** Every answered question must name a file because `generate.py::build_prompt` tags each chunk '[from <filename>]' and `GROUNDING_INSTRUCTION` tells the model to cite it, so five of five is achievable here. Questions the gate refuses never reach the model and name no source by design, so this criterion covers answered questions only. An answer with no source can't be told apart from a hallucination, which is why four of five wouldn't do.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

Yes there was a clean gap. The in-corpus 0.15-0.28 and teh out-of-scope is 0.82-0.91 there is a lrgae gap with no overlap so I made the cutoff 0.5 right in the middle of both. 

---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->



**Why this target:**

The fallback chunker makes 2char and 793 char chunk with teh same corpus so there isn't control. Instead since every reply is self-contained per reply splitting will keep the chunks collected thoughts. 


> **Added in resubmission (Nov 2026):** At least 4 of 5 sampled chunks (from
> `python app.py chunks -n 5`) read as a complete standalone thought, with no
> sentence cut off at either end.
>
> This was added after I had results. The original Criterion 4 above has a
> reason but no criterion sentence, because I left that line blank in unit 1.
> This sentence is the wording I used in my Unit 2 table ("Chunk completeness,
> 4 of 5"), so it states the target that was actually checked rather than a
> new one.

---

## 5. Your choice

My 5 in-corpus's best distance is at least that 0.15 lower on average than the out-of-scope 5 questions's best. 

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->



**Why this target:**

This will help in refusing to answer what it doesn't know since you can't check that by numbers,  0.15 I feel works best so that it won't have a false pass. Since the in corpus average is 0.277 and the out of scope is 0.876, witha large gap of 0.65 is bigger than my 0.15 target. 



> **Correction:** The in-corpus average I wrote in the reason above (0.277)
> does not match the five best distances in my README table (0.150, 0.244,
> 0.278, 0.183, 0.282), which average 0.227. The "0.65 gap" I wrote matches
> 0.227 (0.876 - 0.227 = 0.649), not 0.277, so the gap was right and the
> average was a typo.
>
> The Unit 2 run log (`results/run_2026-09-30_0002_before.md`) uses the exact
> wording in `questions.py`, which differs from the wording behind the
> Milestone 4 table, so its best distances are different: 0.1689, 0.4473,
> 0.3312, 0.3010, 0.2282, average 0.295, giving a gap of 0.58 against the
> out-of-scope average of 0.876. Both gaps are well past the 0.15 target.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->

## Capstone

1. Latency
The measurement will use duration_ms per request across the in-scope questions from the 15-question evaluation set, excluding out-of-scope questions since they are refused and do not call Gemini. Caching will be turned off using AI201_CACHE=0. The goal is for at least 95 of the 99 requests remaining after skipping the first cold request to finish under 5 seconds. This is based on the warm median of about 1.1 seconds, and the 23-second request would fail. A 5-second limit allows some variation without accepting unusually slow requests. Testing will use drive.py with --n 100 and --url, followed by summarize_log.py --skip-first. The script cycles through the 15 questions until it reaches the requested 100 requests.

2. Failure path
The failure path will be tested by setting an incorrect GEMINI_API_KEY before starting the server, with caching turned off to prevent cached answers from bypassing Gemini. All 3 out of 3 requests should return JSON with a 5xx HTTP status and a non-empty error field in the response. The log should also show status: "error" with a non-empty error field. Responses should finish within 30 seconds to avoid Gunicorn returning HTML. Testing will involve starting the server with the wrong key and sending 3 questions using drive.py or curl. All 3 requests must pass because one incorrectly handled error would mean the failure path is not fully reliable.

3. Log completeness
Testing will start with an empty log file using a fresh AI201_LOG_PATH and produce 50 records across two runs: 40 successful requests, 5 refusals and 5 errors. The successful requests will be sent normally, refusals will be triggered using --out-of-scope, and the 5 errors will be sent in a separate run using the same wrong-key setup from Criterion 2 with caching turned off. Each record must contain all 23 required fields, even if some values are null or empty, but status cannot be null. The /health endpoint is excluded. A script will count records and check for missing fields. This test is expected to pass based on the current logging behavior.

4. Memory
The measurement will use max_rss_mb, which is the maximum memory usage across 50 requests, using the default ONNX provider selected by the installed environment and one worker. No CPU-only override or temporary wrapper will be used. The goal is to stay under 400 MB. This is based on the earlier default-provider result of about 770 MB, compared to about 297 MB when a temporary wrapper forced CPUExecutionProvider. A 400 MB limit allows some extra memory variation without being too high. Testing will involve starting the server using the normal instructions in RUNNING.md, sending 50 requests and checking the maximum value in the log. The 50 requests will include a mix of successful questions and refusals. Based on the earlier result, this test is expected to miss the target.

5. Load
Normal load will be tested at 1 request every 10 seconds for 60 seconds, giving 6 requests, while 10x load will be tested at 1 request per second for 60 seconds, giving 60 requests. All 6 normal requests must succeed, while at least 57 of 60 requests must return HTTP 2xx under 10x load. A 200 refusal counts as success, while client timeouts and HTTP 429 responses count as failures. Gemini rate limits will be identified through the log's error field but will still count as misses. Testing will use drive.py with --rate, --n, --concurrency 10, --max-inflight 10 and --timeout 60. The 95% target allows a small number of failures while still requiring most requests to succeed, making it stricter than a 90% target without requiring perfect results.

Clarifications Made Before Tests

* Criterion 1: The in-scope evaluation set contains 5 questions, which will be repeated 20 times to reach 100 total requests.
* Criterion 5: The `--concurrency` flag cannot be combined with `--rate`, so the load test will use `--rate` with `--max-inflight 10` to allow requests to overlap.
* Pacing constraint: The 30-requests-per-minute pacing in `generate.py` will affect Criteria 1, 3, and 5. This is a known constraint of the current implementation. The targets for all three criteria remain unchanged.
