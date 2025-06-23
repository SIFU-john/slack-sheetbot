import os
import httpx
import pandas as pd

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

async def answer_query(df: pd.DataFrame, query: str) -> str:
    prompt = f"""
You're a data analyst. The user asked: "{query}"

Data Preview:
{df.head().to_markdown()}
Columns: {df.columns.tolist()}

Answer clearly and concisely.
"""

    payload = {
        "model": "mistral-medium",  # use "mistral-tiny", "mistral-small", "mistral-medium" as needed
        "messages": [
            {"role": "system", "content": "You are a helpful spreadsheet analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "top_p": 0.9
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(MISTRAL_ENDPOINT, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
