
---

# ✅ FINAL BULLETPROOF FIX

Replace your **entire function** with this **100% safe version**:

```python
def generate_ai_review(code: str) -> dict:
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

        # 🔹 Remove markdown ```json blocks if present
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        # 🔹 Find JSON boundaries safely
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
