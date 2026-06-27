# Known Risks

## Current Risk Register (as of Week 10 final submission)

| Risk | Likelihood | Impact | Status | Mitigation |
|---|---|---|---|---|
| Live JotForm form not yet provisioned — pipeline runs on synthetic data | High | Medium | Open | JotForm MCP wired in Node 1; activating requires only `JOTFORM_OAUTH_TOKEN` + `JOTFORM_FORM_ID` in `.env` — no code change |
| Gmail OAuth in testing mode — limited to approved test users | High | Medium | Open | Production use requires app verification or a service account; file fallback ensures pipeline always completes |
| Signal detection thresholds tuned on synthetic data — may misfire on real submissions | Medium | High | Open | Thresholds documented per signal; recalibration planned when live JotForm data is available |
| HuggingFace model download (~330MB) on first run requires stable internet | Medium | Low | Mitigated | Cached after first run; GitHub Actions workflow caches the model between CI runs |
| ChromaDB empty until `embed.py` is run — RAG returns no context | Medium | Medium | Mitigated | Documented in README Quick Start (step 4); pipeline continues without RAG context |
| Streamlit drill-down detail view (HITL "drill_down" option) not fully implemented | High | Low | Open | Button is wired; detail view pending — known limitation documented in README |
| Escalate path does not email shift lead — note is logged only | High | Low | Open | Escalation note captured in state; secondary email to shift lead is future work |
| ChromaDB collection mismatch between prototype and agent RAG | Low | High | Resolved | Fixed — both use the same collection name and embedding model |
| HITL invalid input silently accepted | Low | High | Resolved | Fixed in Week 10 — validation loop re-prompts; node returns error state on invalid input |
| Technical report incomplete | Low | High | Resolved | Full 11-page PDF submitted covering all 6 required sections |
