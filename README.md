# Iris - Voice Assistant

Offline wakeword voice assistant. Listens for the keyword "Iris" via Vosk, records speech, sends it to OpenAI GPT-3.5 and replies via TTS. Responses are kept short and friendly.

## Stack
Python 3.x   `openai`, `vosk`, `pyaudio`, `pydub`, `python-dotenv`

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install openai vosk pyaudio pydub python-dotenv
```

Download the Vosk speech model separately: https://alphacephei.com/vosk/models; extract `vosk-model-small-en-us-0.15` into the project folder.

```bash
python Iris.py
```

## Env
Needs your own `.env` with `OPENAI_API_KEY=sk-...` (see `.env.example`).

## Note
Vosk model (~40 MB) is not in the repo, download it externally.
