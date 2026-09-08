# AI Agents — Code

Runnable code from *AI Agents: Designing, Orchestrating, and Governing
LLM-Based Systems* by Michael Bücker and Michael Hewing.

One notebook per chapter, generated from the book's sources. Do not edit
the notebooks by hand — changes belong in the manuscript and are
regenerated from there.

## Status

These notebooks currently require an **Azure OpenAI** resource. Support for
plain `OPENAI_API_KEY` and other OpenAI-compatible endpoints is in
preparation.

## Setup

```bash
git clone https://github.com/ai-agents-book/code.git
cd code
uv sync
cp .env.example .env   # then fill in your own values
```

`uv.lock` pins the exact versions the book's printed outputs were produced
with. Installing anything newer may change what you see.

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

The chapter notebooks make **real API calls that cost money**. Chapters 1
and 2 are the largest, at roughly forty calls between them. Nothing here
runs against a free tier by default.

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
