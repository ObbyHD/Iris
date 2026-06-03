# Iris — Voice Assistant

Offline-Wake-Word Voice Assistant. Hört per Vosk auf das Codewort "Iris", nimmt Sprache auf, schickt sie an OpenAI GPT-3.5 und gibt die Antwort per TTS aus. Antworten kurz und freundlich.

## Stack
Python 3.x — `openai`, `vosk`, `pyaudio`, `pydub`, `python-dotenv`

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install openai vosk pyaudio pydub python-dotenv
```

Vosk Sprachmodell separat laden: https://alphacephei.com/vosk/models — `vosk-model-small-en-us-0.15` in den Projektordner entpacken.

```bash
python Iris.py
```

## Env
Eigene `.env` mit `OPENAI_API_KEY=sk-...` (siehe `.env.example`).

## Hinweis
Vosk-Modell (~40MB) ist nicht im Repo — extern laden.
