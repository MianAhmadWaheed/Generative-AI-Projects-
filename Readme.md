# AI Multitask Platform

## 🚀 Overview
<img width="956" alt="AI 1" src="https://github.com/user-attachments/assets/6711da57-de6d-4e81-af83-6fc70a1ffa5a" />
<img width="935" alt="YT 1" src="https://github.com/user-attachments/assets/d71a1769-bf6a-4ac2-adb8-7ac8770d11f8" />


The **AI Multitask Platform** is an advanced speech processing and transcription system built with Python and Flask. It supports multiple AI-driven tasks, including:

- 🎙 **Audio to Text** (Speech-to-Text)
- 📹 **Video to Text** (Extract and transcribe speech from video files)
- 🔗 **YouTube Link to Text** (Download and transcribe audio from YouTube videos)
- 🗣 **Real-Time Voice to Text** (WebSocket-based live transcription)
- 🔊 **Text to Speech** (Convert text into speech audio)

## 🛠 Technologies Used
- **Python** (Flask, Whisper, Deepgram, gTTS, NumPy, etc.)
- **Flask** (Backend Framework)
- **Whisper AI** (Speech Recognition Model)
- **Deepgram API** (Real-time transcription)
- **Socket.IO** (For real-time communication)
- **YouTube-DL** (To extract audio from YouTube videos)
- **FFmpeg** (For audio processing)
- **gTTS** (Text-to-Speech Conversion)
- **Waitress** (Production-ready WSGI Server)

## 📌 Features
### 🎤 Audio to Text
Upload an audio file to get a text transcription.

### 🎞 Video to Text
Extracts and transcribes the speech from an uploaded video file.

### 🔗 YouTube Link to Text
Provide a YouTube link, and the system will extract and transcribe the audio.

### ⏳ Real-Time Voice to Text
Live transcription using WebSockets.

### 🗣 Text to Speech
Enter text, and the system will generate speech output.

## 🖥 Installation & Setup
### 🔹 Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- FFmpeg (Add it to system PATH)
- Virtual Environment (Recommended)

### 🔹 Clone the Repository
```bash
$ git clone https://github.com/your-repo/AI-Multitask-Platform.git
$ cd AI-Multitask-Platform
```

### 🔹 Create & Activate Virtual Environment
```bash
$ python -m venv whisper-env
$ source whisper-env/bin/activate   # On macOS/Linux
$ whisper-env\Scripts\activate      # On Windows
```

### 🔹 Install Dependencies
```bash
$ pip install -r requirements.txt
```

### 🔹 Run the Application
```bash
$ python app.py
```

The server will start at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🎯 API Endpoints
### 📢 Transcribe Audio
```http
POST /transcribe/audio
```
- Upload an audio file for transcription.

### 🎥 Transcribe Video
```http
POST /transcribe/video
```
- Upload a video file, and it will extract and transcribe speech.

### 🔗 Transcribe YouTube Video
```http
POST /transcribe/youtube
```
- Provide a YouTube video link to extract and transcribe its audio.

### ⏳ Real-Time Voice to Text
```http
WebSocket Connection: /transcribe/realtime
```
- Stream audio for real-time speech-to-text conversion.

### 🗣 Text to Speech
```http
POST /text-to-speech
```
- Convert input text to an audio file.

## 📷 Screenshots
<img src="docs/screenshot1.png" width="600" alt="Audio to Text Demo">
<img src="docs/screenshot2.png" width="600" alt="YouTube to Text Demo">

## 📜 License
This project is licensed under the MIT License.

## 👨‍💻 Author
- **Muhammad Ahmad Waheed**  
  📧 Email: [aw6065209@gmail.com]()

## ⭐ Contribute & Support
If you like this project, please ⭐ star this repository and contribute!




