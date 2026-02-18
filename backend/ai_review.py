import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load .env variables
load_dotenv()

# ✅ Create Groq client correctly
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_ai_review(code: str) -> dict:
    """
    Generate structured AI code review in strict JSON format.
    """

    try:
        prompt = f"""
You are a senior software engineer.

Analyze the following code and return ONLY valid JSON.
Do NOT include markdown, explanations, or extra text.

Return strictly in this format:

{{
  "bugs": [],
  "security": [],
  "performance": [],
  "best_practices": [],
  "score": 0
}}

Code:
{code}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        text = response.choices[0].message.content.strip()

        # Remove ```json markdown if present
        if "```" in text:
            parts = text.split("```")
            text = parts[1] if len(parts) > 1 else text
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        # Extract JSON safely
        start = text.find("{")
        end = text.rfind("}") + 1

        if start == -1 or end == -1:
            raise ValueError("No JSON found in AI response")

        json_text = text[start:end]

        return json.loads(json_text)

    except Exception as e:
        return {
            "bugs": ["AI processing error"],
            "security": [],
            "performance": [],
            "best_practices": [str(e)],
            "score": 0,
        }
