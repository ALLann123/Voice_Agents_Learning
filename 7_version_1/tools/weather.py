#!/usr/bin/python3
import requests
import os
from dotenv import load_dotenv

# Load our API key
load_dotenv()

# access it
API_KEY=os.getenv("WEB_API")

def get_weather(city):
    # fetching weather from open weather web app
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    # Send our HTTP request
    response=requests.get(url)

    # filter and iterate through the request
    if response.status_code==200:
        # If we connected to the web seaver. Convert the response received to json
        data=response.json()

        temperature=data["main"]["temp"]
        humidity=data["main"]["humidity"]
        description=data["weather"][0]["description"]
        wind_speed=data["wind"]["speed"]
        weather_report = f"""
    Current Weather Report

    Location: {city}
    Temperature: {temperature}°C
    Humidity: {humidity}%
    Conditions: {description}
    Wind Speed: {wind_speed} m/s
    """
        # return the above report
        return weather_report
    
    else:
        return f"Error retrieving weather data: {response.status_code}"
    

