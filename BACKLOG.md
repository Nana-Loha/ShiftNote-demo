# BACKLOG

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

## Week 9 — Remaining Priorities

- Wire Gmail MCP OAuth for Node 1 (ingestion) — replace CSV fallback with live Gmail read.
- Wire Gmail MCP OAuth for Node 5 (delivery) — replace file fallback with Gmail send to Ted.
- Fix HITL invalid input handling — add validation and retry prompt in `human_review` node and `run_pipeline.py`.
- Wire escalate path to email shift lead via Gmail MCP (Node 5 Option B).
- Tune hybrid signal classifier thresholds on real JotForm sample data.
- Set up GitHub Actions CI workflow (`.github/workflows/ci.yml`) — 10 tests currently passing locally.

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
