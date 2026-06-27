# ShiftNotes

### Transforming Operational Reporting into Actionable Intelligence

🎬 **[Watch the full project walkthrough on YouTube →](YOUR_YOUTUBE_LINK_HERE)**

---

## Submission Deliverables — AI 410 Final Project

**Team:** Pitchanan Lohavanichbutr, Geetanjali Kulkarni, Careen Mollel

| Deliverable | Link |
|---|---|
| Codebase (this repo) | [github.com/Nana-Loha/ShiftNote-demo](https://github.com/Nana-Loha/ShiftNote-demo) |
| README.md | [README.md](./README.md) — setup, run steps, architecture summary |
| CLAUDE.md | [CLAUDE.md](./CLAUDE.md) — project guidance and workflow context |
| Technical Report (PDF) | [ShiftNotes_Technical_Report.pdf](./ShiftNotes_Technical_Report.pdf) |

**Technical report covers all required sections:**
- Problem statement and business justification
- Architecture decisions and framework rationale
- Model selection and benchmark evidence
- RAG / reasoning pipeline design
- Responsible AI analysis (risks and mitigations)
- Lessons learned and future work

**Final checks:**
- Reproducibility: `uv sync` + `uv run python run_pipeline.py` — see [Quick Start](#quick-start)
- Demo path: documented below under [Demo Path](#demo-path)
- Known limitations: listed below under [Known Limitations](#known-limitations)

---

## Overview

ShiftNotes is an AI-powered intake and intelligence system designed to transform operational shift reports into structured data, automated insights, and actionable operational intelligence.

The project originated from operational reporting workflows used by **Dsquared Hospitality at T-Mobile Headquarters**. Shift leads submit daily reports containing information about food quality, inventory concerns, guest feedback, staffing observations, and operational notes.

While these reports contain valuable information, much of that knowledge becomes archived in emails and folders, making historical analysis, trend detection, and operational insight extraction largely manual processes.

ShiftNotes acts as an intelligence layer on top of the existing reporting workflow. Instead of simply storing reports, the system organizes information, identifies recurring patterns, generates operational summaries, and surfaces insights that help leadership make more informed operational decisions.

Although the initial prototype focuses on hospitality operations within the T-Mobile Headquarters environment, the underlying concepts can be applied to any organization that relies on recurring operational reporting.

---

## Current Scope

| Category      | Details                                          |
| ------------- | ------------------------------------------------ |
| Environment   | Dsquared Hospitality at T-Mobile Headquarters    |
| Data Source   | Shift Lead Reports & Operational Notes           |
| Primary Goal  | Operational Insight Generation & Trend Detection |
| Current Stage | Prototype / Proof of Concept                     |

---

## The Problem

Current operational reporting workflows are effective at collecting information but are not optimized for extracting intelligence.

### Current Workflow

```text
Shift Lead
    ↓
JotForm Submission
    ↓
Email Inbox
    ↓
Folder Organization
    ↓
Manual Review
    ↓
Operational Action
```

While this process successfully captures information, it relies heavily on manual review, individual memory, and historical searching.

As reports accumulate over time, recurring patterns and operational trends become increasingly difficult to identify.

Examples include:

* Recurring food outages
* Staffing trends
* Guest feedback patterns
* Repeated operational issues
* Employee recognition trends
* Inventory concerns
* Escalation frequency

Many of these insights already exist within the reports but require significant manual effort to uncover.

---

## The Solution

ShiftNotes introduces an intelligence layer on top of existing reporting workflows.

### Proposed Workflow

```text
Operational Reports
        ↓
Processing Layer
        ↓
Structured Intelligence
        ↓
Trend Detection
        ↓
Operational Insights
        ↓
Leadership Reporting
```

Instead of simply storing operational reports, ShiftNotes transforms them into searchable and analyzable organizational knowledge.

The system is designed to:

* Extract meaningful operational signals
* Organize unstructured reporting data
* Detect recurring trends
* Generate automated summaries
* Surface actionable insights
* Reduce manual review effort

---

## Core Objectives

* Preserve existing reporting workflows
* Reduce information loss
* Improve operational visibility
* Support leadership decision-making
* Identify recurring operational trends
* Transform operational notes into organizational intelligence

---

## Architecture

JotForm submissions
        ↓
Node 1 — ingest_email        (JotForm MCP via OpenAI connector / CSV fallback)
        ↓
Node 2 — classify_intent     (route: signals or RAG query)
        ↓
Node 3 — detect_signals      (hybrid regex + zero-shot classifier)
        ↓
Node 4 — retrieve_and_generate  (ChromaDB → OpenAI → briefing)
        ↓
Node 5 — send_briefing       (Gmail API / file fallback)
        ↓
Node 6 — human_review (HITL) (accept / drill_down / escalate)
```

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Nana-Loha/ShiftNote-demo.git
cd ShiftNote-demo

# 2. Install dependencies (requires uv)
pip install uv
uv sync

# 3. Configure environment
cp .env.example .env
# Edit .env and set: OPENAI_API_KEY, GROQ_API_KEY, TED_EMAIL

# 4. Populate ChromaDB (required for RAG / Ask ShiftNotes tab)
uv run python prototype/rag/embed.py

# 5. Set up Gmail sending (one time) — see TEAMMATE_SETUP_GUIDE.md
#    Requires credentials.json in the project root, then:
uv run python generate_gmail_token.py

# 6a. Run the agent pipeline (CLI)
uv run python run_pipeline.py
#    When prompted, enter: accept | drill_down | escalate

# 6b. Run the Streamlit dashboard
uv run streamlit run streamlit_app.py
```

> **Note:** `chroma_db/` is generated locally by `embed.py` and is not included in the repo. Run step 4 before using the Ask ShiftNotes or Briefings tabs.

> **Gmail sending:** If `TED_EMAIL`, `credentials.json`, or `token.json` is not set up, the briefing is saved to the `briefings/` folder instead of emailed. This is expected fallback behavior. See `TEAMMATE_SETUP_GUIDE.md` for full setup.

---

## Documentation Guide

The following documents provide deeper insight into the design, implementation, and evolution of ShiftNotes.

| Document                 | Purpose                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------- |
| PRODUCT_VISION.md        | Defines the purpose, philosophy, goals, and future direction of ShiftNotes.           |
| CURRENT_FORM_ANALYSIS.md | Examines the current reporting workflow and identifies opportunity for improvement. |
| USER_EXPERIENCE.md       | Defines how users interact with the system and consume insights.                      |
| ARCHITECTURE.md          | Documents system components, data flow, and technical design decisions.               |
| SPEC.MD                  | Full product specification including pipeline design and MCP integration plan.        |
| RISKS.md                 | Known risks with likelihood, impact, and mitigation actions.                          |
| BACKLOG.md               | Completed and planned work by week.                                                   |

---

## Status

### Current Phase

* LangGraph agent pipeline — operational
* Streamlit dashboard — integrated with agent pipeline
* ChromaDB RAG — active
* HITL review — working (accept / drill_down / escalate), with input validation
* JotForm MCP — Node 1 wired via OpenAI MCP connector; uses CSV fallback until live form is provisioned
* Gmail API — Node 5 sends real briefing emails; file fallback when unconfigured
* GitHub Actions CI — active (pytest on push/PR to main)

## Known Limitations

* The live JotForm form is not yet provisioned; the pipeline runs on a synthetic dataset of 100 reports. Activating live ingestion requires setting `JOTFORM_OAUTH_TOKEN` and `JOTFORM_FORM_ID`.
* Gmail sending runs in OAuth testing mode, limited to approved test users. Production use would require app verification or a service account.
* The Streamlit drill-down interface (HITL "drill_down" option) is partially implemented.
* Signal detection thresholds are tuned on synthetic data and would need calibration on real submissions.

See [RISKS.md](./RISKS.md) for the full risk register.

## Demo Path

A complete end-to-end run for demonstration:

1. `uv run python run_pipeline.py`
2. Pipeline ingests 100 reports, detects signals in ~45, generates a briefing
3. Briefing is emailed to `TED_EMAIL` via the Gmail API
4. Pipeline pauses at the HITL checkpoint
5. Enter an invalid value to show input rejection, then enter `accept` to complete

## Demo Video

[![ShiftNotes Demo](https://img.youtube.com/vi/zINqPPPskt4/maxresdefault.jpg)](https://youtu.be/zINqPPPskt4)

A full walkthrough of the ShiftNotes pipeline: end-to-end run, the human-in-the-loop checkpoint, failure recovery, and the drill-down dashboard.

---

## Project Goal

The goal of ShiftNotes is not to replace existing reporting workflows.

The goal is to augment them.

By transforming operational reports into structured intelligence, ShiftNotes aims to reduce information loss, improve visibility, and help leadership make better operational decisions using information that already exists within the organization.
