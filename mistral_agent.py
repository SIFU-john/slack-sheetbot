import os
from mistralai import mistral

api_key = os.getenv("MISTRAL_API_KEY")

async def answer_query(df, query):
    prompt = f"""
You're a data analyst. The user asked: "{query}"

Data Preview:
{df.head().to_markdown()}
Columns: {df.columns.tolist()}

Answer clearly and concisely:
"""
    response = client.chat.complete(
        model="Mistral Medium",
        messages=[
            {"role": "system", "content": "You are a helpful spreadsheet analyst."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
