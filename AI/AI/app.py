from flask import Flask, request, jsonify, render_template
import os
from flask_socketio import SocketIO, emit  # Import SocketIO
import whisper
from deepgram import Deepgram
import yt_dlp as youtube_dl
from gtts import gTTS
from flask_cors import CORS
import time
import subprocess
import numpy as np
import io
import torch
import soundfile as sf
import uuid
import eventlet  # Required for WebSocket Support

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize SocketIO with async_mode='eventlet' for WebSockets
socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000", async_mode="eventlet")

# Load Whisper model
model = whisper.load_model("base")

# Deepgram API Key
DEEPGRAM_API_KEY = "c6405ba98eef90bdc74edd6b1ff9a03fb3752373"
dg_client = Deepgram(DEEPGRAM_API_KEY)

# Ensure temp directory exists
os.makedirs("temp", exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


# 1. Audio to Text
@app.route("/transcribe/audio", methods=["POST"])
def transcribe_audio():
    file = request.files["file"]
    file_path = f"temp/{file.filename}"
    file.save(file_path)

    # Transcribe using Whisper
    result = model.transcribe(file_path)
    os.remove(file_path)

    return jsonify({"transcription": result["text"]})


@app.route("/transcribe/video", methods=["POST"])
def transcribe_video():
    file = request.files["file"]

    # Ensure the temp directory exists
    os.makedirs("temp", exist_ok=True)

    # Generate a unique filename to avoid issues
    file_extension = file.filename.rsplit(".", 1)[-1]  # Get file extension
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join("temp", unique_filename)

    file.save(file_path)

    # Extract audio using subprocess
    audio_path = file_path.rsplit(".", 1)[0] + ".wav"  # Change extension to .wav
    subprocess.run(
        ["ffmpeg", "-i", file_path, "-q:a", "0", "-map", "a", audio_path], check=True
    )

    # Transcribe using Whisper
    result = model.transcribe(audio_path)

    # Cleanup files
    os.remove(file_path)
    os.remove(audio_path)

    return jsonify({"transcription": result["text"]})


# 3. YouTube to Text
@app.route("/transcribe/youtube", methods=["POST"])
def transcribe_youtube():
    data = request.json
    url = data["url"]

    # Download audio from YouTube
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "wav"}],
        "outtmpl": "temp/%(id)s.%(ext)s",
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        audio_path = f"temp/{info['id']}.wav"

    # Transcribe using Whisper
    result = model.transcribe(audio_path)
    os.remove(audio_path)

    return jsonify({"transcription": result["text"]})


# Real-time Transcription via WebSockets
@socketio.on("audio_chunk")
def handle_audio_chunk(data):
    try:
        if len(data) == 0:
            raise ValueError("Received empty audio data")

        # Convert ArrayBuffer to NumPy array and normalize
        audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

        if audio_np.size == 0:
            raise ValueError("Audio buffer is empty")

        # Write the audio data to a temporary file
        temp_audio_path = "temp/temp_audio.wav"
        sf.write(temp_audio_path, audio_np, 16000)  # 16kHz sample rate

        # Transcribe using Whisper
        result = model.transcribe(temp_audio_path)
        transcription = result["text"]

        # Send transcription back to the frontend
        emit("transcription", {"text": transcription})

    except Exception as e:
        emit("error", {"message": str(e)})


# 4. Real-Time Transcription (Deepgram WebSocket API)
@app.route("/transcribe/realtime", methods=["POST"])
def realtime_transcription():
    try:
        data = request.get_json()
        audio_url = data.get("audio_url")

        if not audio_url:
            return jsonify({"error": "No audio URL provided"}), 400

        response = dg_client.transcription.sync_prerecorded(
            {"url": audio_url}, {"punctuate": True, "language": "en"}
        )

        transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        return jsonify({"transcription": transcript})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 5. Text to Speech
@app.route("/text-to-speech", methods=["POST"])
def text_to_speech():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    tts = gTTS(text)
    tts.save("temp/output.mp3")

    return jsonify({"audio_url": "/temp/output.mp3"})


# ✅ Correct way to run Flask with WebSockets
if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
