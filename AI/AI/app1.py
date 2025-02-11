import gradio as gr
import whisper
from deepgram import Deepgram
import yt_dlp as youtube_dl
from gtts import gTTS
import os
import subprocess
import uuid
from libretranslatepy import LibreTranslateAPI

# Load Whisper Model
model = whisper.load_model("base")

# Deepgram API Key
DEEPGRAM_API_KEY = "c6405ba98eef90bdc74edd6b1ff9a03fb3752373"
dg_client = Deepgram(DEEPGRAM_API_KEY)

# LibreTranslate API
lt = LibreTranslateAPI("https://libretranslate.de")


def transcribe_audio(file, target_lang):
    result = model.transcribe(file)
    text = result["text"]
    if target_lang != "original":
        text = lt.translate(text, "auto", target_lang)
    return text


def transcribe_video(file, target_lang):
    audio_path = "temp_audio.wav"
    subprocess.run(["ffmpeg", "-i", file.name, "-q:a", "0", "-map", "a", audio_path], check=True)
    result = model.transcribe(audio_path)
    os.remove(audio_path)
    text = result["text"]
    if target_lang != "original":
        text = lt.translate(text, "auto", target_lang)
    return text


def transcribe_youtube(url, target_lang):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "wav"}],
        "outtmpl": "temp/%(id)s.%(ext)s",
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        audio_path = f"temp/{info['id']}.wav"
    result = model.transcribe(audio_path)
    os.remove(audio_path)
    text = result["text"]
    if target_lang != "original":
        text = lt.translate(text, "auto", target_lang)
    return text


def text_to_speech(text, lang, target_lang):
    if target_lang != "original":
        text = lt.translate(text, "auto", target_lang)
    tts = gTTS(text, lang=lang)
    audio_path = "temp_tts.mp3"
    tts.save(audio_path)
    return audio_path


def translate_text(text, source_lang, target_lang):
    return lt.translate(text, source_lang, target_lang)


with gr.Blocks() as app:
    gr.Markdown(
        """
        <h1 style="text-align: center;">🎤 AuraSpeak</h1>
        <h3 style="text-align: center; color: gray;">Emphasizing a seamless and natural AI-powered speech system.</h3>
        """
    )
    with gr.Tabs():
        with gr.Tab("🎧 Audio to Text"):
            audio_input = gr.Audio(type="filepath")
            target_lang_audio = gr.Dropdown(choices=["original", "en", "ur", "fr", "es"], label="Translate To")
            audio_output = gr.Textbox(label="Transcription")
            gr.Button("Transcribe").click(transcribe_audio, inputs=[audio_input, target_lang_audio], outputs=audio_output)

        with gr.Tab("📹 Video to Text"):
            video_input = gr.File()
            target_lang_video = gr.Dropdown(choices=["original", "en", "ur", "fr", "es"], label="Translate To")
            video_output = gr.Textbox(label="Transcription")
            gr.Button("Transcribe").click(transcribe_video, inputs=[video_input, target_lang_video], outputs=video_output)

        with gr.Tab("🎬 YouTube to Text"):
            youtube_input = gr.Textbox(label="YouTube URL")
            target_lang_youtube = gr.Dropdown(choices=["original", "en", "ur", "fr", "es"], label="Translate To")
            youtube_output = gr.Textbox(label="Transcription")
            gr.Button("Transcribe").click(transcribe_youtube, inputs=[youtube_input, target_lang_youtube], outputs=youtube_output)

        with gr.Tab("🔊 Text to Speech"):
            tts_text = gr.Textbox(label="Enter Text")
            tts_lang = gr.Dropdown(choices=["en", "ur", "fr", "es"], label="Select Language for Speech")
            tts_target_lang = gr.Dropdown(choices=["original", "en", "ur", "fr", "es"], label="Translate To Before Speech")
            tts_output = gr.Audio(label="Generated Speech")
            gr.Button("Convert").click(text_to_speech, inputs=[tts_text, tts_lang, tts_target_lang], outputs=tts_output)

        with gr.Tab("🌍 Translate Text"):
            trans_input = gr.Textbox(label="Enter Text")
            source_lang = gr.Dropdown(choices=["auto", "en", "ur", "fr", "es"], label="Source Language")
            target_lang = gr.Dropdown(choices=["en", "ur", "fr", "es"], label="Target Language")
            trans_output = gr.Textbox(label="Translated Text")
            gr.Button("Translate").click(translate_text, inputs=[trans_input, source_lang, target_lang], outputs=trans_output)

app.launch(share=True)
