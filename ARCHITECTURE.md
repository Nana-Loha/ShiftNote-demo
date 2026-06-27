# ARCHITECTURE

## Purpose

This document describes the current ShiftNotes architecture after the Week 8 transition from a notebook prototype to a LangGraph agent pipeline.

ShiftNotes is now explicitly designed as a six-node LangGraph workflow with a human-in-the-loop checkpoint, JotForm MCP ingestion, and Gmail API delivery.

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
JotForm submission
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

**Role:** Ingests JotForm shift report submissions.

- **Current implementation:** Reads from JotForm MCP when `JOTFORM_OAUTH_TOKEN` and `JOTFORM_FORM_ID` are set; falls back to `mock_shift_notes.csv` otherwise
- **Output:** Structured report records added to pipeline state

### MCP integration point

- JotForm MCP read is wired via `_read_from_jotform_mcp()` using the official JotForm MCP server (`https://mcp.jotform.com`) via the OpenAI Responses API connector
- Activate by setting `JOTFORM_OAUTH_TOKEN` and `JOTFORM_FORM_ID` in `.env`
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

- **Current implementation:** Sends via Gmail API (`google-api-python-client`) when `TED_EMAIL`, `credentials.json`, and `token.json` are present; falls back to `briefings/` file output otherwise
- **Gmail setup:** run `generate_gmail_token.py` once to create `token.json`; see `GMAIL_SETUP.md` for full instructions

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
| Email delivery | Gmail API (`google-api-python-client`) |
| Report ingestion | JotForm MCP via OpenAI Responses API connector |
| Drill-down UI | Streamlit (dashboard active; drill-down detail view pending) |

---

# Integration Points

| Node | Current behavior | To activate |
|------|------------------|------------|
| Node 1 — ingest_email | JotForm MCP read via OpenAI connector; CSV fallback when tokens absent | Set `JOTFORM_OAUTH_TOKEN` + `JOTFORM_FORM_ID` in `.env` |
| Node 5 — send_briefing | Gmail API send; file fallback when credentials absent | Set `TED_EMAIL` in `.env`; place `credentials.json` + `token.json` in project root |

Both integration points are isolated — the LangGraph pipeline is unchanged regardless of which path runs.

---

# Current Limitations

- Live JotForm form not yet provisioned — pipeline runs on synthetic CSV until `JOTFORM_OAUTH_TOKEN` and `JOTFORM_FORM_ID` are set.
- Gmail sending runs in OAuth testing mode — limited to approved test users; production requires app verification or a service account.
- ChromaDB is empty until `prototype/rag/embed.py` is run — RAG retrieval returns no context until indexed.
- The HuggingFace model download is large (~330MB) on first run and requires stable internet.
- Signal detection thresholds are tuned for synthetic data and may need adjustment for real JotForm reports.
- Streamlit drill-down detail view (HITL "drill_down" option) is not yet implemented; button is wired but no detail view exists.
- Escalate path logs the decision but does not email the shift lead.

---

# Notes

The original notebook prototype remains available under `prototype/` for reference, but the active architecture now centers on the LangGraph agent pipeline.
