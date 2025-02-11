# AURASPEAK -- AI Multitask Platform

## 🚀 Overview

<img width="946" alt="W-1" src="https://github.com/user-attachments/assets/4552fe4e-cb54-4f18-ad14-4babba9bf752" />


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

The server will start at: [http://127.0.0.1:7860](http://127.0.0.1:7860)
* Running on public URL: https://2f753fc62d32b935e1.gradio.live


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
<img width="929" alt="W-2" src="https://github.com/user-attachments/assets/b11ac4f6-d0be-45ae-b19e-9984630d0574" />
<img width="919" alt="W-3" src="https://github.com/user-attachments/assets/b8ef6540-947e-43fc-a5e4-f4c2f2a5fd95" />
<img width="902" alt="W-4" src="https://github.com/user-attachments/assets/65e2111b-f4d9-47e4-898a-0cf4d57073d6" />

## 📜 License
This project is licensed under the MIT License.

## 👨‍💻 Author
- **Muhammad Ahmad Waheed**  
  📧 Email: [aw6065209@gmail.com]()

## ⭐ Contribute & Support
If you like this project, please ⭐ star this repository and contribute!




