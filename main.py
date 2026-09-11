

from flask import Flask, render_template, request, jsonify, send_file
import json
from ddgs import DDGS
from gtts import gTTS
import io

app = Flask(__name__)


# --------------------------------
# Load local knowledge
# --------------------------------

with open("question.json", "r", encoding="utf-8") as file:
    knowledge = json.load(file)


# --------------------------------
# Home page
# --------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# --------------------------------
# AI Question Endpoint
# --------------------------------

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()


    # --------------------------------
    # Check request
    # --------------------------------

    if not data:

        return jsonify({
            "answer": "Please ask me something."
        })


    user_question = data.get(
        "question",
        ""
    ).strip()


    if not user_question:

        return jsonify({
            "answer": "Please ask me a question."
        })


    # --------------------------------
    # Get Internet ON/OFF setting
    # --------------------------------

    internet_enabled = data.get(
        "internet",
        True
    )


    # --------------------------------
    # 1. Check local knowledge first
    # --------------------------------

    for question, answer in knowledge.items():

        if user_question.lower() == question.lower():

            return jsonify({
                "answer": answer
            })


    # --------------------------------
    # 2. Internet search
    # --------------------------------

    if internet_enabled:

        try:

            results = DDGS().text(
                user_question,
                max_results=3
            )


            if results:

                answer = results[0].get(
                    "body",
                    "I couldn't find a good answer."
                )


                return jsonify({
                    "answer": answer
                })


        except Exception as e:

            print(
                "Internet search error:",
                e
            )


    # --------------------------------
    # 3. Internet OFF / nothing found
    # --------------------------------

    if not internet_enabled:

        return jsonify({
            "answer":
                "Internet is OFF. I don't know this yet."
        })


    return jsonify({
        "answer":
            "I couldn't find an answer on the Internet."
    })


# --------------------------------
# AI Voice Endpoint
# --------------------------------

@app.route("/speak", methods=["POST"])
def speak():

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "No data received."
        }), 400


    text = data.get(
        "text",
        ""
    ).strip()


    if not text:

        return jsonify({
            "error": "No text provided."
        }), 400


    try:

        # --------------------------------
        # Create temporary audio in memory
        # --------------------------------

        audio = io.BytesIO()


        # --------------------------------
        # Convert text to speech
        # --------------------------------

        tts = gTTS(
            text=text,
            lang="en",
            slow=False
        )


        # --------------------------------
        # Save MP3 into memory
        # --------------------------------

        tts.write_to_fp(audio)


        # --------------------------------
        # Move back to beginning
        # --------------------------------

        audio.seek(0)


        # --------------------------------
        # Send audio to browser
        # --------------------------------

        return send_file(
            audio,
            mimetype="audio/mpeg",
            as_attachment=False
        )


    except Exception as e:

        print(
            "TTS error:",
            e
        )


        return jsonify({
            "error":
                "Voice generation failed."
        }), 500


# --------------------------------
# Run Flask
# --------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
