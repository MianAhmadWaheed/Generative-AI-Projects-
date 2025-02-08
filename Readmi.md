# 📜 ShaayarBot 🤖  AI Poetry Generator (Roman Urdu)

Welcome to the **AI Poetry Generator**! 🌟 This FastAPI-based web application generates beautiful Roman Urdu poetry using a trained deep learning model. It is built with **TensorFlow**, **FastAPI**, and **Jinja2** for an interactive UI. 📝✨

---

# Overview 🚀
<img width="632" alt="AI P2 1" src="https://github.com/user-attachments/assets/db2aa8c0-e223-4b1a-805b-1a4bae9c0b66" />
<img width="619" alt="AI P2 2" src="https://github.com/user-attachments/assets/19721708-11f8-4a94-9582-db19b967b767" />

---


## 🚀 Features
- 🎤 **Generate Roman Urdu poetry** based on a seed text.
- 🧠 **LSTM-based deep learning model** for text generation.
- 🌐 **FastAPI backend** with a simple web-based UI.
- 📂 **Uses Rekhta dataset** for poetry training.

---

## 📦 Installation

### 1️⃣ Clone the Repository
```sh
 git clone https://github.com/yourusername/ai-poetry-generator.git
 cd ai-poetry-generator
```

### 2️⃣ Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Run the FastAPI Server
```sh
uvicorn app:app --reload
```

The server will start at: `http://127.0.0.1:8000/` 🌍

---

## 🏗 Project Structure
```
├── poetry_model/              # Trained model & character mappings
│   ├── roman_urdu_poetry_model.keras
│   ├── char2idx.json
│   ├── idx2char.npy
│
├── data/
│   ├── dataset.txt            # Poetry dataset
│
├── templates/
│   ├── index.html             # Web UI for input & output
│
├── app.py                     # FastAPI backend & model integration
├── requirements.txt            # Dependencies
└── README.md                   # Project documentation
```

---

## 🎭 Usage

### 1️⃣ Open the Web Interface
Once the server is running, go to:
```
http://127.0.0.1:8000/
```

### 2️⃣ Enter a Seed Text
- Type any **starting words** in the input box.
- Click on **Generate Poetry** ✨
- The model will generate poetry based on your input!

---

## 🛠 API Endpoints

### 🔹 Generate Poetry (POST `/generate`)
**Request:**
```sh
curl -X POST "http://127.0.0.1:8000/generate" \
     -d "seed_text=Mohabbat ek aisi cheez hai" \
     -d "length=100" \
     -d "temperature=0.8"
```

**Response:**
```json
{
  "poetry": "Mohabbat ek aisi cheez hai jo dil ke kareeb rehti hai..."
}
```

---

## 📚 Model Details
- **Architecture:** LSTM-based text generation model 🧠
- **Training Data:** Rekhta poetry dataset 📖
- **Vocabulary Size:** Dependent on dataset
- **Loss Function:** Sparse Categorical Crossentropy

---

## 🤝 Contributing
Pull requests are welcome! Feel free to open an issue if you have suggestions.

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 🌟 Credits
- Developed by **Muhammad Ahmad Waheed** 🚀
- Dataset Source: **Rekhta.org** 🏛️

🔹 _Enjoy generating beautiful Roman Urdu poetry!_ ✨
