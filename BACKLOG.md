# BACKLOG

## Week 7 — Completed Items

- Created initial project documentation: `PRODUCT_VISION.md`, `CURRENT_FORM_ANALYSIS.md`, `USER_EXPERIENCE.md`, `MOCK_DATA_DESIGN.md`, and `README.md` — established the business context, problem statement, user roles (Ted as GM, shift leads), and design philosophy.
- Designed and generated synthetic mock dataset: `prototype/mock_shift_notes.csv` — 100 shift reports across 6 kiosks (A–F) with realistic field coverage including food quality ratings, inventory concerns, guest feedback, and staffing notes.
- Built Jupyter notebook prototype `prototype/ShiftNotes_Prototype.ipynb` — end-to-end signal detection pipeline with kiosk summary aggregation, weekly trend analysis, and ground truth validation.
- Implemented hybrid signal classifier `prototype/signal_classifier.py` — regex layer for deterministic signals (chicken shortage, poke request, ops issues, team recognition) with HuggingFace zero-shot fallback (`cross-encoder/nli-MiniLM2-L6-H768`) and per-signal confidence thresholds to prevent overfiring. All 7/7 ground truth checks passing.
- Built RAG prototype: `prototype/embed.py` (ChromaDB ingestion) and `prototype/retriever.py` (semantic retrieval) — embedded all 100 mock reports into ChromaDB for the Ask ShiftNotes tab.
- Built Streamlit RAG app `prototype/app.py` — interactive Ask ShiftNotes interface with structured logging, HITL approval gate placeholder, and MCP tool layer stub. Validated RAG retrieval returning 5 source reports per query with contextual answers via Groq.
- Created `ARCHITECTURE.md` — documented the 6-node LangGraph pipeline architecture with data flow, node responsibilities, MCP integration points, and HITL design before implementation began.
- Drafted initial `SPEC.MD` — product specification covering problem statement, user needs, signal definitions, pipeline design, and MCP integration plan.
- Created team task backlog in `BACKLOG.md` and refactored `rag/` folder into `prototype/` for cleaner project structure.

---

## Week 8 — Completed Items

- Completed the Week 8 checkpoint deliverable by updating the specification and architecture documentation.
- Transitioned the active design from the original Jupyter notebook prototype to a LangGraph agent pipeline.
- Defined the six-node pipeline: `ingest_email`, `classify_intent`, `detect_signals`,
  `retrieve_and_generate`, `send_briefing`, `human_review`.
- Documented the Gmail MCP integration plan and identified the two MCP swap points: Node 1 ingestion and Node 5 briefing delivery.
- Added a known risks document with Week 9 risk tracking.
- Preserved the notebook-based prototype in `prototype/` while making the agent pipeline the primary architecture.
- Created and updated `SPEC.MD` and `ARCHITECTURE.md` to reflect the current LangGraph design, HITL checkpoint, RAG pipeline, and MCP integration.
- Added a RAG backlog and roadmap in `prototype/ROADMAP.md` for future retrieval-augmented generation work.
- Populated ChromaDB and validated RAG retrieval in `retrieve_and_generate.py`.
- Built and validated full LangGraph execution path including HITL checkpoint — accept, drill_down, and escalate paths tested end-to-end.
- Integrated LangGraph pipeline into `streamlit_app.py` Briefings tab with 4-state UI (idle → awaiting_review → complete → error).
- Added `st.secrets` support with sidebar text-input fallback for both `OPENAI_API_KEY` and `GROQ_API_KEY`; guarded with try/except so app runs locally without `secrets.toml`.
- Added pre-flight `OPENAI_API_KEY` check to `run_pipeline.py` — exits early with clear error if key is missing or still placeholder.
- Added `GROQ_API_KEY` to `.env.example` and `CLAUDE.md`.
- Gitignored generated `briefings/*.txt` files.

## Week 9 — Completed and In-Progress Items (Geeta's original plan)

- Populate ChromaDB and validate RAG retrieval — ✅ Done. `retrieve_and_generate.py` working end-to-end.
- Validate full LangGraph execution path including HITL checkpoint — ✅ Done. All 3 paths (accept, drill_down, escalate) tested end-to-end.
- Confirm Gmail MCP email delivery — ⚠️ Partial. Gmail OAuth token returned 401 due to OpenAI connector incompatibility. Resolved in Week 10 with direct Gmail API.
- Prototype Streamlit drill-down detail view for Ted — ⚠️ Partial. Drill Down button wired in Briefings tab; detail view not implemented (known limitation).
- Document risks and limitations in RISKS.md — ✅ Done. RISKS.md has 10 tracked risks with likelihood, impact, and mitigations.
- Tune hybrid signal classifier thresholds on real JotForm sample data — ❌ Not completed. Still using synthetic mock data (known limitation).

## Week 9 — Additional Technical Items

- Set up GitHub Actions CI workflow (`.github/workflows/ci.yml`) — ✅ Done. CI runs `uv run pytest tests/ -v` on push and PR to main.
- Fix HITL invalid input handling — ✅ Done in Week 10. Validation loop added to `run_pipeline.py` and `human_review.py`; invalid input re-prompts instead of silently defaulting to `accept`.
- Wire escalate path to email shift lead — ❌ Not completed. Escalation note is captured in state but no secondary email is sent (known limitation).

## Week 9 QA Checkpoint Artifacts

- Peer review feedback received from Leah (MS CS, Boise State) — ✅ Done. Response actions documented in WEEK9_REPORT.md.
- HITL validation evidence with a non-team user — ✅ Done. All 3 paths validated; screenshots in `screenshot/`.
- Backlog completion report — ✅ Done. ~82% completion (11.5/14 items).
- Technical report draft (Sections 1–3) — ✅ Done. Expanded to full report in Week 10.

---

## Week 10 — Completed Items

- Fixed HITL invalid input — re-prompt loop added to `run_pipeline.py`; `human_review.py` now returns error state instead of silently defaulting to `accept`.
- Replaced Gmail MCP (broken 401) with direct Gmail API in Node 5 — real briefing emails now delivered via `google-api-python-client`.
- Switched Node 1 ingestion from Gmail MCP to JotForm MCP via OpenAI Responses API connector with CSV fallback.
- Completed full 10-page technical report — all 6 required sections; published as `ShiftNotes_Technical_Report.pdf`.
- Updated README with submission deliverables section, demo path, known limitations, and YouTube demo placeholder.
- Fixed `streamlit_app.py` to call `load_dotenv()` and added `get_config_value()` helper for `.env` + `st.secrets` fallback.
- Gitignored entire `briefings/` folder; updated `generate_gmail_token.py` with better error handling and narrowed OAuth scope.
- 10/10 pytest tests passing; GitHub Actions CI green on main.

## Week 10 — Final Delivery Requirements

### Required Deliverables

- Codebase: documented, test-covered, reproducible environment ✅
- README.md: setup, run steps, architecture summary ✅
- CLAUDE.md: project guidance and workflow context ✅
- 10-page technical report (`ShiftNotes_Technical_Report.pdf`) ✅
  - Problem statement and business justification
  - Architecture decisions and framework rationale
  - Model selection and benchmark evidence
  - RAG or reasoning pipeline design
  - Responsible AI analysis (risks and mitigations)
  - Lessons learned and future work

### Final Presentation and Demo Guide

- 15-minute live demo and presentation
- 5-minute Q&A
- All team members must participate

### Required Demo Elements

- End-to-end system run with realistic input
- One HITL checkpoint in action (show invalid input rejection, then valid decision)
- One failure mode and recovery demonstration (Gmail fallback to file)
- Brief walkthrough of architecture and key design choices

---

## Week 11 — Final Presentation and Submission

### Submission Status

- Final codebase submitted ✅ — Jun 26, 2026 6:09pm
- GitHub repo: https://github.com/Nana-Loha/ShiftNote-demo
- Technical report PDF: `ShiftNotes_Technical_Report.pdf` (11 pages, all 6 sections)

### Final Requirements Cross-Check

| Requirement | Status | Evidence |
|---|---|---|
| Codebase: documented | ✅ | ARCHITECTURE.md, SPEC.MD, RISKS.md, BACKLOG.md, CLAUDE.md |
| Codebase: test-covered | ✅ | 10/10 pytest tests passing; CI green on push to main |
| Codebase: reproducible environment | ✅ | `uv.lock` + `pyproject.toml` pin all dependencies |
| README.md: setup and run steps | ✅ | Quick Start section with 6 steps |
| README.md: architecture summary | ✅ | 6-node pipeline diagram in README |
| CLAUDE.md: project guidance | ✅ | Setup, structure, env vars, run instructions |
| Technical report: problem statement | ✅ | Section 1 — Business Context (Dsquared Hospitality) |
| Technical report: architecture decisions | ✅ | Section 2 — LangGraph, ChromaDB, MCP rationale |
| Technical report: model selection & benchmarks | ✅ | Section 2 — model table + confidence thresholds |
| Technical report: RAG pipeline design | ✅ | Section 2 + 3 — ChromaDB → OpenAI → briefing |
| Technical report: responsible AI | ✅ | RISKS.md + technical report section on risks |
| Technical report: lessons learned | ✅ | Final section of technical report |
| Demo path documented | ✅ | README "Demo Path" section |
| Known limitations listed | ✅ | README "Known Limitations" section |

### Presentation Demo Script (15 minutes)

> Legend: [SLIDE] = presentation slide · [LIVE] = VS Code / terminal · (Speaker N) = suggested presenter

---

#### PART 1 — Opening Slides (3 min)

**Slide 1 — Title (15 sec) — (Speaker 1)**
Introduce the team and preview: problem, architecture, live run, failure handling.

**Slide 2 — The Problem (45 sec) — (Speaker 1)**
- Shift leads submit JotForm reports covering food quality, inventory, guest feedback, staff recognition
- Reports pile up — manager reads every one by hand to spot patterns
- Cross-location trends (e.g. chicken shortage across kiosks) get missed
- Guiding principle: *the intelligence comes to the manager, not the other way around*

**Slide 3 — Architecture (75 sec) — (Speaker 1)**
Show the 6-node pipeline diagram.
- Node 1: JotForm MCP ingestion (CSV fallback)
- Node 2: intent classification
- Node 3: hybrid signal detection (regex first, zero-shot fallback)
- Node 4: ChromaDB retrieval → OpenAI → briefing
- Node 5: Gmail API delivery
- Node 6: HITL checkpoint (accept / drill_down / escalate)

**Slide 4 — Model and Tool Choices (45 sec) — (Speaker 2)**
- `gpt-4o-mini` at low temperature for factual summarization
- Zero-shot classifier — no labeled training data required
- Compact sentence-embedding model with ChromaDB for retrieval
- Responsible AI: human in control of every decision; logs record regex vs. model per signal; briefing grounded in retrieved history; secrets out of version control

---

#### PART 2 — Live Demo in VS Code (8 min)

**Transition — (Speaker 2):** "Rather than tell you it works, let's run it."

**Step 1 — Project structure (45 sec) — (Speaker 2)**
[LIVE] Expand `shiftnotes_agent/nodes/` in VS Code.
- Each node is its own file; `graph.py` wires them; `state.py` holds shared state; `logger.py` handles structured logging

**Step 2 — Run the pipeline (90 sec) — (Speaker 2)**
[LIVE]
```bash
uv run python run_pipeline.py
```
Narrate the structured logs as nodes execute:
- Node 1: loads 100 reports from synthetic CSV (JotForm MCP fallback — token not set)
- Node 2: sets intent
- Node 3: signals detected — ~45/100 reports flagged; each logged with regex or zero-shot source
- Node 4: retrieves context, generates briefing
- Node 5: sends via Gmail API

**Step 3 — Show the real briefing email (90 sec) — (Speaker 3)**
[LIVE] Switch to Gmail inbox in browser.
- Real email: subject `ShiftNotes Weekly Briefing — Run <id>`
- Body: plain-English summary (18 poke requests, 16 team recognitions, 15 chicken shortage flags, kiosks with most flags)
- "This is what the manager opens instead of reading 100 reports."

**Step 4 — HITL checkpoint + failure/recovery (3 min) — (Speaker 3)**
[LIVE] Terminal is paused at the human review prompt.

"The pipeline has paused. The briefing is already delivered — review happens after delivery on purpose, so the manager doesn't have to approve a draft just to read it."

Type an invalid input first:
```
nah uh
```
"The system rejects it and re-prompts. In the original version any unrecognized input was silently treated as acceptance — a typo would be recorded as approval with no indication. We identified that as an unsafe failure mode and fixed it. That's the failure and recovery: a hidden failure turned into a visible, correctable one."

Then enter a valid decision:
```
accept
```
"The graph resumes from exactly where it paused, records the decision, and completes."

**Step 5 — Second failure path (30 sec) — (Speaker 3)** *(mention only if time allows)*
"If Gmail credentials or `TED_EMAIL` aren't configured, Node 5 falls back to saving the briefing as a file instead of crashing. Every external integration has a controlled fallback — the pipeline always completes."

---

#### PART 3 — Closing Slides (3 min)

**Slide 5 — Failure Modes and Observability (45 sec) — (Speaker 1)**
- Shared `error` field in pipeline state — any node that fails writes into it; downstream nodes stop gracefully
- Real example: empty cells read as numbers broke signal detection; logging caught it; diagnosed from logs; fixed and regression test added

**Slide 6 — Testing and CI (30 sec) — (Speaker 2)**
- 10/10 pytest tests covering signal classifier and state definition
- GitHub Actions runs tests on every push to main

**Slide 7 — Team Process and Lessons Learned (45 sec) — (Speaker 2)**
- Committed directly to main → merge conflicts on shared files
- Lesson: work on branches, pull before working, merge via reviewed PRs, divide file ownership

**Slide 8 — Known Limitations and Next Steps (45 sec) — (Speaker 3)**
- Live JotForm form not yet provisioned — activating it is a config change, not a code change
- Gmail OAuth in testing mode — production needs app verification or service account
- Drill-down interface partially built
- Next steps: live form, production auth, finish drill-down, tune thresholds on real submissions

**Slide 9 — Close (15 sec) — (Speaker 1)**
"ShiftNotes ingests reports, detects signals, delivers a briefing by email, and keeps a human in control — all orchestrated by LangGraph and observable end to end. Thank you."

---

#### Pre-Recording Checklist

1. `git pull origin main` — ensure latest code
2. `uv sync` — confirm dependencies installed
3. Confirm `.env` has `OPENAI_API_KEY` and `TED_EMAIL` set
4. Confirm `credentials.json` and `token.json` in project root (Gmail sending works)
5. Run the pipeline once in advance to warm up model download and confirm email lands; delete that test email so inbox is clean
6. Have Gmail inbox open in a browser tab, signed in, ready to switch to
7. Increase terminal font size so logs are readable on video
8. Record a backup run in advance — if the live run fails (network, API hiccup), fall back to the backup

#### Timing Summary

| Segment | Time |
|---|---|
| Part 1 — Opening slides | 3:00 |
| Part 2 — Live demo | 8:00 |
| Part 3 — Closing slides | 3:00 |
| Buffer | 1:00 |
| **Total** | **15:00** |
