# Gemini Function Call

This project provides a modular, AI-powered agent that utilizes **Google Gemini's function calling**, external APIs (e.g. OpenWeather, AviationWeather), and a local mock database to process natural language prompts and return context-aware responses.

It supports real-time weather queries, aviation METAR reports, geocoding, and capturing user profession.

---

## Features

- **Get current weather** by city name or coordinates  
- **Weather forecast** (5-day) for coordinates  
- **METAR aviation reports** by ICAO airport code  
- **Convert city names to lat/lon**  
- **Capture and store user profession**    
- Seamlessly integrates with **Gemini 2.0 Flash** model and tools API

---

## File Structure

```text
functionCall.py         # Main agent class using Gemini tools
config.env              # Environment file with Gemini API Key
database.json           # JSON DB to store user data (username → profession)
```

---

## Setup

1. **Install Dependencies**

```bash
pip install google-generativeai python-dotenv requests
```

2. **Environment Variables**

Create a file called `config.env` in the root or `Tasks/Voice Assistant/` directory with:

```
Gemini_API=your_gemini_api_key_here
Rapid_API_Key=your_own_rapidapi_key_here
```

3. **RapidAPI (Weather)**

Weather data uses [OpenWeather13 API on RapidAPI](https://rapidapi.com/weatherapi/api/open-weather13).

---

## How It Works

- Prompts are sent to Gemini using the `chat.send_message()` method.
- If Gemini detects a function call (e.g., `get_weather_by_city`), it triggers an associated Python method.
- Responses are returned either as:
  - A dictionary mapping result types (`"weather"`, `"profession"`, etc.)
  - Or error details if something fails.

---

## Supported Functions

| Function Name | Description |
|---------------|-------------|
| `get_weather_by_city` | Fetch current weather for a city |
| `get_weather_by_latitude_and_longitude` | Current weather by coordinates |
| `get_weather_forecast` | 5-day forecast by coordinates |
| `aviation_weather_center` | METAR report for ICAO-coded airport |
| `store_user_profession` | Stores user profession in JSON DB |
| `get_profession_from_prompt` | Extracts profession from casual prompts |
| `get_lat_long_from_city` | Converts city name to lat/lon |

---

## Example Usage

```python
from functionCall import Agent

ai = Agent()

while True:
    prompt = input("You: ")
    if prompt.lower() == "quit":
        print("Chatbot: Goodbye!")
        break
    response = ai.response(prompt)
    print("Chatbot:", response)
```

---

## Sample Prompt Inputs

```text
"What's the weather in Paris right now?"
"Show me METAR for KLAX."
"I'm a mechanical engineer named James."
"What's the forecast for 37.77, -122.41?"
```

---

## Notes

- Uses Gemini's `tools` and `function_response` mechanism for structured interaction.
- Local DB is a simple `database.json` file and non essential—can be swapped with a real DB (e.g., SQLite) if found useful.
- Geocoding function (`get_lat_long_from_city`) is defined but not added to `tools` list yet.

---

## Error Handling

If Gemini or the external APIs fail, `response()` returns a dictionary with:

```json
{
  "error": "ExceptionType",
  "msg": "Description of the issue"
}
```

---

## License

This project is open-source and available for use or extension under the MIT License.