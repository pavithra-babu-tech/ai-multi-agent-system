from flask import Flask, request, jsonify
import requests

from tools import calculator,weather

app = Flask(__name__)

# ---------------- OLLAMA FUNCTION ----------------
def run_ollama(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3:latest",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload, timeout=300)

    return response.json()["response"]

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return "API is running 🚀"

@app.route("/process", methods=["POST"])
def process():
    try:
        data = request.get_json()
        query = data.get("query", "")

        print("📥 Query received:", query)

        # 🔥 TOOL LOGIC (ADD THIS)

        # Calculator
        if any(op in query for op in ["+", "-", "*", "/"]):
            result = calculator(query)
            return jsonify({
                "research": f"Calculation Result: {result}",
                "summary": result,
                "email": f"The result of your calculation is {result}"
            })

        # Weather
        if "weather" in query.lower():
            city = query.lower().replace("weather", "").strip()
            result = weather(city)
            return jsonify({
    "research": result,
    "summary": f"Current weather: {result}",
    "email": f"Subject: Weather Update\n\nDear User,\n\nThe current weather is:\n{result}\n\nRegards"
})

        # 🤖 AI (keep your existing code below)
        full_prompt = f""" ... """

        result = run_ollama(full_prompt)

        # your parsing + return
        full_prompt = f"""
You MUST respond in EXACT format:

RESEARCH:
(detailed explanation)

SUMMARY:
(short summary)

EMAIL:
(professional email)

Now answer this:
{query}
"""

        print("👉 Calling Ollama...")

        result = run_ollama(full_prompt)

        print("RAW OUTPUT:\n", result)

        # ---------------- PARSING ----------------
        research = summary = email = "Not generated"

        if "SUMMARY:" in result:
            parts = result.split("SUMMARY:")
            research = parts[0].replace("RESEARCH:", "").strip()

            if "EMAIL:" in parts[1]:
                parts2 = parts[1].split("EMAIL:")
                summary = parts2[0].strip()
                email = parts2[1].strip()
            else:
                summary = parts[1].strip()

        return jsonify({
            "research": research,
            "summary": summary,
            "email": email
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5000)