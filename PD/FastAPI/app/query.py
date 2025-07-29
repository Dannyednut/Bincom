import requests

def get_response(prompt: str):
    url = f"http://127.0.0.1:8000/chat/"
    response = requests.post(url, json={"prompt": prompt})
    if response.status_code == 200:
        print(response.json())
    else:
        print({"error": "Failed to get response from the server"})

print()    
# get_response("Hey, I'm a python developer. what is the weather safety status for Murtala Muhammed airport, icao is DNMM")

def req():
    url = f"https://aviationweather.gov/api/data/metar?ids=KLAX&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        print("response:", response.json())
    else:
        print({"error": "Failed to get response from the server"})

req()