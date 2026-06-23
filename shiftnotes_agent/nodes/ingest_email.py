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


def ingest_email(state: ShiftNotesState) -> ShiftNotesState:
    run_id = state.get("run_id", str(uuid.uuid4()))
    log_node_entry(logger, "ingest_email", run_id)

    try:
        if os.getenv("GMAIL_OAUTH_TOKEN"):
            reports = _read_from_gmail_mcp()
        else:
            logger.info("GMAIL_OAUTH_TOKEN not set — reading from CSV fallback")
            reports = _read_from_csv()

        log_node_exit(logger, "ingest_email", run_id, f"loaded {len(reports)} reports")

        return {
            **state,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "raw_reports": reports,
            "error": None
        }

    except Exception as e:
        log_error(logger, "ingest_email", run_id, str(e))
        return {
            **state,
            "run_id": run_id,
            "error": f"ingest_email failed: {str(e)}"
        }


def _get_access_token() -> str:
    """Loads and auto-refreshes the Google OAuth access token from token.json."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    token_path = Path(__file__).parent.parent.parent / "token.json"
    creds = Credentials.from_authorized_user_file(str(token_path))
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json())
    return creds.token


def _read_from_gmail_mcp() -> list[dict]:
    """
    Reads JotForm shift report emails from Gmail via OpenAI MCP connector.
    Falls back to CSV if Gmail returns no results.
    """
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    resp = client.responses.create(
        model="gpt-4o-mini",
        tools=[
            {
                "type": "mcp",
                "server_label": "gmail",
                "connector_id": "connector_gmail",
                "authorization": _get_access_token(),
                "require_approval": "never",
            }
        ],
        input=(
            "Search Gmail for emails from JotForm with subject containing "
            "'Bowls & Buns Shift Notes'. For each email found, extract: "
            "date, lead_name, food_quality_rating, food_quantity_rating, "
            "food_concerns_or_outages, team_members_who_did_well, "
            "guest_issues_for_the_day, operational_notes, "
            "number_of_unclaimed_lunches. "
            "Return ONLY a JSON array of report objects, nothing else."
        ),
    )

    raw = (resp.output_text or "").strip()

    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]

    try:
        result = json.loads(raw)
        if isinstance(result, list) and result:
            return result
        logger.warning("Gmail MCP returned no emails — falling back to CSV")
        return _read_from_csv()
    except (json.JSONDecodeError, AttributeError):
        logger.warning("Gmail MCP returned no results — falling back to CSV")
        return _read_from_csv()


def _read_from_csv() -> list[dict]:
    """
    Reads mock shift reports from CSV.
    Fallback when Gmail MCP returns no results.
    """
    df = pd.read_csv(MOCK_CSV_PATH)
    return df.to_dict(orient="records")