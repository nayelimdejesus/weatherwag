from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from datetime import datetime
import os


import requests

# to get key
load_dotenv()

app = Flask(__name__)

# API key
API_key = os.getenv("WEATHER_KEY")


# home page
@app.route("/", methods=["POST", "GET"])
def index():
    weather_data = None
    walk_times = None
    suggested_walk = None
    error = ""
    condition = ""
    dog_warning = ""
    color_message = ""
    dog_data = None
    default_city = "san jose"
    default_state = "ca"

    city = default_city
    state = default_state

    # if the user submits the form
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
    else:
        city = default_city
        state = default_state


    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},us&appid={API_key}&units=imperial"
    response = requests.get(url)
    data = response.json()

    # if the user inputs something invalid
    if response.status_code != 200:
        city = default_city
        state = default_state
        error = "Invalid city or state code. Please try again."
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},us&appid={API_key}&units=imperial"
        response = requests.get(url)
        data = response.json()
        
    walk_times = {
        "green": {
            "morning": "Morning: 7 AM – 10 AM",
            "afternoon": "Afternoon: 12 PM – 5 PM<br>(shaded recommended)",
            "evening": "Evening: 6 PM – 9 PM",
        },
        "orange": {
            "morning": "Morning: Before 8 AM",
            "evening": "Evening: After 7 PM",
            "note": "Avoid: 10 AM – 6 PM",
        },
        "red": {
            "morning": "Morning: Before 7:30 AM",
            "evening": "Evening: After 8 PM",
            "note": "Avoid: Most of the day – heat stress risk",
        },
        "danger": {"note": "Warning: Too hot to walk safely – stay indoors"},
    }
     
    # convert suntime, sunset data to time
    sunrise_time = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p")
    sunset_time = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")


    weather_temp = round(data["main"]["feels_like"])
    humidity = data["main"]["humidity"]
    
    if 32 > weather_temp <= 45:
        color_message = "orange"
        dog_warning = "Cold weather, limit walks to 15-30 min. Use a coat or booties for small, thin-coated, or elderly dogs."
    elif 20 > weather_temp <= 32:
        color_message = "red"
        dog_warning = "Very cold, most dogs should only go out for quick potty breaks. Dress small, short haired, or elderly dogs warmly."
    elif weather_temp < 20:
        color_message = "red"
        dog_warning = "Dangerously cold, limit time outdoors. Risk of frostbite and hypothermia. Bundle up or stay indoors."
    elif weather_temp < 16:
        color_message = "danger"
        dog_warning = "Extreme cold, avoid outdoor walks. Only bring out with full winter gear and direct supervision."
    elif weather_temp <= 85 and humidity <= 60:
        color_message = "green"
        dog_warning = "Conditions appear comfortable for most dogs. Please monitor your dog and use caution during outdoor activities."
    elif 85 < weather_temp <= 90:
        color_message = "orange"
        dog_warning = "It's getting warm. Keep walks shorts and stay hyrdated. Avoid midday heat."
    elif 90 < weather_temp <= 95:
        color_message = "red"
        dog_warning = "Very hot weather. Walk early or late. Watch your dog for signs of overheating."
    elif weather_temp > 95:
        color_message = "danger"
        dog_warning = "Danger: Too hot for dogs to walk safely. Please stay indoors."
    elif 50 < weather_temp <= 85 and humidity > 60:
        if humidity > 75:
            color_message = "red"
            dog_warning = "High humidity can be hard on dogs. Even in mild temps, watch for signs of overheating. Take it easy."
        else:
            color_message = "orange"
            dog_warning = "Mild temps but elevated humidity. Take breaks and make sure your dog stays hydrated."

    else:
        color_message = "green"
        dog_warning = "Conditions appear comfortable for most dogs. Please monitor your dog and use caution during outdoor activities."

    suggested_walk = walk_times[color_message]
    dog_data = {
        "dog_warning": dog_warning,
        "color_message": color_message,
        "walk_times": suggested_walk,
    }
    weather_data = {
        "country": data["sys"]["country"],
        "city": data["name"],
        "temperature": round(data["main"]["temp"]),
        "feels_temp": round(data["main"]["feels_like"]),
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "wind": round(data["wind"]["speed"]),
        "wind_gust": round(data["wind"].get("gust", 0)),
        "sunrise": sunrise_time,
        "sunset": sunset_time,
    }
    condition = weather_data["condition"].lower()
    user_state = state.upper()
    
    return render_template(
        "index.html",
        dog=dog_data,
        weather=weather_data,
        error=error,
        condition=condition,
        state=user_state,
    )


if __name__ in "__main__":
    app.run(debug=True, port=5001)
