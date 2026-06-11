# ShiftNotes — Gmail API Setup Guide

**For teammates cloning from `https://github.com/wanlemvo/ShiftNotes`**

---

## What changed from the original repo

The original ShiftNotes used OpenAI's MCP Gmail connector (controlled by `GMAIL_OAUTH_TOKEN`). That was replaced with a direct **Google Gmail API** integration using `google-api-python-client`. Three things changed:

| File | What changed |
|---|---|
| `shiftnotes_agent/nodes/send_briefing.py` | Rewritten — now uses `google-api-python-client` directly instead of MCP |
| `generate_gmail_token.py` | **New file** — one-time script to generate `token.json` |
| `pyproject.toml` | Added three Google dependencies |
| `.gitignore` | Added `credentials.json`, `token.json`, `client_secret*.json` to keep secrets out of git |

> **Note:** The `.env.example` still shows `GMAIL_OAUTH_TOKEN` — that variable is a leftover from the MCP era and is **not used** by the current code. You can ignore it.

---

## Step 1 — Clone and install dependencies

```bash
git clone https://github.com/wanlemvo/ShiftNotes
cd ShiftNotes
pip install uv          # if you don't have uv yet
uv sync
```

`uv sync` installs everything in `pyproject.toml`, including the three Google packages:
- `google-api-python-client`
- `google-auth-httplib2`
- `google-auth-oauthlib`

---

## Step 2 — Get `credentials.json` from Google Cloud Console

This file proves your app is allowed to call the Gmail API. Each teammate needs their own, tied to their own Google account.

1. Go to [https://console.cloud.google.com/](https://console.cloud.google.com/) and sign in with the Google account that will **send** the briefing emails.
2. Create a new project (or select an existing one).
3. Navigate to **APIs & Services → Library**, search for **Gmail API**, and click **Enable**.
4. Navigate to **APIs & Services → Credentials**.
5. Click **Create Credentials → OAuth client ID**.
6. If prompted to configure the OAuth consent screen: choose **External**, fill in app name (e.g. "ShiftNotes"), add your email as a test user, and save.
7. Back in **Create OAuth client ID**: choose **Desktop app** as the application type. Name it anything (e.g. "ShiftNotes Desktop").
8. Click **Create**, then **Download JSON**.
9. Rename the downloaded file to exactly `credentials.json` and place it in the project root (same folder as `run_pipeline.py`):

```
ShiftNotes/
├── credentials.json   ← here
├── run_pipeline.py
├── generate_gmail_token.py
...
```

> `credentials.json` is in `.gitignore` — it will never be committed.

---

## Step 3 — Set up your `.env` file

```bash
cp .env.example .env
```

Open `.env` and fill in these values:

```dotenv
OPENAI_API_KEY=sk-...          # required — pipeline exits without this
GROQ_API_KEY=gsk_...           # optional — only needed for the Streamlit RAG tab
GMAIL_OAUTH_TOKEN=             # leave blank — not used by current code
TED_EMAIL=ted@example.com      # required for Gmail send; without it briefing saves to file
```

The only two that matter for Gmail delivery are **`OPENAI_API_KEY`** and **`TED_EMAIL`**.

---

## Step 4 — Run `generate_gmail_token.py` to authenticate

This is a one-time step. It opens a browser window, asks you to sign in to Google, and saves an OAuth token to `token.json`.

```bash
uv run python generate_gmail_token.py
```

What happens:
1. A browser window opens asking you to sign in with the Google account from Step 2.
2. You'll see an "unverified app" warning (expected for dev apps) — click **Continue**.
3. Grant the permission: **"Send email on your behalf"**.
4. The browser shows a success message. Close it.
5. Back in the terminal you'll see:

```
token.json saved to .../ShiftNotes/token.json
```

`token.json` is now in the project root alongside `credentials.json`. It is also in `.gitignore` and will never be committed.

> `token.json` auto-refreshes when it expires, as long as `credentials.json` is still present. You should only need to run this script once per machine.

---

## Step 5 — Verify the pipeline sends via Gmail

Run the pipeline:

```bash
uv run python run_pipeline.py
```

Watch the console output. A successful Gmail send produces this sequence:

```
✓ Node completed: ingest_email
✓ Node completed: classify_intent
✓ Node completed: detect_signals
✓ Node completed: retrieve_and_generate
✓ Node completed: send_briefing          ← briefing delivered here

==================================================
PIPELINE PAUSED — AWAITING TED'S DECISION
==================================================
```

In the structured logs, look for:

```
[send_briefing] Briefing sent to ted@example.com via Gmail API — message_id: 18f...
```

If you see this line, Gmail delivery worked. Ted's inbox will have the email before you are prompted for a decision.

---

## Fallback behavior (when Gmail is not configured)

If credentials are missing or `TED_EMAIL` is not set, `send_briefing` automatically falls back to saving a `.txt` file:

```
[send_briefing] TED_EMAIL not set — saving briefing to file
[send_briefing] Briefing saved to briefings/briefing_20260610_143022_a1b2c3d4.txt
```

The pipeline continues normally either way — the HITL checkpoint in Node 6 still fires.

---

## Quick checklist

- [ ] `credentials.json` in project root (from Google Cloud Console)
- [ ] `generate_gmail_token.py` run once → `token.json` generated
- [ ] `TED_EMAIL` set in `.env`
- [ ] `OPENAI_API_KEY` set in `.env`
- [ ] `uv sync` completed with no errors
