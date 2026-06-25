import pandas as pd
import uuid
import json
import os
from datetime import datetime
from pathlib import Path

from shiftnotes_agent.state import ShiftNotesState
from shiftnotes_agent.logger import get_logger, log_node_entry, log_node_exit, log_error

logger = get_logger("ingest_email")

MOCK_CSV_PATH = Path(__file__).parent.parent.parent / "prototype" / "mock_shift_notes.csv"

# JotForm MCP server (official remote MCP endpoint)
JOTFORM_MCP_URL = "https://mcp.jotform.com"


def ingest_email(state: ShiftNotesState) -> ShiftNotesState:
    run_id = state.get("run_id", str(uuid.uuid4()))
    log_node_entry(logger, "ingest_email", run_id)

    try:
        # Use JotForm MCP only when both an OAuth token and a form ID are set.
        # Otherwise fall back to the synthetic CSV so the demo always runs.
        if os.getenv("JOTFORM_OAUTH_TOKEN") and os.getenv("JOTFORM_FORM_ID"):
            reports = _read_from_jotform_mcp()
        else:
            logger.info(
                "JOTFORM_OAUTH_TOKEN / JOTFORM_FORM_ID not set - reading from CSV fallback"
            )
            reports = _read_from_csv()

        log_node_exit(logger, "ingest_email", run_id, f"loaded {len(reports)} reports")

        return {
            **state,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "raw_reports": reports,
            "error": None,
        }

    except Exception as e:
        log_error(logger, "ingest_email", run_id, str(e))
        return {
            **state,
            "run_id": run_id,
            "error": f"ingest_email failed: {str(e)}",
        }


def _read_from_jotform_mcp() -> list[dict]:
    """
    Reads shift report submissions from JotForm via the official JotForm MCP
    server (https://mcp.jotform.com), using the OpenAI Responses API as the
    MCP client.

    The LLM is given the JotForm MCP server as a tool and asked to call
    get_submissions for the configured form. This is a genuine MCP integration:
    the model discovers and invokes MCP tools through the protocol rather than
    us calling a REST endpoint directly.

    Falls back to the synthetic CSV if JotForm returns no usable submissions.
    """
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    form_id = os.getenv("JOTFORM_FORM_ID")

    resp = client.responses.create(
        model="gpt-4o-mini",
        tools=[
            {
                "type": "mcp",
                "server_label": "jotform",
                "server_url": JOTFORM_MCP_URL,
                "authorization": os.getenv("JOTFORM_OAUTH_TOKEN"),
                "require_approval": "never",
            }
        ],
        input=(
            f"Call get_submissions for JotForm form {form_id}. "
            "For each submission, extract these fields: date, lead_name, "
            "food_quality_rating, food_quantity_rating, food_concerns_or_outages, "
            "team_members_who_did_well, guest_issues_for_the_day, "
            "operational_notes, number_of_unclaimed_lunches. "
            "Return ONLY a JSON array of submission objects, nothing else."
        ),
    )

    raw = (resp.output_text or "").strip()

    # Strip markdown code fences if the model wrapped the JSON
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]

    try:
        result = json.loads(raw)
        if isinstance(result, list) and result:
            logger.info(f"JotForm MCP returned {len(result)} submissions")
            return result
        logger.warning("JotForm MCP returned no submissions - falling back to CSV")
        return _read_from_csv()
    except (json.JSONDecodeError, AttributeError):
        logger.warning("JotForm MCP returned unparseable output - falling back to CSV")
        return _read_from_csv()


def _read_from_csv() -> list[dict]:
    """
    Reads mock shift reports from CSV.
    Fallback when JotForm MCP is not configured or returns no results.
    """
    df = pd.read_csv(MOCK_CSV_PATH)
    return df.to_dict(orient="records")