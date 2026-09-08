# AI Agents — Code

Runnable code from *AI Agents: Designing, Orchestrating, and Governing
LLM-Based Systems* by Michael Bücker and Michael Hewing.

One notebook per chapter, generated from the book's sources. Do not edit
the notebooks by hand — changes belong in the manuscript and are
regenerated from there.

## What you need

An API key for OpenAI or for any OpenAI-compatible endpoint — a hosted
provider, a self-hosted model server, or a gateway in front of either. The
notebooks construct the client with a bare `OpenAI()`, which reads
`OPENAI_API_KEY` and, when set, `OPENAI_BASE_URL` from the environment.

If your organization provides **Azure OpenAI** and nothing else, the client
construction differs by a few lines and everything after it is identical.
Both forms are in `reference/api-clients.md` and in the book's setup
appendix.

## Setup

```bash
git clone https://github.com/ai-agents-book/code.git
cd code
uv sync
cp .env.example .env   # then fill in your own values
```

**`CHAT_MODEL` and `EMBED_MODEL` have no defaults and must be set.** The
book deliberately pins no model, so that it does not name a choice
providers retire on their own schedule. Set them to identifiers your
provider actually serves; a notebook left without them fails immediately
with a `KeyError` naming the missing variable.

`uv.lock` pins the exact versions the book's printed outputs were produced
with. Installing anything newer may change what you see.

The outputs printed in the book were generated with GPT-4o. A different
model will phrase its answers differently and may make different
tool-calling choices, so expect the structure of each result to match
rather than its exact wording.

### Chapter 1's word-embedding data

Chapter 1's notebook loads pretrained GloVe word vectors from
`assets/glove.6B.100d.txt`. That file is **347 MB** and is deliberately
**not included in this repository** -- shipping it would make every clone
carry a third of a gigabyte nobody but chapter 1 needs. Fetch it once,
before opening `notebooks/ch01-llms.ipynb`:

```bash
python scripts/fetch_assets.py
```

The script downloads the full GloVe 6B archive (**about 862 MB**) and keeps
only the one file the notebook uses, deleting the rest. It uses only the
Python standard library, so it runs before `uv sync`, and it does nothing
if `assets/glove.6B.100d.txt` is already present -- safe to re-run.

## Cost

The chapter notebooks make **real API calls that cost money**. Across all
of them there are about thirty call sites, and several sit inside agent
loops or probe lists, so the number of requests a full run actually issues
is higher and depends on how the model behaves. Chapters 4, 1 and 13 are
the heaviest; chapters 5 and 13 have a single call site each but chapter
13 runs it against five probes. Nothing here uses a free tier by default.

## Chapters

| Chapter | Notebook |
|---|---|
| 1 — Large Language Models | `notebooks/ch01-llms.ipynb` |
| 2 — Tools | `notebooks/ch02-tools.ipynb` |
| 3 — Memory | `notebooks/ch03-memory.ipynb` |
| 4 — Flow | `notebooks/ch04-flow.ipynb` |
| 5 — Integration | `notebooks/ch05-integration.ipynb` |
| 10 — Orchestration | `notebooks/ch10-orchestration.ipynb` |
| 11 — Governance | `notebooks/ch11-governance.ipynb` |
| 13 — Security | `notebooks/ch13-security.ipynb` |
| Appendix C — Deep Learning | `notebooks/appc-deeplearning.ipynb` |

Chapters 6 to 9 and 12 contain no executable code. Appendix B's Python
snippets are in `reference/python-primer.md`. Appendix A's two
client-construction snippets — an Azure client and an OpenAI-compatible
one — are in `reference/api-clients.md`; the book does not execute either.
