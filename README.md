# Crypto KPI Pipeline — Take-Home Starter

This is a starter project for a 2-hour take-home exercise. It contains a working-ish but flawed pipeline that:

1. Fetches the top 10 cryptocurrencies from the public CoinGecko API
2. Computes a few KPIs (top gainers, top losers, market cap stats)
3. Stores the result in MinIO (an S3-compatible object store)
4. Displays the result in a Streamlit dashboard

## Stack

- **Python 3.11** for the pipeline and dashboard
- **CoinGecko public API** for data (no API key required)
- **MinIO** as a local S3-compatible object store
- **Streamlit** for the dashboard
- **Docker Compose** to run everything together

## Running the project

```bash
docker compose up --build
```

Then visit:

- Dashboard: http://localhost:8501
- MinIO console: http://localhost:9001 (login: `minioadmin` / `minioadmin`)

> Heads up: running `docker compose up` once and expecting it to "just work" is part of the exercise. If it doesn't, that's a clue, not a blocker.

## Your task (~2 hours)

The starter runs in the happy path but has problems. Your job is to make it better. Please:

1. **Get it running.** You may need to fix at least one thing just to make the dashboard show data.
2. **Find and fix bugs.** There are correctness bugs in the data processing — at least two. Find them, fix them, and tell us what you found.
3. **Add error handling.** What happens when the API is slow, returns an error, or returns unexpected data? What happens when MinIO isn't ready yet?
4. **Improve the structure.** The code is procedural, repetitive, and full of hardcoded values. Refactor toward something you'd be comfortable maintaining — OO, modules, or any structure you can defend.
5. **Pick one extra improvement of your choice.** Examples: logging, tests, env-var config, retry/backoff, a new KPI, a chart, a `Makefile`, CI, etc. Tell us why you chose it.

Don't try to do everything. **Two solid, well-reasoned improvements beat ten half-finished ones.**

## What to submit

A link to a Git repo containing:

- Your modified code
- A `CHANGES.md` listing:
  - The bugs you found and how you fixed them
  - The improvements you made and why you chose them
  - One paragraph at the end: what you'd do next with another two hours
- Your AI prompt history (if you used any AI tool), in any format — `prompts.md`, exported chat, screenshots, all fine

## A note on AI

Using AI assistants (Claude, ChatGPT, Copilot, Cursor, etc.) is fully allowed and won't count against you. We will, however, ask you to walk us through your code and explain your decisions in the follow-up call. Ship things you understand.

## Ground rules

- Cap yourself at ~2 hours of focused work. If you go over, write down what you would have done and stop.
- If anything in the brief is genuinely unclear, ask. Knowing when to ask is part of what we're evaluating.
- Have fun.
