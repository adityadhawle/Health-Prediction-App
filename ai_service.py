
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL = "qwen/qwen3.8-27b"

def generate_health_remarks(glucose, haemoglobin, cholesterol):

    if not GROQ_API_KEY:
        raise ValueError("Groq API key not found in .env file.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a cautious health information assistant. "
                    "Explain possible observations from blood test values. "
                    "Do not diagnose diseases. Mention that interpretation "
                    "depends on units, laboratory reference ranges, age and "
                    "medical history. Recommend consulting a qualified doctor."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Glucose: {glucose}, "
                    f"Haemoglobin: {haemoglobin}, "
                    f"Cholesterol: {cholesterol}. "
                    "Provide a concise response in plain text with 3 short bullet points. "
		    "Cover all three test values. Avoid markdown tables. "
		    "Do not stop until all three values are covered."
                )
            }
        ],
        "temperature": 0.3,
        "max_completion_tokens": 1000
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]
