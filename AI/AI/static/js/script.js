document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".tab-button");
    const sections = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            sections.forEach(sec => sec.classList.remove("active"));

            tab.classList.add("active");
            document.getElementById(tab.dataset.tab).classList.add("active");
        });
    });
});

// Function for audio transcription
document.getElementById("transcribeAudio").addEventListener("click", async () => {
    const file = document.getElementById("audioFile").files[0];
    if (!file) return alert("Select an audio file.");

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/transcribe/audio", {
        method: "POST",
        body: formData,
    });

    const result = await response.json();
    document.getElementById("audioResult").innerText = result.transcription;
});

// Function for video transcription
document.getElementById("transcribeVideo").addEventListener("click", async () => {
    const file = document.getElementById("videoFile").files[0];
    if (!file) return alert("Select a video file.");

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/transcribe/video", {
        method: "POST",
        body: formData,
    });

    const result = await response.json();
    document.getElementById("videoResult").innerText = result.transcription;
});

// Function for YouTube transcription
document.getElementById("transcribeYouTube").addEventListener("click", async () => {
    const url = document.getElementById("youtubeLink").value;
    if (!url) return alert("Enter a YouTube URL.");

    const response = await fetch("/transcribe/youtube", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
    });

    const result = await response.json();
    document.getElementById("youtubeResult").innerText = result.transcription;
});

// Text-to-Speech
document.getElementById("convertToSpeech").addEventListener("click", () => {
    const text = document.getElementById("textToSpeech").value;
    if (!text) return alert("Enter text.");

    const speech = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(speech);
});

// Real-Time Transcription (WebSocket)
let socket = io.connect("http://localhost:5000");
let mediaRecorder;
let isRecording = false;

document.getElementById("startRealtime").addEventListener("click", async () => {
    if (!navigator.mediaDevices.getUserMedia) {
        alert("Your browser does not support audio recording.");
        return;
    }

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    isRecording = true;

    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0 && isRecording) {
            let reader = new FileReader();
            reader.onloadend = function () {
                let audioBuffer = reader.result;

                // Check the length of the buffer and adjust if needed
                let bufferLength = audioBuffer.byteLength;
                if (bufferLength % 2 !== 0) {
                    // Ensure buffer length is a multiple of element size
                    let adjustedBuffer = new ArrayBuffer(bufferLength + 1); // Add 1 byte to make it valid
                    let view = new DataView(adjustedBuffer);
                    new Uint8Array(adjustedBuffer).set(new Uint8Array(audioBuffer));
                    audioBuffer = adjustedBuffer;
                }

                socket.emit("audio_chunk", audioBuffer);
            };
            reader.readAsArrayBuffer(event.data);
        }
    };

    mediaRecorder.start(5000); // Send chunks every 500ms
});


document.getElementById("stopRealtime").addEventListener("click", () => {
    if (mediaRecorder) {
        isRecording = false;
        mediaRecorder.stop();
    }
});

socket.on("transcription", (data) => {
    document.getElementById("realtimeResult").innerText += data.text + " ";
});

socket.on("error", (data) => {
    console.error("Error:", data.message);
});
