from openai import OpenAI
import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play
import os
from pathlib import Path
import re
import keyboard

OPENAI_API_KEY = '***REVOKED-KEY***'
client = OpenAI(api_key=OPENAI_API_KEY)

def get_completion(prompt):
    rawresponse = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": "Du bist ein freundlicher und hilfsbereiter Assistent, der ähnlich wie ein bester Freund agiert. Deine Antworten sind kurz, prägnant und auf den Punkt, es sei denn, der Benutzer bittet um mehr Details oder eine ausführliche Erklärung. Du antwortest freundlich, aber vermeidest unnötige Wörter. Fokus liegt auf Effizienz und Klarheit. Wenn der Benutzer dich um längere oder detailliertere Antworten bittet, gehst duausführlich darauf ein. Du hilfst bei alltäglichen Aufgaben, wie z. B. das Wetter zu prüfen oder andereeinfache Anfragen schnell zu erledigen. Sei immer positiv, aber nicht übermäßig förmlich. Bleibe natürlich im Ton,wie ein guter Freund, der jederzeit hilfsbereit ist. Stelle sicher, dass deine Antworten an den Kontext angepasst sind."}, {"role": "user", "content": prompt}]
    )
    msgresponse = bytes(rawresponse.choices[0].message.content, 'utf-8')
    response = str(msgresponse, encoding='utf-8', errors='strict')
    print(response)
    return(response)

os.system('cls' if os.name == 'nt' else 'clear')

while(True):
    input('Hold "Enter" to record...')

    filename = "output.wav"
    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sample_rate = 44100
    p = pyaudio.PyAudio()
    wf = wave.open("output.wav", "wb")
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
    data = stream.read(chunk)
    while(True):
        if(keyboard.is_pressed("Enter")):
            print('Started recording.')
            while(True):
                if(keyboard.is_pressed("enter")):
                    data = stream.read(chunk)
                    frames.append(data)
                    stream.write(data)
                else:
                    break
            print('Finished recording.')
            break
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.writeframes(b"".join(frames))
    wf.close()

    audio_file = open("output.wav", "rb")
    prompt = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="text"
    )
    print(prompt)

    response = get_completion(prompt)

    output_path = Path(__file__).parent / "output.mp3"
    audioresponse = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=response
    )

    audioresponse.stream_to_file(output_path)

    mp3_file = AudioSegment.from_mp3("outputiris.mp3")
    play(mp3_file)
    print('\n')
    