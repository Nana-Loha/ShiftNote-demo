# ShiftNotes

### Transforming Operational Reporting into Actionable Intelligence

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

The system runs as a 6-node LangGraph pipeline:

```text
JotForm → Gmail inbox
        ↓
Node 1 — ingest_email        (Gmail MCP / CSV fallback)
        ↓
Node 2 — classify_intent     (route: signals or RAG query)
        ↓
Node 3 — detect_signals      (hybrid regex + HuggingFace)
        ↓
Node 4 — retrieve_and_generate  (ChromaDB → OpenAI → briefing)
        ↓
Node 5 — send_briefing       (Gmail MCP / file fallback)
        ↓
Node 6 — human_review (HITL) (accept / drill_down / escalate)
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for full data flow and node responsibilities.

---

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
# Edit .env and set OPENAI_API_KEY and GROQ_API_KEY

# 4. Populate ChromaDB (required for RAG / Ask ShiftNotes tab)
uv run python prototype/rag/embed.py

# 5a. Run the agent pipeline (CLI)
uv run python run_pipeline.py

# 5b. Run the Streamlit dashboard
uv run streamlit run streamlit_app.py
```

> **Note:** `chroma_db/` is generated locally by `embed.py` and is not included in the repo. Run step 4 before using the Ask ShiftNotes or Briefings tabs.

---

## Documentation Guide

The following documents provide deeper insight into the design, implementation, and evolution of ShiftNotes.

| Document                 | Purpose                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------- |
| PRODUCT_VISION.md        | Defines the purpose, philosophy, goals, and future direction of ShiftNotes.           |
| CURRENT_FORM_ANALYSIS.md | Examines the current reporting workflow and identifies opportunities for improvement. |
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
* HITL review — working (accept / drill\_down / escalate)
* Gmail MCP — code wired for Node 1 and Node 5; requires `GMAIL_OAUTH_TOKEN` in `.env`
* GitHub Actions CI — active (pytest on push/PR to main)

### Week 9 Remaining

* Fix HITL invalid input handling — CLI path silently defaults to accept
* Wire escalate path to email shift lead (Option B)
* Tune signal classifier thresholds on real JotForm data

---

## Project Goal

The goal of ShiftNotes is not to replace existing reporting workflows.

The goal is to augment them.

By transforming operational reports into structured intelligence, ShiftNotes aims to reduce information loss, improve visibility, and help leadership make better operational decisions using information that already exists within the organization.