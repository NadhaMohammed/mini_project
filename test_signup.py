import requests

url = "http://127.0.0.1:5000/signup"
data = {
    "username": "testadmin",
    "password": "password123"
}

print(f"Testing signup at {url}...")
try:
    response = requests.post(url, data=data, allow_redirects=False)
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Location: {response.headers.get('Location')}")
except Exception as e:
    print(f"Error: {e}")
