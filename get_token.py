import os
import requests
import dotenv


dotenv.load_dotenv(override=True)

url = 'https://api.upstox.com/v2/login/authorization/token'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
    'code': os.getenv("CODE"),
    'client_id': os.getenv("CLIENT_ID"),
    'client_secret': os.getenv("CLIENT_SECRET"),
    'redirect_uri': os.getenv("REDIRECT_URI"),
    'grant_type': 'authorization_code',
}

response = requests.post(url, headers=headers, data=data)

print(response.status_code)
print(response.json())