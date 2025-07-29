from google import genai
from google.genai.types import (
    FunctionDeclaration, 
    Tool, Part, Content, 
    GenerateContentConfig
)

import os
import ast
import json
import requests

from dotenv import load_dotenv
from google.api_core import exceptions as api_exception

load_dotenv(dotenv_path='config.env')

API_KEY = os.getenv('Gemini_API')
RAPID_API_KEY = os.getenv('Rapid_API_Key')

class Agent:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)


        # Function for current weather in a city
        self.get_weather_by_city = FunctionDeclaration(
            name="get_weather_by_city",
            description=
                "Retrieves the current, real-time weather conditions for a specified city or province. "
                "This includes details like temperature, humidity, wind speed, and general conditions. "
                "Use this function when the user asks for the 'current weather', 'weather now', or 'what's the weather like' "
                "for a specific named location.",
            parameters={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": (
                            "The full, unabbreviated name of the city or province for which current weather "
                            "information is requested. For example, use 'California' not 'CA', or 'New York City' not 'NYC'."
                        ),
                    },
                },
                "required": ["city"],
            },
        )

        # Function for current weather by coordinates
        self.get_weather_by_lat_long = FunctionDeclaration(
            name="get_weather_by_latitude_and_longitude",
            description=
                "Obtains the current weather conditions for a precise geographical location "
                "defined by its latitude and longitude coordinates. "
                "This is suitable when the user explicitly provides coordinates, or when coordinates "
                "have been previously determined for a location (e.g., via a geocoding service).",
            parameters={
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "string", # Changed to number for better type hint
                        "description": "The latitude of the location, expressed as a decimal number (e.g., 34.0522).",
                    },
                    "longitude": {
                        "type": "string", # Changed to number for better type hint
                        "description": "The longitude of the location, expressed as a decimal number (e.g., -118.2437).",
                    },
                },
                "required": ["latitude", "longitude"],
            },
        )

        # Function for weather forecast by coordinates
        self.get_weather_forecast = FunctionDeclaration(
            name="get_weather_forecast",
            description=
                "Provides a multi-day or hourly weather forecast for a specific geographical location "
                "identified by its latitude and longitude. "
                "This function is distinct from retrieving current weather and should be used when the user "
                "specifically asks for 'forecast', 'tomorrow's weather', 'weather for next N days', or 'future weather'. "
                "It requires precise geographical coordinates.",
            parameters={
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "string", 
                        "description": "The latitude of the location for which weather forecast information is requested.",
                    },
                    "longitude": {
                        "type": "string", 
                        "description": "The longitude of the location for which weather forecast information is requested.",
                    },
                    
                },
                "required": ["latitude", "longitude"],
            },
        )

        # Function for aviation weather
        self.aviation_weather_center = FunctionDeclaration(
            name="aviation_weather_center",
            description=
                "Generates a standardized Aviation Routine Weather Report (METAR) for a given airport. "
                "This provides critical real-time weather information relevant to aviation, "
                "including wind, visibility, runway visual range, and cloud cover. "
                "Use this exclusively when the user explicitly mentions an 'airport', 'METAR', 'aviation weather', "
                "or asks for weather pertinent to flight operations.",
            parameters={
                "type": "object",
                "properties": {
                    "icao": {
                        "type": "string",
                        "description": (
                            "The four-letter ICAO identifier of the airport (e.g., 'KLAX' for Los Angeles International Airport, "
                            "'LSGG' for Geneva Airport). This ID should be derived by the model from the airport's name, "
                            "or directly provided by the user if they know it. Do not guess; if uncertain, ask the user to clarify."
                        ),
                    },
                },
                "required": ["icao"],
            },
        )

        # Function to store user profession
        self.store_user_profession = FunctionDeclaration(
            name="store_user_profession",
            description=
                "Get the user's stated profession or occupation for personalization or profile management purposes. "
                "Only call this function when the user explicitly identifies their profession and (optionally) their name. "
                "This is not a general data extraction tool; it's specific to capturing user self-identification of their role.",
            parameters={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": (
                            "The explicit username of the user as provided by them (e.g., 'Alice Smith', 'John Doe'). "
                            "Do not infer a name from roles or adjectives like 'developer' or 'manager'."
                        ),
                    },
                    "profession": {
                        "type": "string",
                        "description": "The user's stated profession, occupation, or job title (e.g., 'developer', 'doctor', 'engineer').",
                    },
                },
                "required": ["username","profession"], 
            },
        )


        self.get_profession_from_prompt = FunctionDeclaration(
            name="get_profession_from_prompt",
            description=(
                "Captures and extracts the user's stated profession, occupation, or job title "
                "from their prompt. This function is designed to identify the user's professional role "
                "even if their name is not provided in the same input. "
                "Use this when the user identifies their profession at any position in their prompt even when it's out of context."
                "Crucially, this function should be used even when the user identifies their profession within a prompt primarily "
                "focused on another task or question (i.e., a context switch)."
                "This does not store, but only capture the user profession for later reference"
            ),
            parameters={
                "type": "object",
                "properties": {
                    "profession": {
                        "type": "string",
                        "description": "The user's stated profession, occupation, or job title (e.g., 'developer', 'doctor', 'engineer', 'student').",
                    },
                },
                "required": ["profession"], 
            },
        )

        # Geocoding Function
        self.get_lat_long_from_city = FunctionDeclaration(
            name="get_lat_long_from_city",
            description=
                "Determines the precise geographical latitude and longitude coordinates for a given city name. "
                "This function is crucial for converting human-readable city names into the numerical "
                "coordinates required by other location-based services like weather forecasts. "
                "Use this when coordinates are needed but only a city name is available. "
                "Prioritize exact city names to avoid ambiguity (e.g., 'Paris, France' vs. 'Paris, Texas').",
            parameters={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The full name of the city for which coordinates are requested. Include country or state if ambiguous.",
                    }
                },
                "required": ["city"],
            },
        )


        self.tools = Tool(function_declarations=[
            self.get_weather_by_city, 
            self.get_weather_by_lat_long, 
            self.get_weather_forecast,
            self.aviation_weather_center, 
            self.store_user_profession,
            self.get_profession_from_prompt,
            self.get_lat_long_from_city
        ])

        self.chat = self.client.chats.create(
            model='gemini-2.0-flash',
            config=GenerateContentConfig(
                temperature=0,
                system_instruction="You are a regular AI assistant that performs the functions defined in the your tools "\
                "But not restricted to your tools only. If you should also look up informations needed.",
                tools=[self.tools],
                # max_output_tokens=100,
            )
        )

        self.data_map = {
            "get_profession_from_prompt": "profession",
            "get_weather_by_city": "weather",
            "aviation_weather_center":"weather",
            "store_user_profession": "profession"
        }

    def get_weather(self, city: str = None, lat: str = None, long: str = None, forecast: bool = False):
        if city:
            url = "https://open-weather13.p.rapidapi.com/city" 
        elif not city and lat:
            url = "https://open-weather13.p.rapidapi.com/latlon"
        elif lat and forecast:
            url = "https://open-weather13.p.rapidapi.com/fivedaysforcast"

        querystring = {"city":city,"lang":"EN"} if city else {"latitude":lat,"longitude":long,"lang":"EN"}

        headers = {
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "open-weather13.p.rapidapi.com"
        } 

        response = requests.get(url, headers=headers, params=querystring)

        return response.json()

    import requests

    def metar_report(self, icao: str):
        url = f"https://aviationweather.gov/api/data/metar?ids={icao}&format=json"
        d = requests.get(url)
        d = d.json()
        l = ["metar_id","icaoId","receiptTime","obsTime","reportTime","metarType", "rawOb"]
        # Iterate over a copy of the keys to avoid RuntimeError
        for i in list(d[0].keys()):
            if not d[0][i] or i in l:
                del d[0][i]
        response = d[0]
        return response


    def store_user_info(self, username: str, occupation: str):
        database = "./Tasks/database.json"
        with open(database, 'r') as file:
            data = json.load(file)
        
        if username in data['users']:
            data['users'][username]['occupation'] = occupation
        else:
            data['users'][username] = {'occupation': occupation}

        with open(database, 'w') as file:
            json.dump(data, file)

        return {"profession": occupation}


    def function_response(self, function_calls: list):
        if not function_calls:
            return None, None
        
        responses = []
        for function_call in function_calls:
            
            if function_call.name == "store_user_profession":
                username, occupation = function_call.args['username'], function_call.args['profession']
                
                part = Part.from_function_response(
                            name=function_call.name,
                            response={
                                    "content": self.store_user_info(username, occupation)['profession']
                            }
                        )
            
            elif function_call.name == "aviation_weather_center":
                icao= function_call.args['icao']
                
                part = Part.from_function_response(
                            name= function_call.name,
                            response={
                                    "content": self.metar_report(icao)
                            }
                        )
                
            elif function_call.name in {
                "get_weather_by_city", 
                "get_weather_forecast", 
                "get_weather_by_latitude_and_longitude"
            }:
                part = Part.from_function_response(
                            name= function_call.name,
                            response={
                                    "content": self.get_weather(
                                        function_call.args['city']
                                    ) if 'city' in function_call.args else self.get_weather(
                                        lat = function_call.args['latitude'],
                                        long= function_call.args['longitude'],
                                        forecast= True if 'forecast' in function_call.args else False
                                    )
                            }
                        )
            
            elif function_call.name == "get_profession_from_prompt":
                part = Part.from_function_response(
                            name= function_call.name,
                            response={
                                    "content": function_call.args['profession']
                            }
                        )
                
            else:
                part = Part.from_function_response(
                            name=function_call.name,
                            response={
                                    "content": function_call.args
                            }
                        )
                                        
            responses.append(part)

        return [pt.function_response for pt in responses], self.chat.send_message(responses)  
                
    def response(self, prompt:str):
        try:
            response = self.chat.send_message(
                message=prompt,
            )

            # if response.candidates[0].content.parts[0].function_call:
            function_calls = [
                part.function_call for part in response.candidates[0].content.parts
                if part.function_call
            ] if response.candidates[0].content.parts[0].function_call else None
                
            function_response, ai_response = self.function_response(function_calls)
            
            return {
                self.data_map[fr.name]:fr.response['content'] for fr in function_response
            } if function_calls else {} # response.text


        
        except Exception as e:
            return {
                "error": type(e).__name__,
                "msg": str(e) if not '503' in str(e) else (
                    ast.literal_eval(str(e).split(". ", 1)[1])['error']
                )#"An error occurred while processing your request."
            }
        

