import os
import json
from openai import OpenAI
import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play
from pathlib import Path
import re
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv
import time
import threading
import random
import playsound

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

# Load Vosk-Modell
vosk_model_path = ".\vosk-model-small-en-us-0.15"  # Change Path Vosk File
model = Model(vosk_model_path)
recognizer = KaldiRecognizer(model, 16000)

def get_completion(prompt):
    rawresponse = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Du bist ein freundlicher und hilfsbereiter Assistent, der ähnlich wie ein bester Freund agiert. Deine Antworten sind seehr kurz, prägnant und auf den Punkt gebracht, es sei denn, der Benutzer bittet um mehr Details oder eine ausführliche Erklärung. Du antwortest freundlich, aber vermeidest unnötige Wörter. Fokus liegt auf Effizienz und Klarheit. Wenn der Benutzer dich um längere oder detailliertere Antworten bittet, gehst du ausführlich darauf ein. Du hilfst bei alltäglichen Aufgaben, wie z. B. das Wetter zu prüfen oder andere einfache Anfragen schnell zu erledigen. Sei immer positiv, aber nicht übermäßig förmlich. Bleibe natürlich im Ton, wie ein guter Freund, der jederzeit hilfsbereit ist. Stelle sicher, dass deine Antworten an den Kontext angepasst sind. Antworte ausschließlich in Englisch oder Deutsch."}, 
                  {"role": "user", "content": prompt}]
    )
    response = rawresponse.choices[0].message.content
    print(response)
    return response

os.system('cls' if os.name == 'nt' else 'clear')

# Boolean = False
is_recording = False
stop_transcription = False 

def listen_for_keyword():
    global is_recording
    print("Warten auf das Codewort 'Iris'...")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()

    while True:
        data = stream.read(1024)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            text = result_dict['text']
            print(f"Erkannt: {text}")

            # Boolean = true
            if "iris" in text.lower():
                print("Starting to record...")
                is_recording = True
                break

    stream.stop_stream()
    stream.close()
    p.terminate()

def save_temp_wav(frames, filename="temp_output.wav"):
    # temporary wav file
    p = pyaudio.PyAudio()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

def record_audio_IRT():
    global is_recording, stop_transcription
    filename = "output.wav"
    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sample_rate = 44100
    p = pyaudio.PyAudio()

    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)

    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []
    print("Aufnahme läuft...")
    if random(1,100) == 69:
        playsound("/sound/bing.mp3")
    else:
        playsound("/sound/bing.mp3")

    silence_duration = 5 # sleep 1 sec
    last_speech_time = time.time()

    def transcribe_IRT():
        global is_recording, stop_transcription
        while is_recording and not stop_transcription:
            try:
                save_temp_wav(frames, "temp_output.wav")

                with open("temp_output.wav", "rb") as audio_file:
                    transcribed_text = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="text"
                    )
                    print(f"Transkription: {transcribed_text}")
            except Exception as e:
                if "audio_too_short" in str(e):
                    # Ignore Error
                    pass
                else:
                    print(f"Fehler bei der Echtzeit-Transkription: {e}")
            time.sleep(0.25)  

    transcription_thread = threading.Thread(target=transcribe_IRT)
    transcription_thread.start()

    try:
        while is_recording:
            data = stream.read(chunk)
            frames.append(data)

            # Spracherkennung
            if recognizer.AcceptWaveform(data):
                if json.loads(recognizer.Result())['text'] != '':
                    last_speech_time = time.time()  # reset sleep timer
                    silence_duration = 1.5 # set silence duration to lower number

            # Stop transkription recording if no voice detected
            if last_speech_time < time.time() - silence_duration:
                print("Keine Sprache erkannt. Aufnahme wird beendet.")
                stop_transcription = True 
                if random(1,100) == 69:
                    playsound("/sound/gnib.mp3")
                else:
                    playsound("/sound/gnib.mp3")
                break
    except KeyboardInterrupt:
        pass

    is_recording = False
    transcription_thread.join() 

    # Stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save WAV file
    wf.writeframes(b"".join(frames))
    wf.close()

    return filename

while True:
    listen_for_keyword()

    if is_recording:
        audio_file_path = record_audio_IRT()

        # Transcribe audio
        with open(audio_file_path, "rb") as audio_file:
            prompt = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text"
            )
        
        print(f"Transkription: {prompt}")

        response = get_completion(prompt)

        # Save to temporary directory
        temp_dir = Path.home() / "temp"
        temp_dir.mkdir(exist_ok=True)
        output_path = temp_dir / "outputiris.mp3"
        
        # TTS output
        audioresponse = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=response
        )

        with open(output_path, "wb") as out_file:
            out_file.write(audioresponse.content)

        # Play MP3
        mp3_file = AudioSegment.from_mp3(output_path)
        play(mp3_file)
        os.remove("output.wav")
        print('\n')
 