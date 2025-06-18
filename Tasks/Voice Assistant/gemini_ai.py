from google import genai
import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path='./Tasks/Voice Assistant/config.env')

key = os.getenv('Gemini_api')
client = genai.Client(api_key=key)

chat = client.chats.create(model='gemini-2.0-flash')

while True:
    message = input('You: ')
    if message.lower() == 'bye':
        print('Chatbot: Alright, have a nice day or night')
        break
    response = chat.send_message(message = message)
    print("Chatbot: ", response.text)