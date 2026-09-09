from flask import Flask, render_template, request, jsonify
import json
from ddgs import DDGS

app = Flask(__name__)

# Load local knowledge
with open("question.json", "r", encoding="utf-8") as file:
    knowledge = json.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_question = data.get("question", "").strip()

    # 1. Check local knowledge first
    for question, answer in knowledge.items():
        if user_question.lower() == question.lower():
            return jsonify({"answer": answer})

    # 2. If not found, search the Internet
    try:
        results = DDGS().text(user_question, max_results=3)

        if results:
            answer = results[0].get("body", "I couldn't find an answer .")
            return jsonify({"answer": answer})

    except Exception as e:
        print("Internet search error:", e)

    # 3. Nothing found
    return jsonify({
        "answer": "I couldn't find an answer on the Internet."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)