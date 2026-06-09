# ShiftNotes — Technical Report Draft
**AI 410 Final Project**
**Team:** Pitchanan Lohavanichbutr, Geetanjali Kulkarni, Careen Mollel, Isaac Wablemvo
**Date:** June 7, 2026

---

## Section 1: Problem Statement and Business Context

Dsquared Hospitality operates multiple food kiosks at T-Mobile HQ under the Bowls & Buns brand. Shift leads submit daily JotForm reports covering food quality, inventory concerns, guest feedback, and employee recognition. Before ShiftNotes, these reports accumulated in the GM (Ted)'s inbox and required manual review to identify patterns.

The core problem is information loss through manual aggregation. When Ted reads reports one by one, recurring issues such as repeated chicken shortages across kiosks or consistent guest requests for poke are easy to miss. Trends that would be obvious in aggregate remain invisible at the individual-report level.

ShiftNotes is an intelligence layer that automatically reads shift reports, detects operational signals, and delivers a plain-English briefing to Ted — so he spends less time reading and more time acting. The system is designed to be passive: shift leads do not change their submission workflow, and Ted receives intelligence rather than having to query for it.

**Users:**
- **Ted (GM)** — primary recipient of briefings; reviews and acts on HITL decisions
- **Shift leads** — submit JotForm reports; no change to their current workflow

**Success criteria:**
- Operational signals (chicken shortages, poke requests, ops issues, team recognition) are detected automatically from freeform report text
- A plain-English briefing reaches Ted after each reporting cycle
- Ted can accept, drill down, or escalate from a single interface

---

## Section 2: Architecture and Framework Rationale

ShiftNotes uses a 6-node LangGraph stateful agent pipeline with RAG (ChromaDB + OpenAI) and a human-in-the-loop checkpoint at Node 6.

### Pipeline Overview

```
Shift lead writes report
    ↓ JotForm → Gmail inbox
Node 1 — ingest_email       reads reports via Gmail MCP (CSV fallback)
    ↓
Node 2 — classify_intent    routes: signals vs. RAG query
    ↓
Node 3 — detect_signals     hybrid regex + HuggingFace zero-shot
    ↓
Node 4 — retrieve_and_generate   ChromaDB search → OpenAI → briefing
    ↓
Node 5 — send_briefing      Gmail MCP send to Ted (file fallback)
    ↓
Node 6 — human_review (HITL)    Ted: accept | drill_down | escalate
```

### Framework Decisions

| Framework | Role | Rationale |
|-----------|------|-----------|
| LangGraph | Pipeline orchestration | Stateful graph execution, native HITL interrupt, conditional routing |
| ChromaDB | Vector store | Lightweight local RAG retrieval — no external service required |
| OpenAI gpt-4o-mini | Briefing generation | Cost-efficient, compatible with Gmail MCP connector |
| Gmail MCP | Email ingestion and delivery | Standardized integration; isolates MCP logic to Node 1 and Node 5 |
| HuggingFace Transformers | Zero-shot signal fallback | `cross-encoder/nli-MiniLM2-L6-H768` — no fine-tuning required |
| Streamlit | HITL review UI | Hosts the Briefings tab and HITL decision buttons |

### Key Design Decisions

**Send-then-review (not review-then-send):** The briefing is generated and delivered to Ted before the HITL checkpoint fires. Intelligence comes to Ted passively — he does not have to request it. Node 6 then interrupts the graph and waits for his decision.

**Hybrid signal detection:** Regex handles deterministic cases cheaply. HuggingFace zero-shot (`cross-encoder/nli-MiniLM2-L6-H768`) handles ambiguous text. Per-signal confidence thresholds prevent false positives:

| Signal | Threshold |
|--------|-----------|
| `chicken_shortage` | 0.70 |
| `poke_request` | 0.50 |
| `ops_issue` | 0.70 |
| `team_recognition` | 0.95 |

**MCP as isolated swap points:** Gmail MCP is wired only at Node 1 (ingestion) and Node 5 (delivery). Both nodes fall back gracefully to CSV read / file write when `GMAIL_OAUTH_TOKEN` is not set, so the entire pipeline runs in offline development mode without changing graph logic.

---

## Section 3: Implementation Progress and Validation Evidence

### Pipeline Validation

End-to-end pipeline ran successfully (Run ID: `14feff7a`):

- 100 reports ingested from mock CSV
- 45 signals detected across 4 signal types
- All 3 HITL paths tested: accept ✅, drill_down ✅, escalate ✅
- CI: 10/10 pytest tests passing
- GitHub Actions CI: green badge on push to main

**Signal detection results (Node 3):**

| Signal | Count | Method |
|--------|-------|--------|
| `chicken_shortage` | 15 | regex + HuggingFace |
| `poke_request` | 18 | regex + HuggingFace |
| `ops_issue` | 16 | regex |
| `team_recognition` | 32 | regex |

**HITL decision paths validated:**

| Decision | Result |
|----------|--------|
| `accept` | Decision recorded — pipeline complete |
| `drill_down` | Decision recorded — detail view pending (Week 10) |
| `escalate` | Decision recorded — escalation note captured |

### CI Evidence

10/10 pytest tests passing across two test files:

```
tests/test_signal_classifier.py — 9 tests (text building, regex, classification)
tests/test_state.py             — 1 test  (LangGraph state schema)
10 passed
```

GitHub Actions CI runs `uv run pytest tests/ -v` on every push and PR to main.
→ https://github.com/Nana-Loha/ShiftNote-demo/actions

### Known Limitations

1. **Gmail MCP OAuth** — token incompatibility with OpenAI connector returns 401; CSV/file fallback is active for Week 9
2. **Signal classifier** — tuned on synthetic mock data; JotForm threshold tuning planned for Week 10
3. **Streamlit drill-down** — detail view not yet implemented; button is wired but shows no additional content
4. **HITL input validation** — invalid inputs silently default to `accept`; validation loop planned for Week 10
5. **RAG evaluation** — hit rate and MRR not yet measured; metric tracking planned for Week 10

→ See [RISKS.md](./RISKS.md) for the full 10-item risk register
