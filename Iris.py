import os
import openai # type: ignore
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# API-Key aus .env
openai.api_key = os.getenv('OPENAI_API_KEY')

def create_chat_completion(system_prompt, user_prompt, model="gpt-4", temperature=0.3, max_tokens=500):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        # Extrahiere die erste Antwort des Modells
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        # Fehlerbehandlung, falls API fehlschlägt
        return f"Error: {str(e)}"

def main():
    
    # Rolle die GPT-4 übernehmen soll
    system_behavior = " Du bist ein freundlicher und hilfsbereiter Assistent, der ähnlich wie ein bester Freund agiert. Deine Antworten sind kurz, prägnant und auf den Punkt, es sei denn, der Benutzer bittet um mehr Details oder eine ausführliche Erklärung. Du antwortest freundlich, aber vermeidest unnötige Wörter. Fokus liegt auf Effizienz und Klarheit. Wenn der Benutzer dich um längere oder detailliertere Antworten bittet, gehst du ausführlich darauf ein. Du hilfst bei alltäglichen Aufgaben, wie z. B. das Wetter zu prüfen oder andere einfache Anfragen schnell zu erledigen. Sei immer positiv, aber nicht übermäßig förmlich. Bleibe natürlich im Ton, wie ein guter Freund, der jederzeit hilfsbereit ist. Stelle sicher, dass deine Antworten an den Kontext angepasst sind und flexibel reagieren können."
 
    # Benutzer-Prompt (Frage oder Thema)
    user_prompt = input ("Deine Frage an GPT-4: ")
    
    # Anfrage an GPT-4 senden und Antwort anzeigen
    response = create_chat_completion(system_prompt=system_behavior, user_prompt=user_prompt)
    print("\nGPT-4 Antwort:\n", response)

if __name__ == "__main__":
    main()
