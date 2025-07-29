from flask import Flask, request, jsonify
from flask_cors import CORS
from hecate import Hecate
import argparse
import subprocess
import sys
import os
import speech_recognition as sr

app = Flask(__name__)
CORS(app)

# Instantiate Hecate
hecate = Hecate()


def run_server():
    """Start the Flask API server."""
    app.run(host="0.0.0.0", port=8080)

@app.route("/health", methods=["GET"])
def health():
    """Simple health check endpoint."""
    return jsonify({"status": "ok"})

@app.route("/talk", methods=["POST"])
def talk():
    data = request.json
    user_input = data.get("message", "")
    response = hecate.respond(user_input)
    try:
        with open("conversation.log", "a") as log:
            log.write(f"User: {user_input}\n")
            log.write(f"Hecate: {response}\n")
    except Exception:
        pass
    return jsonify({"reply": response})


@app.route("/talk/audio", methods=["POST"])
def talk_audio():
    """Accept an audio file and return the transcript and response."""
    if "file" not in request.files:
        return jsonify({"error": "Missing audio file"}), 400
    audio_file = request.files["file"]
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
    except Exception as e:
        return jsonify({"error": f"Speech recognition failed: {e}"}), 400
    response = hecate.respond(text)
    return jsonify({"transcript": text, "reply": response})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hecate API server")
    parser.add_argument(
        "-b",
        "--background",
        action="store_true",
        help="Run the front end API server in the background",
    )
    args = parser.parse_args()

    if args.background:
        # Relaunch this script detached from the current session
        cmd = [sys.executable, os.path.abspath(__file__)]
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
        print("Server started in background")
    else:
        run_server()
