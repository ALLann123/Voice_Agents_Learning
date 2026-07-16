#!/usr/bin/python3
import requests
import os
from dotenv import load_dotenv

# load our API key
load_dotenv()

# access it
API_KEY=os.getenv("WEB_API")

# function
def get_weather(city):
    # we are fetching our weather from openweather web app.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    # send our HTTP request
    response=requests.get(url)

    #iterate through the request
    if response.status_code==200:
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

# call the function
result=get_weather("Nairobi")
print(f"FROM API= {result}")

"""
\Tools\weather_api>python main.py
FROM API=
    Current Weather Report

    Location: Nairobi
    Temperature: 24.35°C
    Humidity: 43%
    Conditions: overcast clouds
    Wind Speed: 2.39 m/s
"""