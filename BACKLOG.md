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
- Confirm Gmail MCP email delivery — ⚠️ Partial. MCP connector code wired in Node 1 and Node 5; Gmail OAuth token returns 401 due to OpenAI connector incompatibility. CSV/file fallback is active production behavior.
- Prototype Streamlit drill-down detail view for Ted — ⚠️ Partial. Drill Down button wired in Briefings tab; detail view not yet implemented.
- Document risks and limitations in RISKS.md — ⚠️ Partial. RISKS.md updated with 10 tracked risks; ongoing.
- Tune hybrid signal classifier thresholds on real JotForm sample data — ❌ Pending. Still using synthetic mock data. Planned for Week 10.

## Week 9 — Additional Technical Items

- Set up GitHub Actions CI workflow (`.github/workflows/ci.yml`) — ✅ Done. CI runs `uv run pytest tests/ -v` on push and PR to main.
- Fix HITL invalid input handling — ❌ Pending. `human_review.py` currently silently defaults any invalid input to `accept`. Validation loop planned for Week 10.
- Wire escalate path to email shift lead via Gmail MCP (Node 5 Option B) — ❌ Pending. Escalation note is captured in state but no email is sent. Planned for Week 10.

## Week 9 QA Checkpoint Artifacts

The Week 9 submission will include the following artifacts:

- Peer review feedback received and response actions taken.
- HITL validation evidence with a non-team user.
- Backlog completion report targeting 80% or more of planned work.
- Technical report draft covering sections 1 through 3.

### Artifact integration plan

- Collect peer review notes on the LangGraph architecture, MCP plan, and risk/backlog documentation.
- Capture non-team HITL validation using a structured checklist and evidence notes.
- Track completed backlog items as a percentage of planned Week 9 priorities.
- Draft the first three sections of the technical report to document architecture, implementation, and validation approach.

---

## Week 10 — Final Delivery Requirements

### Required Deliverables

- Codebase: documented, test-covered, reproducible environment
- README.md: setup, run steps, architecture summary
- CLAUDE.md: project guidance and workflow context
- 10-page technical report with the following sections:
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
- One HITL checkpoint in action
- One failure mode and recovery demonstration
- Brief walkthrough of architecture and key design choices
