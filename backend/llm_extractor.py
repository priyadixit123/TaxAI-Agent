import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")




api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in backend/.env")


client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


def extract_salary_data(text: str) -> dict:

    prompt = f"""
You are a tax document extraction assistant.

Extract salary information from the following OCR text.

OCR TEXT:
{text}

Return ONLY valid JSON:

{{
    "employee_name": null,
    "month": null,
    "basic_salary": null,
    "hra": null,
    "other_allowance": null,
    "gross_salary": null,
    "tds": null,
    "net_salary": null
}}

Rules:
- Return numbers as numbers.
- If a value is not present, return null.
- Do not invent information.
"""

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError:
        raise ValueError(
            f"LLM returned invalid JSON: {result}"
        )