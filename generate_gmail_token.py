from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
TOKEN_PATH = Path(__file__).parent / "token.json"


def generate_token():
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    TOKEN_PATH.write_text(creds.to_json())
    print(f"token.json saved to {TOKEN_PATH}")


if __name__ == "__main__":
    generate_token()
