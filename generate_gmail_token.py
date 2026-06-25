"""
generate_gmail_token.py

One-time script to generate token.json for Gmail sending.

Run this once: it opens a browser, you log in with a Gmail account that is
registered as a Test User on the project's OAuth consent screen, approve the
gmail.send permission, and it writes token.json to the project root.

After this, Node 5 (send_briefing.py) can send real emails without prompting.

Requires credentials.json (downloaded from Google Cloud Console) in this folder.
"""

from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

# Must match the scope Node 5 uses in send_briefing.py
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

PROJECT_ROOT = Path(__file__).parent
CREDENTIALS_PATH = PROJECT_ROOT / "credentials.json"
TOKEN_PATH = PROJECT_ROOT / "token.json"


def main():
    if not CREDENTIALS_PATH.exists():
        print("ERROR: credentials.json not found in the project root.")
        print(f"Expected at: {CREDENTIALS_PATH}")
        print("Download it from Google Cloud Console -> Credentials -> OAuth client (Desktop app).")
        return

    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
    creds = flow.run_local_server(port=0)

    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())

    print(f"Success! token.json written to {TOKEN_PATH}")
    print("You can now run: uv run python run_pipeline.py")


if __name__ == "__main__":
    main()
