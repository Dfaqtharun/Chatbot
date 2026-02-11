from flask import Flask, request, jsonify, render_template
import requests
import re
import os

app = Flask(__name__)
API_KEY = os.environ.get("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ✅ Allowed topic keywords
CASUAL_KEYWORDS = [
    "hi", "hello", "how are you", "your name", "who are you",
    "good morning", "good evening", "bye"
]

SQL_KEYWORDS = [
    "sql", "select", "insert", "update", "delete",
    "join", "where", "group by", "order by",
    "mysql", "postgresql", "database"
]

def is_allowed(message: str) -> bool:
    msg = message.lower()

    for word in CASUAL_KEYWORDS + SQL_KEYWORDS:
        if word in msg:
            return True
    return False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    # ❌ Restriction check
    if not is_allowed(user_msg):
        return jsonify({
            "reply": "❌ Sorry! I can only answer casual chat or SQL-related questions."
        })

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a friendly assistant that ONLY answers casual conversation and SQL-related questions."
            },
            {
                "role": "user",
                "content": user_msg
            }
        ]
    }

    try:
        r = requests.post(URL, headers=HEADERS, json=payload, timeout=20)
        r.raise_for_status()
        data = r.json()
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True, port=5002)
