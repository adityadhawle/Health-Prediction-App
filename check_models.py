
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/models"

response = requests.get(
    url,
    headers={"Authorization": f"Bearer {api_key}"},
    timeout=30
)

print("Status:", response.status_code)

if response.ok:
    models = response.json()["data"]

    print("\nAvailable models:\n")

    for model in models:
        if model.get("active", True):
            print(model["id"])
else:
    print(response.text)
