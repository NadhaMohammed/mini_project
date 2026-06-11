import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

data = {
    "username": "testadmin2",
    "password": "hashed_password",
    "college_code": "TEST-123"
}

print(f"Testing Supabase insert...")
try:
    response = requests.post(f"{SUPABASE_URL}/rest/v1/admin_username_pass", headers=headers, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
