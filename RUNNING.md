# Capstone: how to run this (Path B, local with logs)

The Unofficial Guide is a question-answering service over 23 student advice threads (75 chunks, the `advice_threads` corpus). It retrieves the closest replies, refuses questions the threads don't cover, and otherwise asks a hosted Gemini model to answer from them, naming its sources. Every `/ask` request is written to a structured log.

## Environment

- **OS tested:** macOS 26.0.1 (arm64).
- **Python:** 3.13.15. Supported versions are 3.11 to 3.13, not 3.14.
- **Dependencies:** the pinned `requirements.txt`. The main ones are `chromadb` (0.6.x, vector store and the embedder), `flask` (the web service), `gunicorn` (the server), `google-genai` (the Gemini client), and `python-dotenv`.
- **Embedding model:** `all-MiniLM-L6-v2` as an ONNX file, run on your own machine. It is 87 MB unpacked plus a 79 MB tarball, about 166 MB for the whole `~/.cache/chroma` folder. It is downloaded the first time it is used, from `chroma-onnx-models.s3.amazonaws.com`, into `~/.cache/chroma`.
- **Disk:** a fresh `.venv` is about 432 MB and the model cache in `~/.cache/chroma` about 166 MB, so allow roughly 600 MB plus the repo.
- **Generation calls a hosted Gemini model**, so you need a `GEMINI_API_KEY` (free at https://aistudio.google.com).

## Steps, from a clean checkout

1. Clone and enter the repo:
   ```bash
   git clone https://github.com/hansikam07/ai201-project1-unofficial-guide-starter-v2026.git
   cd ai201-project1-unofficial-guide-starter-v2026
   ```
2. Create and activate a virtual environment (use Python 3.11 to 3.13):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   On Windows PowerShell: `python -m venv .venv` then `.venv\Scripts\Activate.ps1`.
3. Install the pinned dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create your `.env` and set the key and the corpus. The default corpus is `campus_life`, not `advice_threads`, so the last line matters:
   ```bash
   cp .env.example .env
   # open .env and paste your key after GEMINI_API_KEY=
   echo "AI201_CORPUS=advice_threads" >> .env
   ```
   (`config.py` loads `.env`, and `AI201_CORPUS` in it overrides the default.)
5. Build the index (the first run downloads the embedding model if it is not cached yet). This is slow and prints nothing while it embeds the 75 chunks: it took about 2 minutes on the tested machine, so wait for the "Ready." line:
   ```bash
   python app.py index
   ```
6. Start the service:
   ```bash
   python -m gunicorn serve:app
   ```
   On Windows gunicorn does not run; use `python serve.py` instead.

## Check that it works

The two start commands use different ports:

- `python -m gunicorn serve:app` (step 6) listens on `127.0.0.1:8000`, or on `0.0.0.0:$PORT` if `PORT` is set. **The examples below use 8000.**
- `python serve.py` (Windows) listens on port 5000, or on `$PORT` if it is set. Replace `8000` with `5000` in the examples below.
  On macOS, port 5000 is already taken by the AirPlay Receiver, so `python serve.py` fails with "Address already in use" and curl gets an HTTP 403 from AirPlay instead. Use `PORT=5001 python serve.py` there and port 5001 in the examples.

```bash
curl http://127.0.0.1:8000/health
```
Expect `"status": "ok"` and `"index_ready": true`.

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question": "In the dorms when will the laundry actually be free?"}'
```
Expect a JSON object with `question`, `answer`, `refused`, `sources`, `best_distance`, `threshold` and `corpus`. For this question the answer says laundry is free on Tuesday and Wednesday mornings and cites `thread_laundry_timing.txt`; `refused` is `false`, `best_distance` is about 0.17 and `threshold` is 0.5. The exact wording of the answer varies from run to run. A question the threads don't cover (for example "What is the capital of Mongolia?") returns HTTP 200 with `"refused": true`.

## Logs and settings

Each `/ask` request appends one JSON line to `logs/requests.jsonl` (the folder is created on the first request; `/health` is not logged). Settings, all environment variables (put them in `.env` or set them before the start command):

| Variable | What it does |
|---|---|
| `AI201_CORPUS` | which corpus to serve; set it to `advice_threads` |
| `AI201_CACHE` | `0` turns the answer cache off, which you need when measuring |
| `AI201_LOG_PATH` | where the request log is written (default `logs/requests.jsonl`) |
| `PORT` | the port to listen on |

## Known limits

The first `/ask` after the server starts is slower, because the embedding model loads then, not at startup.

---

# Running this project

Everything about how the starter works and how to use it.

---

## Before your first class

Setup happens **before class**, not during it. The
[environment setup page](../pages/ide_setup) has the per-operating-system
commands, the exact versions, and where to get your API key.

The short version, from inside this repo after you've forked and cloned it:

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then paste your key into .env
python test.py
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env         # then paste your key into .env
python test.py
```

**You're ready when `python test.py` passes.** The first run is slow — it
downloads the embedding model, about 80 MB. That's exactly why this happens
before class rather than during it.

The model comes down from Chroma's own servers, not from Hugging Face, and
embedding runs entirely on your machine. If your network blocks one of those
and not the other, this is the one that has to get through:
`chroma-onnx-models.s3.amazonaws.com`.

If it doesn't pass and you've made one honest attempt at the error, post the
**whole** output in the help channel. Setup problems are normal and nobody has
ever been judged for having one.

> **Activate the virtual environment every time you open a new terminal.** You
> should see `(.venv)` at the start of your prompt. Installing into your system
> Python instead is the single most common cause of "it worked yesterday."

---

## Your first five minutes

```bash
python app.py corpora                     # see what's available
python app.py index                       # build the search index
python app.py ask "is the housing lottery random?"
```

That's the whole pipeline running end to end. The answer won't be great yet —
you're checking that it runs at all and that your key works.

To use a different corpus:

```bash
python app.py --corpus city_guides index
python app.py --corpus city_guides ask "how do I get to Kestrelford?"
```

Or set `CORPUS` in `config.py` once and stop typing it. **Re-run `index` after
switching corpora.**

---

## Every command

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment. Run it whenever something feels off |
| `python app.py corpora` | Lists the provided corpora with a one-line description |
| `python app.py index` | Loads, chunks, embeds and stores your corpus. Run after any change to chunking |
| `python app.py ask "question"` | Asks one question, end to end |
| `python app.py ask` | Keeps asking until you press Enter on an empty line |
| `python app.py chunks` | Prints sample chunks — **Milestone 3** |
| `python app.py retrieve "question"` | Shows distances without spending a model call — **Milestone 4** |
| `python run_eval.py --label before` | Runs every test question three times, puts every `OUT_OF_SCOPE` question through the gate, and writes a run log — **unit 2** |

Useful flags:

| Flag | Works on | What it does |
|---|---|---|
| `--corpus NAME` | all | Use a different corpus without editing `config.py` |
| `--variant NAME` | `index`, `ask`, `retrieve` | Keep two different indexes of the same corpus side by side |
| `-n 5` | `chunks` | How many chunks to print |
| `--top-k 8` | `ask`, `retrieve` | Retrieve more or fewer chunks |
| `--threshold 0.7` | `ask` | Try a different relevance cutoff without editing `config.py` |
| `--label before` | `run_eval.py` | Names the output file, so before and after are distinguishable |

---

## Which command goes with which milestone

| Milestone | What you're doing | Command |
|---|---|---|
| 1 | Pick a corpus and see it work | `app.py corpora`, `app.py index`, `app.py ask "..."` |
| 2 | Write your acceptance criteria | Edit `criteria.md` and `questions.py` |
| 3 | Swap in your own chunker | Edit `chunker.py`, then `app.py index` and `app.py chunks` |
| 4 | Tune retrieval, set your cutoff | `app.py retrieve "..."`, then edit `THRESHOLD` in `config.py` |
| 5 | Write it up | Fill in `README.md` |
| Unit 2 | Run the test, fix one thing, re-run | `run_eval.py --label before` … `run_eval.py --label after` |

`app.py chunks` prints each chunk with its **source file and the function that
produced it** — both of which your README has to name. Copy them straight
across.

`run_eval.py` also runs the five questions in `OUT_OF_SCOPE` at the bottom of
`questions.py` through retrieval and the relevance gate, and puts what happened
in the run log under its own heading. That's the evidence for criterion 3, and
it costs you nothing: a question the gate refuses never reaches the model, so
there is no API call. It runs them once rather than three times, because
retrieval is deterministic and the gate is a comparison against a fixed
number — three passes would produce the same three answers.

---

## Where everything lives

| File | What it does |
|---|---|
| `config.py` | Every setting worth changing: chunk size, overlap, top-k, the relevance cutoff |
| `ingest.py` | Loads documents off disk and cleans them — **stage 1** |
| `chunker.py` | Splits documents into chunks — **stage 2, and the file you replace in Milestone 3** |
| `store.py` | Embeds chunks, stores them, retrieves them with distances — **stages 3 and 4** |
| `gate.py` | The relevance gate. Refuses questions nothing came back close enough for |
| `generate.py` | Writes the answer — **stage 5**. The only thing that calls out to a service |
| `app.py` | The command line |
| `serve.py` | The same pipeline behind HTTP, for when it has to run as a service — **unit 9** |
| `run_eval.py` | Runs your questions repeatedly and writes the run log |
| `questions.py` | Your five test questions, and the five out-of-corpus ones the gate should refuse. **You fill in the first five** |
| `criteria.md` | Your five acceptance criteria. **You fill this in** |
| `README.md` | Your submission |
| `corpora/` | The provided documents, and `corpora/README.md` describing each |
| `results/` | Run logs, written by `run_eval.py`. **Commit these** — they're your evidence |

The five stages matter more than they look. In unit 2 you diagnose each failure
by naming which stage caused it, so it's worth knowing now which file is which.

---

## About rate limits

The free tier allows a small number of calls per minute. `generate.py` handles
this for you:

- **It paces its own requests** and prints a message when it's waiting. **A
  pause is the starter doing its job, not a bug.**
- **It caches repeated prompts** while you're building, so re-running the same
  question twenty times while debugging costs one call.
- **Caching turns itself off during evaluation runs.** Three runs of the same
  question have to be three real answers, not one answer repeated.
- **It stops if a session makes an unreasonable number of calls**, rather than
  silently draining your whole day's allowance. If you hit that, you almost
  certainly have a loop running away — look for it before raising the limit in
  `config.py`.
- **It prints how many calls and tokens you've used** when you exit. The
  token counts come off the responses themselves, so they're a measurement of
  what a run cost rather than an estimate.

If you see a `429` or "resource exhausted" error, that's a rate limit and not a
broken key. Wait a minute and re-run.

---

## When something goes wrong

| What you see | What it means |
|---|---|
| `No index called '...'. Run python app.py index first.` | You haven't indexed, or you switched corpus without re-indexing |
| `No GEMINI_API_KEY found` | No `.env` file, or the key wasn't pasted in. On Windows check it didn't save as `.env.txt` |
| `No corpus at ...` | The corpus name is wrong. `python app.py corpora` lists the real ones |
| The system refuses everything | Your cutoff is too low for this corpus. Try `--threshold 0.75` to confirm, then set it properly in Milestone 4 |
| The system never refuses anything | Your cutoff is too high. Same process in reverse |
| `[rate limit] ... Waiting 34s` | Working as intended. Leave it |
| `QuotaGuard: This session has made 300 requests` | A loop is running away. Find it before raising the budget |
| Indexing is very slow | Expected on the first run — it's downloading the embedding model. Later runs are much faster |

Still stuck after one honest attempt? Post in the help channel with the full
error, what you ran, and what you expected. You are not expected to debug your
own machine alone.

---

## Running it somewhere else — **unit 9**

Unit 1 doesn't need this. It's here because the file it describes ships in the
starter, and finding out in unit 9 that it exists is worse than reading one
table now.

`serve.py` puts the same pipeline behind HTTP, so it can run as a service that
stays up instead of a command that exits.

```bash
python serve.py                    # locally, on port 5000
gunicorn serve:app                 # the way a host starts it
```

| Thing | What it does |
|---|---|
| `POST /ask` | Send `{"question": "..."}`, get the answer and its sources back as JSON |
| `GET /health` | Says whether the service is up and whether an index exists to search |
| `PORT` | The port to listen on. Hosts set it for you; on your laptop it defaults to 5000 |
| `AI201_DEBUG=1` | Flask's reloader and debugger. Local only — never set it on a deployed service |

> The free hosting tier sleeps after about fifteen minutes with no traffic, so
> the first request after a quiet spell waits roughly a minute for it to wake
> up. That's the tier, not your code.

`serve.py` has **no logging and no timing in it on purpose** — building that is
the unit 9 exercise, and it is easier to instrument something you wrote.

---

## Stretch features

Optional, for extra credit. **Say what you're adding in your README before you
start** — a feature the README never claims earns nothing.

- **Metadata filtering** — let people narrow results by source or date. Chroma
  supports a `where` clause on `collection.query`; `store.py::search` is where
  it would go.
- **Conversational memory** — let the next question build on the last.
- **A second embedding model** — swap `EMBEDDING_MODEL` in `config.py`, index
  into a different `--variant`, and write down what moved. This is the one
  option that needs a package the default install doesn't have:
  `pip install 'sentence-transformers>=3.4,<3.5'` first. It's a large install
  (it brings PyTorch), so do it before class, not during. Expect your
  threshold to move too — a different model means different distances, and
  the 0.6 you measured in Milestone 4 was measured against this one.

`rank-bm25` is already installed for unit 2's hybrid-search option. The
dependency ships; the implementation is yours.

---

## A note on committing

Commit as you go — at least four new commits in unit 1, at least four more in
unit 2. Your commit history is what shows your criteria existed before your
results did.

**Do not delete and recreate this repository.** You submit the same URL both
units.

`results/` is deliberately **not** in `.gitignore`. Your run logs are evidence
that the test actually happened, and they're part of what gets graded.
