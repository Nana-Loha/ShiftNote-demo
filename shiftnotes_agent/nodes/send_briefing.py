import base64
import os
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from shiftnotes_agent.state import ShiftNotesState
from shiftnotes_agent.logger import get_logger, log_node_entry, log_node_exit, log_error

logger = get_logger("send_briefing")

OUTPUT_DIR = Path("briefings")
_PROJECT_ROOT = Path(__file__).parent.parent.parent
_TOKEN_PATH = _PROJECT_ROOT / "token.json"
_CREDENTIALS_PATH = _PROJECT_ROOT / "credentials.json"
_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def send_briefing(state: ShiftNotesState) -> ShiftNotesState:
    run_id = state.get("run_id", "unknown")
    log_node_entry(logger, "send_briefing", run_id)

    try:
        if state.get("error"):
            return state

        briefing = state.get("generated_briefing", "")

        if not briefing:
            log_node_exit(logger, "send_briefing", run_id, "no briefing to send")
            return {**state, "briefing_sent": False}

        _send_via_gmail_api(briefing, run_id)

        log_node_exit(logger, "send_briefing", run_id, "briefing delivered")

        return {**state, "briefing_sent": True}

    except Exception as e:
        log_error(logger, "send_briefing", run_id, str(e))
        return {
            **state,
            "briefing_sent": False,
            "error": f"send_briefing failed: {str(e)}"
        }


def _get_gmail_service():
    """Loads Gmail credentials, refreshing or running OAuth flow as needed."""
    creds = None

    if _TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(_TOKEN_PATH), _SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(_CREDENTIALS_PATH), _SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(_TOKEN_PATH, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def _send_via_gmail_api(briefing: str, run_id: str):
    """
    Sends briefing to Ted's inbox via the Gmail API.
    Falls back to saving a file if credentials are missing or the send fails.
    """
    ted_email = os.getenv("TED_EMAIL", "")

    if not ted_email:
        logger.info("TED_EMAIL not set - saving briefing to file")
        _save_to_file(briefing, run_id)
        return

    if not _TOKEN_PATH.exists() and not _CREDENTIALS_PATH.exists():
        logger.info("No token.json or credentials.json found - saving briefing to file")
        _save_to_file(briefing, run_id)
        return

    try:
        service = _get_gmail_service()

        message = EmailMessage()
        message["To"] = ted_email
        message["Subject"] = f"ShiftNotes Weekly Briefing - Run {run_id}"
        message.set_content(briefing)

        encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
        result = service.users().messages().send(
            userId="me",
            body={"raw": encoded}
        ).execute()

        logger.info(f"Briefing sent to {ted_email} via Gmail API - message_id: {result['id']}")

    except Exception as e:
        logger.warning(f"Gmail API send failed - falling back to file: {e}")
        _save_to_file(briefing, run_id)


def _save_to_file(briefing: str, run_id: str):
    """Saves briefing to local file when Gmail delivery is unavailable."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = OUTPUT_DIR / f"briefing_{timestamp}_{run_id}.txt"

    with open(filepath, "w") as f:
        f.write("ShiftNotes Weekly Briefing\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"Run ID: {run_id}\n")
        f.write("=" * 50 + "\n\n")
        f.write(briefing)

    logger.info(f"Briefing saved to {filepath}")