# BACKLOG

## Week 7 — Completed Items

- Project kickoff and initial architecture planning
- Architecture diagram for final project
- SPEC.md draft and team task backlog

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
