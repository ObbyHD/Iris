import os
import openai # type: ignore
from openai import OpenAI
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
    system_behavior = "Du bist eine Person, die einem Freund erklärt, wie man sich im Kino verhalten soll."
    
    # Benutzer-Prompt (Frage oder Thema)
    user_prompt = input
    
    # Anfrage an GPT-4 senden und Antwort anzeigen
    response = create_chat_completion(system_prompt=system_behavior, user_prompt=user_prompt)
    print("\nGPT-4 Antwort:\n", response)

if __name__ == "__main__":
    main()
