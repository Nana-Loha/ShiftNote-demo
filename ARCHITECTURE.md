# ARCHITECTURE

## Purpose

This document describes the current ShiftNotes architecture after the Week 8 transition from a notebook prototype to a LangGraph agent pipeline.

ShiftNotes is now explicitly designed as a six-node LangGraph workflow with a human-in-the-loop checkpoint and Gmail MCP integration points.

---

# System Overview

ShiftNotes is implemented as a LangGraph agent pipeline that ingests shift report email content, detects operational signals, optionally performs retrieval-augmented generation, delivers briefings, and then pauses for Ted's review.

The architecture is intentionally modular, with clear separation between:

- data ingestion
- intent routing
- signal detection
- retrieval and generation
- delivery
- human review

---

# High-Level Data Flow

```text
Shift lead writes report
    ↓
JotForm → Gmail inbox
    ↓
Node 1 — ingest_email
    ↓
Node 2 — classify_intent
    ↓
Node 3 — detect_signals
    ↓
Node 4 — retrieve_and_generate (RAG)
    ↓
Node 5 — send_briefing
    ↓
Node 6 — human_review (HITL)
    ↓
Ted either accepts, drills down, or escalates
```

---

# The 6-Node Pipeline

## Node 1 — ingest_email

**Role:** Ingests incoming JotForm report emails.

- **Current implementation:** Reads from Gmail MCP when `GMAIL_OAUTH_TOKEN` is set; falls back to `mock_shift_notes.csv` otherwise
- **Output:** Structured report records added to pipeline state

### MCP integration point

- Gmail MCP read is wired via `_read_from_gmail_mcp()` — activate by setting `GMAIL_OAUTH_TOKEN` in `.env`
- This node is the primary live-input gateway for the agent

---

## Node 2 — classify_intent

**Role:** Determines whether the pipeline is handling a report signal batch or a conversational RAG query.

- **Input:** ingested report data or incoming user query
- **Output:** intent label `signals` or `rag_query`
- **Routing:** `signals` → Node 3, `rag_query` → Node 4

---

## Node 3 — detect_signals

**Role:** Detects operational signals from shift report text.

- **Detection approach:** hybrid regex fast-path plus HuggingFace zero-shot fallback
- **Signals:**
  - `chicken_shortage`
  - `poke_request`
  - `ops_issue`
  - `team_recognition`

### Implementation details

- Regex stage captures deterministic cases and short-circuits the model call
- HuggingFace stage uses `cross-encoder/nli-MiniLM2-L6-H768`
- Per-signal thresholds ensure conservative classification

### Thresholds

| Signal | Threshold |
|--------|-----------|
| `chicken_shortage` | 0.70 |
| `poke_request` | 0.50 |
| `ops_issue` | 0.70 |
| `team_recognition` | 0.95 |

---

## Node 4 — retrieve_and_generate (RAG)

**Role:** Retrieves relevant historical context and generates plain-English briefing content.

- **Retrieval:** ChromaDB vector search over indexed reports
- **Generation:** OpenAI prompt-based briefing construction

### Important note

ChromaDB is empty until reports are indexed. When empty, RAG context is unavailable and the system falls back to current briefing generation behavior.

---

## Node 5 — send_briefing

**Role:** Delivers generated briefings to Ted.

- **Current implementation:** Sends via Gmail MCP when `GMAIL_OAUTH_TOKEN` is set; falls back to `briefings/` file output otherwise
- **Gmail MCP URL:** `https://gmailmcp.googleapis.com/mcp/v1`
- **MCP integration point:** `_send_via_gmail_mcp()` — activate by setting `GMAIL_OAUTH_TOKEN` and `TED_EMAIL` in `.env`

---

## Node 6 — human_review (HITL)

**Role:** Provides the human-in-the-loop checkpoint after briefing delivery.

- **Input:** delivered briefing
- **Output:** Ted's decision logged for downstream action

### Decision paths

| Decision | Result |
|----------|--------|
| `accept` | Ted understands and takes action |
| `drill_down` | Ted reviews details in Streamlit (button wired; dedicated detail view pending) |
| `escalate` | Ted requests source verification; escalation note logged (email to shift lead pending) |

This design preserves the product principle that intelligence should be delivered passively and then reviewed, rather than requiring Ted to request it first.

---

# Project Structure

```
ShiftNotes/
├── prototype/                  ← original notebook prototype
├── shiftnotes_agent/           ← LangGraph agent pipeline
│   ├── nodes/
│   │   ├── ingest_email.py
│   │   ├── classify_intent.py
│   │   ├── detect_signals.py
│   │   ├── retrieve_and_generate.py
│   │   ├── send_briefing.py
│   │   └── human_review.py
│   ├── tools/
│   │   └── signal_classifier.py
│   ├── graph.py
│   ├── state.py
│   └── logger.py
├── briefings/                  ← generated briefing files
├── run_pipeline.py            ← pipeline entrypoint
├── streamlit_app.py           ← Streamlit dashboard (Briefings + Ask ShiftNotes tabs)
├── RISKS.md                   ← known risks list
├── SPEC.MD                    ← current specification
├── README.md
├── PRODUCT_VISION.md
└── pyproject.toml
```

---

# Technology Stack

| Aspect | Technology |
|--------|------------|
| Orchestration | LangGraph |
| HITL | LangGraph interrupt |
| Signal detection | Regex + HuggingFace Transformers |
| Zero-shot model | cross-encoder/nli-MiniLM2-L6-H768 |
| Retrieval | ChromaDB |
| Briefing generation | OpenAI |
| Email integration | Gmail MCP (wired — requires `GMAIL_OAUTH_TOKEN`) |
| Drill-down UI | Streamlit (dashboard active; drill-down detail view pending) |

---

# MCP Integration Points

| Node | Current behavior | To activate |
|------|------------------|------------|
| Node 1 — ingest_email | Gmail MCP read; CSV fallback when token absent | Set `GMAIL_OAUTH_TOKEN` in `.env` |
| Node 5 — send_briefing | Gmail MCP send; file fallback when token absent | Set `GMAIL_OAUTH_TOKEN` + `TED_EMAIL` in `.env` |

Both integration points are isolated — the LangGraph pipeline is unchanged regardless of which path runs.

---

# Current Limitations

- Gmail MCP requires `GMAIL_OAUTH_TOKEN` to be set; pipeline falls back to CSV/file when the token is absent.
- ChromaDB is empty until `prototype/rag/embed.py` is run — RAG retrieval returns no context until indexed.
- The HuggingFace model download is large (~330MB) on first run and requires stable internet.
- Signal detection thresholds are tuned for synthetic data and may need adjustment for real JotForm reports.
- HITL invalid input silently defaults to `accept` in the CLI path.
- Streamlit drill-down detail view (Option A) is not yet implemented; button is wired but no detail view exists.
- Escalate path logs the decision but does not email the shift lead (Option B pending).

---

# Week 9 Remaining

- Fix HITL invalid input handling — add validation and retry prompt in CLI path.
- Wire escalate path to email shift lead via Gmail MCP (Option B).
- Tune signal classifier thresholds on real JotForm sample data.

---

# Notes

The original notebook prototype remains available under `prototype/` for reference, but the active architecture now centers on the LangGraph agent pipeline.
