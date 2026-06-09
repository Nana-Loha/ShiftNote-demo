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

## 1. Peer Review Feedback & HITL Validation Evidence (Non-Team User)

Peer review conducted by: **Leah, MS in Computer Science, Boise State University**
Review date: June 7, 2026

Leah cloned the ShiftNote-demo repository, ran the pipeline end-to-end, and tested all three HITL decision paths independently as a non-team user.

**Evidence:** See attached `Peer_Review_HITL_validation_ShiftNotes.pdf`

**Feedback summary:**

| Area | Observation |
|------|-------------|
| Architecture | 6-node LangGraph pipeline is clear and logical; HITL checkpoint placement is appropriate |
| Quality | Pipeline ran without errors; logging is detailed and well-structured; CSV fallback is a good reliability feature |
| Risk 1 | Gmail MCP returns 401 authError — email delivery currently simulated via fallback |
| Risk 2 | HuggingFace classifier detected only 1/54 signals — ML component needs tuning |
| Risk 3 | HITL stage lacks invalid input validation — unexpected inputs could cause unintended behavior |
| Risk 4 | RAG retrieval accuracy not measured — recommend adding hit rate / MRR evaluation |

**HITL paths validated by Leah:**

| Decision | Result |
|----------|--------|
| Accept | ✅ Decision recorded — pipeline complete |
| Drill Down | ✅ Decision recorded — detail view pending (Week 10) |
| Escalate | ✅ Decision recorded — escalation captured |

**Response actions:**

| Feedback | Action | Timeline |
|----------|--------|----------|
| Gmail MCP 401 | Known limitation — OAuth token incompatibility with OpenAI connector; CSV fallback is production behavior | Week 10 |
| HuggingFace tuning | Investigate classifier coverage gap; tune on JotForm data | Week 10 |
| HITL invalid input | Add validation loop to re-prompt until valid decision entered | Week 10 |
| RAG evaluation | Add hit rate / MRR measurement to retrieval pipeline | Week 10 |

### Pipeline Evidence (Leah's Run)

**Leah's run — accept decision (Run ID: a9f88af9)**
![Leah accept run complete](screenshot/01_leah_accept_run_complete.jpg)

**Pipeline start — ingest & classify nodes**
![Pipeline start ingest classify](screenshot/02_pipeline_start_ingest_classify.png)

**detect_signals — regex detection (mid)**
![Detect signals regex mid](screenshot/03_detect_signals_regex_mid.png)

**detect_signals — HuggingFace + node exit (45/100 reports)**
![Detect signals huggingface exit](screenshot/04_detect_signals_huggingface_exit.png)

**send_briefing — Gmail MCP 401 authError + fallback**
![Send briefing Gmail 401 fallback](screenshot/05_send_briefing_gmail_401_fallback.png)

**send_briefing — MCP debug full log**
![Send briefing MCP debug full](screenshot/06_send_briefing_mcp_debug_full.png)

**send_briefing — node exit**
![Send briefing node exit](screenshot/07_send_briefing_node_exit.png)

**HITL — accept decision complete (Run ID: 6e5b2934)**
![HITL accept pipeline complete](screenshot/08_hitl_accept_pipeline_complete.jpg)

**HITL — escalate decision (Run ID: bb7fcbaa)**
![HITL escalate pipeline complete](screenshot/10_hitl_escalate_pipeline_complete.png)

**HITL — invalid input "no" (Run ID: 095ec71c)**
![HITL invalid input no](screenshot/09_hitl_invalid_input_no.jpg)

---

## 2. Backlog Completion Report

### Week 8 Completed Items (8/8 — 100%) ✅

All Week 8 planned items were completed:

- Finalized SPEC.md and ARCHITECTURE.md
- Transitioned from Jupyter notebook prototype to LangGraph agent pipeline
- Defined and implemented 6-node pipeline (ingest_email → classify_intent → detect_signals → retrieve_and_generate → send_briefing → human_review)
- Documented Gmail MCP integration plan
- Added RISKS.md with 10 tracked risks
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

## 3. Technical Report Draft (Sections 1–3)

### Section 1: Problem Statement and Business Context

Dsquared Hospitality operates multiple food kiosks at T-Mobile HQ under the Bowls & Buns brand. Shift leads submit daily JotForm reports covering food quality, inventory concerns, guest feedback, and employee recognition. Before ShiftNotes, these reports accumulated in the GM (Ted)'s inbox and required manual review to identify patterns.

ShiftNotes is an intelligence layer that automatically reads shift reports, detects operational signals, and delivers a plain-English briefing to Ted — so he spends less time reading and more time acting.

→ See full Section 1 in [TECHNICAL_REPORT_DRAFT.md](https://github.com/Nana-Loha/ShiftNote-demo/blob/main/TECHNICAL_REPORT_DRAFT.md)

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
4. HITL invalid input silently accepted — fix planned for Week 10 per peer review

→ See [RISKS.md](https://github.com/Nana-Loha/ShiftNote-demo/blob/main/RISKS.md)

---



## Repository Structure

```
ShiftNotes/
├── briefings/
├── chroma_db/
├── prototype/
├── screenshot/                        ← peer review & HITL evidence
├── shiftnotes_agent/
│   ├── nodes/
│   ├── graph.py
│   ├── state.py
│   └── logger.py
├── tests/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── test_signal_classifier.py
│   └── test_state.py
├── .env
├── .env.example
├── .gitignore
├── .python-version
├── ARCHITECTURE.md
├── BACKLOG.md
├── CLAUDE.md
├── credentials.json
├── CURRENT_FORM_ANALYSIS.md
├── generate_gmail_token.py
├── MOCK_DATA_DESIGN.md
├── PRODUCT_VISION.md
├── pyproject.toml
├── README.md
├── RISKS.md
├── run_pipeline.py
├── SPEC.MD
├── streamlit_app.py
├── USER_EXPERIENCE.md
├── uv.lock
├── WEEK8_REPORT.md
└── WEEK9_REPORT.md
```

---

*Submitted for AI 410 Week 9 QA Checkpoint*
*Repository: https://github.com/Nana-Loha/ShiftNote-demo*