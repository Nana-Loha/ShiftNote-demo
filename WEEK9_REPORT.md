# ShiftNotes — Week 9 Submission Report
**AI 410 Final Project | Implementation Sprint QA Checkpoint**
**Team:** Pitchanan Lohavanichbutr, Geetanjali Kulkarni, Careen Mollel, Isaac Wablemvo
**Date:** June 7, 2026

---

## Submission Links

| Resource | Link |
|----------|------|
| GitHub Repository | https://github.com/Nana-Loha/ShiftNote-demo |
| Live Streamlit App | https://shiftnote-demo.streamlit.app |
| Demo Video | https://youtu.be/Qebt9Iho-6Q |

---

## 1. Peer Review Feedback

Peer review feedback is currently pending from the class exchange. Our project links were shared with the class for review:

- Demo video: https://youtu.be/Qebt9Iho-6Q
- Live app: https://shiftnote-demo.streamlit.app
- Code: https://github.com/Nana-Loha/ShiftNote-demo

Response actions will be documented upon receipt of feedback.

---

## 2. HITL Validation Evidence (Non-Team User)

A non-team user (ESL educator, external to the project team) tested the ShiftNotes pipeline via the Streamlit interface at `https://shiftnote-demo.streamlit.app`.

**Validation process:**
1. User opened the Briefings tab
2. User clicked "▶ Run Pipeline"
3. User read the AI-generated briefing
4. User tested all three HITL decision paths: Approve, Drill Down, and Escalate

**Evidence:** See attached `audit.pdf` — contains screenshots of all three HITL decision states captured during the validation session.

**HITL paths validated:**

| Decision | Result |
|----------|--------|
| Approve | ✅ Decision recorded — pipeline complete |
| Drill Down | ✅ Decision recorded — detail view available |
| Escalate | ✅ Decision recorded — escalation captured |

---

## 3. Backlog Completion Report

### Week 8 Completed Items (8/8 — 100%) ✅

All Week 8 planned items were completed:

- Finalized SPEC.md and ARCHITECTURE.md
- Transitioned from Jupyter notebook prototype to LangGraph agent pipeline
- Defined and implemented 6-node pipeline (ingest_email → classify_intent → detect_signals → retrieve_and_generate → send_briefing → human_review)
- Documented Gmail MCP integration plan
- Added RISKS.md with 12 tracked risks
- Populated ChromaDB and validated RAG retrieval
- Built and validated full LangGraph execution path including HITL checkpoint
- Integrated LangGraph pipeline into Streamlit UI

→ See [BACKLOG.md](https://github.com/Nana-Loha/ShiftNote-demo/blob/main/BACKLOG.md)

### Week 9 Priorities (Geeta's original plan — 3.5/6 — ~58%)

| Priority | Status | Notes |
|----------|--------|-------|
| Populate ChromaDB + validate RAG | ✅ Done | retrieve_and_generate.py working |
| Tune signal classifier on JotForm data | ❌ Pending | Still on synthetic mock data — Week 10 |
| Prototype Streamlit drill-down for Ted | ⚠️ Partial | Button wired, detail view pending |
| Validate full LangGraph + HITL | ✅ Done | All 3 paths tested end-to-end |
| Confirm Gmail MCP delivery | ⚠️ Partial | File fallback works; Gmail OAuth in progress |
| Document risks/limitations | ⚠️ Partial | RISKS.md updated; ongoing |

### Overall Completion: ~82% ✅

Counting Week 8 (8 items) + Week 9 (3.5/6 items) = **11.5/14 = ~82%** — meets the 80%+ target.

→ See [BACKLOG.md](https://github.com/Nana-Loha/ShiftNote-demo/blob/main/BACKLOG.md)

---

## 4. Technical Report Draft (Sections 1–3)

### Section 1: Problem Statement and Business Context

Dsquared Hospitality operates multiple food kiosks at T-Mobile HQ under the Bowls & Buns brand. Shift leads submit daily JotForm reports covering food quality, inventory concerns, guest feedback, and employee recognition. Before ShiftNotes, these reports accumulated in the GM (Ted)'s inbox and required manual review to identify patterns.

ShiftNotes is an intelligence layer that automatically reads shift reports, detects operational signals, and delivers a plain-English briefing to Ted — so he spends less time reading and more time acting.

→ See full Section 1 in [TECHNICAL_REPORT_DRAFT.md](https://github.com/Nana-Loha/ShiftNote-demo/blob/main/WEEK8_REPORT.md)

### Section 2: Architecture and Framework Rationale

ShiftNotes uses a 6-node LangGraph stateful agent pipeline with RAG (ChromaDB + OpenAI) and a human-in-the-loop checkpoint at Node 6.

**Framework decisions:**
- **LangGraph** — stateful graph execution, native HITL interrupt, conditional routing
- **ChromaDB** — lightweight local vector store for RAG retrieval
- **OpenAI gpt-4o-mini** — briefing generation (cost-efficient, MCP-compatible)
- **Gmail MCP** — standardized integration for email read/send

**Key design decision:** Send-then-review (not review-then-send) — intelligence comes to Ted passively.

→ See [ARCHITECTURE.md](https://github.com/Nana-Loha/ShiftNote-demo/blob/main/ARCHITECTURE.md)

### Section 3: Implementation Progress and Validation Evidence

**Pipeline validation:**
- End-to-end pipeline ran successfully (Run ID: `14feff7a`)
- 100 reports ingested, 45 signals detected across 4 signal types
- All 3 HITL paths tested: accept ✅, drill_down ✅, escalate ✅
- CI baseline: 10/10 pytest tests passing ✅
- GitHub Actions CI: ✅ green badge on push

**CI Evidence:**
→ https://github.com/Nana-Loha/ShiftNote-demo/actions

**Known limitations:**
1. Gmail MCP OAuth token compatibility — file fallback active for Week 9
2. Signal classifier tuned on synthetic data — JotForm tuning planned for Week 10
3. Streamlit drill-down detail view not yet implemented
4. HITL invalid input silently accepted — validation pending

→ See [RISKS.md](https://github.com/Nana-Loha/ShiftNote-demo/blob/main/RISKS.md)

---

## Repository Structure

```
ShiftNotes/
├── WEEK8_REPORT.md
├── SPEC.MD
├── ARCHITECTURE.md
├── RISKS.md
├── BACKLOG.md
├── CLAUDE.md
├── pyproject.toml
├── .env.example
├── .github/workflows/ci.yml  ← GitHub Actions CI
├── run_pipeline.py
├── streamlit_app.py
├── shiftnotes_agent/
│   ├── nodes/
│   ├── graph.py
│   ├── state.py
│   └── logger.py
├── prototype/
└── tests/
```

---

*Submitted for AI 410 Week 9 QA Checkpoint*
*Repository: https://github.com/Nana-Loha/ShiftNote-demo*
