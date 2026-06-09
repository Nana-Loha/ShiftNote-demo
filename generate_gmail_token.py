from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import set_key

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def generate_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES
    )
    creds = flow.run_local_server(port=0)
    access_token = creds.token
    set_key('.env', 'GMAIL_OAUTH_TOKEN', access_token)
    print(f"Success! GMAIL_OAUTH_TOKEN updated in .env: {access_token[:10]}...")

if __name__ == '__main__':
    generate_token()