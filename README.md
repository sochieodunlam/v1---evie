# Voice Chat Demo (VOSK + OpenAI)

A small demo that listens to your mic, transcribes speech with **VOSK**, sends it to **OpenAI ChatGPT**, and then plays back a generated voice response using OpenAI's **TTS**.

## ✅ What it does
- Listens to your microphone in real time
- Uses a local VOSK model to convert speech → text
- Sends the text to OpenAI GPT (chat completion)
- Generates spoken audio (MP3) from GPT's reply
- Plays the MP3 using macOS `afplay`

## 🧩 Prerequisites
- macOS (uses `afplay` to play audio)
- Python 3.13 (a venv is included in `v1/`)
- An OpenAI API key
- The VOSK model directory: `vosk-model-small-en-us-0.15/`

## ⚙️ Setup
1. Copy your OpenAI key into a `.env` file in the repo root:
   ```
   OPENAI_API_KEY=your_key_here
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Run
```bash
python speak.py
```

Then speak into your microphone. The script will show the recognized text and play back the generated response.

## 🔎 Notes
- The prompt in `speak.py` is intentionally "evil" for a video / demo; you can change it in `get_response()`.
- The VOSK model directory must be named `vosk-model-small-en-us-0.15` (as used in the script).
- This project is a simple demo and not meant for production use.
