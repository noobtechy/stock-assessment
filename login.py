import os
import requests
import urllib.parse
import dotenv

dotenv.load_dotenv(override=True)

# Define the parameters
client_id = os.getenv("CLIENT_ID")
redirect_uri = urllib.parse.quote(os.getenv("REDIRECT_URI"), safe="")
response_type = 'code'

# Construct the URL
url = f'https://api.upstox.com/v2/login/authorization/dialog?client_id={client_id}&redirect_uri={redirect_uri}&response_type={response_type}'

# Send the GET request
response = requests.get(url)

# Print the response
if response.status_code == 200:
    print('Success:', response.url)
else:
    print('Error:', response.status_code, response.text)
