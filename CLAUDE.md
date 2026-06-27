# ShiftNotes — Agent Pipeline

## Setup

1. Clone the repo
2. Install uv if not already: `pip install uv`
3. Install dependencies: `uv sync`
4. Copy `.env.example` to `.env` and add your OpenAI API key
5. Run the pipeline: `uv run python run_pipeline.py`

## Project Structure

- `shiftnotes_agent/` — LangGraph agent pipeline
  - `nodes/` — one file per graph node
  - `tools/` — signal classifier
  - `state.py` — shared state definition
  - `graph.py` — graph wiring and compilation
  - `logger.py` — structured logging
- `prototype/` — original Jupyter notebook prototype
- `run_pipeline.py` — end-to-end demo runner
- `briefings/` — generated briefing output files

## Running the demo

```bash
uv run python run_pipeline.py
```

When prompted, enter one of: `accept` | `drill_down` | `escalate`

## Environment variables

| Variable | Description |
|---|---|
| OPENAI_API_KEY | Your OpenAI API key (required — pipeline exits if missing) |
| GROQ_API_KEY | Your Groq API key (used by RAG tab in Streamlit) |
| JOTFORM_OAUTH_TOKEN | OAuth token for JotForm MCP connector (optional — falls back to CSV if not set) |
| JOTFORM_FORM_ID | JotForm form ID to fetch submissions from (required with JOTFORM_OAUTH_TOKEN) |
| TED_EMAIL | Recipient email address for Node 5 briefing delivery (required for Gmail send — falls back to file if not set) |

## Notes

- Node 1 (ingest_email) uses JotForm MCP when `JOTFORM_OAUTH_TOKEN` and `JOTFORM_FORM_ID` are set; falls back to CSV otherwise
- Node 5 (send_briefing) sends via Gmail API when `TED_EMAIL`, `credentials.json`, and `token.json` are present; falls back to file otherwise
- HuggingFace model downloads ~330MB on first run
- ChromaDB persists to `chroma_db/` folder locally