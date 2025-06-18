from google import genai
from google.genai import types
from dotenv import load_dotenv

import pyttsx3
import time
import os
import traceback

load_dotenv(dotenv_path='./Tasks/Voice Assistant/config.env')

# --- Configuration ---
API_KEY = os.getenv('Gemini_api')
MODEL_NAME = "gemini-2.0-flash"

# --- Initialization ---
client = genai.Client(api_key=API_KEY)
chat = client.chats.create(model=MODEL_NAME)
engine = pyttsx3.init()


def generate_response(text: str) -> str:
    time.sleep(2)
    """
    Generate a response from the Gemini model given a user prompt.
    """
    print(f"\nUser: {text}")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction='You are AI customer support for eMigr8' +
                'eMigr8 is a tech‑enabled visa support platform (by Bincom ICT) that helps tech professionals and entrepreneurs relocate to top destinations (UK, US, Canada, Germany, France, Australia, New Zealand, Hong Kong, etc.)',
                max_output_tokens=100
            )
        )
        ai_response = response.text.strip()
        print(f"Assistant: {ai_response}")
        return ai_response

    except Exception as e:
        print("Error in generate_response:", e)
        traceback.print_exc()
        return "I'm sorry, but I couldn't generate a response due to an error."


def tts(text: str) -> None:
    try:
        clean_text = text.replace('*', '')
        engine.say(clean_text)
        engine.save_to_file(clean_text, 'output.wav')
        engine.runAndWait()
        time.sleep(3)
    except Exception as e:
        print("Error in text_to_speech:", e)
        traceback.print_exc()
