import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_ai_review(code: str) -> dict:
    try:
        prompt = f"""
You are a senior software engineer.

Analyze the following code and return STRICT JSON in this format:

{{
  "bugs": [],
  "security": [],
  "performance": [],
  "best_practices": [],
  "score": number
}}

Code:
{code}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        text = response.choices[0].message.content.strip()

        # Extract JSON safely
        start = text.find("{")
        end = text.rfind("}") + 1

        if start == -1 or end == -1:
            raise ValueError("No JSON found in AI response")

        return json.loads(text[start:end])

    except Exception as e:
        # ✅ NEVER crash FastAPI again
        return {
            "bugs": ["AI processing error"],
            "security": [],
            "performance": [],
            "best_practices": [str(e)],
            "score": 0,
        }
