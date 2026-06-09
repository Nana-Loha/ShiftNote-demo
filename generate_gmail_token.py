import os
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import set_key

# ตั้งค่า Scopes ตามที่ MCP ต้องการ
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def generate_token():
    # โหลด client secret ที่ดาวน์โหลดมาจาก Google Cloud
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES
    )
    
    # รัน flow เพื่อขอสิทธิ์ผ่านเบราว์เซอร์
    creds = flow.run_local_server(port=0)
    
    # นำ Access Token ออกมา
    access_token = creds.token
    
    # อัปเดต .env ไฟล์โดยตรง
    set_key('.env', 'GMAIL_OAUTH_TOKEN', access_token)
    print(f"Success! GMAIL_OAUTH_TOKEN updated in .env: {access_token[:10]}...")

if __name__ == '__main__':
    generate_token()