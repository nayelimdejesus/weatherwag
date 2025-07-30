from flask import Flask, jsonify, render_template, request, redirect
from dotenv import load_dotenv
from datetime import datetime
from flask_mail import Mail, Message
from google import genai
from google.genai import types
import os
import json
import time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import random

import requests

load_dotenv()

app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

default_city = "San Jose"
default_state = "CA"

weather_cache = {
    "data": None,
    "timestamp": 0
}

def get_gemini_response(weather_content, question):
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= weather_content + question,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        ),
    )
    return response.text



def convert_utc_to_local_time(utc_timestamp, timezone):
    utc_dt = datetime.fromtimestamp(utc_timestamp, tz = ZoneInfo("UTC"))
    try:
        local_dt = utc_dt.astimezone(ZoneInfo(timezone))
        return local_dt.strftime("%I:%M %p")
    except ZoneInfoNotFoundError:
        return utc_dt.strftime("%I:%M %p")



def fetch_weather_details(city, state, key, user_submits_form):
    now = time.time()
    if not user_submits_form:
        # if data exist in weather_cache and the timestamp is less than 10 minutes
        if weather_cache["data"] and now - weather_cache["timestamp"] < 600:
            return weather_cache["data"]

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},us&appid={key}&units=imperial"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # if the user did not input anything then we will store new data into the weather_cache
        if not user_submits_form:
            weather_cache["data"] = data
            weather_cache["timestamp"] = now
            return weather_cache["data"]
    
        return data
    except requests.exceptions.Timeout:
        error = "OpenWeather API timed out. Please try again later." 
        return error
    except requests.exceptions.HTTPError as req_err:
        error = "Invalid city or state code. Please try again."
        url = f"https://api.openweathermap.org/data/2.5/weather?q={default_city},{default_state},us&appid={key}&units=imperial"
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            error = "Request failed. We're having trouble fetching the weather right now. Please try again shortly."
            return None, error
        return data,error
    except requests.exceptions.RequestException as req_err:
        return f"Request Failed: {req_err}"
    except ValueError:
        error = "Error parsing response from OpenWeather."
        return error
keywords = [
    "walk",
    "walking",
    "dog",
    "dogs",
    "breed",
    "weather",
    "temperature",
    "hot",
    "heat",
    "cold",
    "chilly",
    "rain",
    "rainy",
    "snow",
    "snowy",
    "wind",
    "windy",
    "humidity",
    "sun",
    "sunburn",
    "safe",
    "safety",
    "paws",
    "paw",
    "paw pads",
    "overheating",
    "heat stroke",
    "cold stress",
    "frostbite",
    "hypothermia",
    "uncomfortable",
    "discomfort",
    "hydration",
    "water",
    "drink",
    "exercise",
    "joint pain",
    "arthritis",
    "clothing",
    "coat",
    "gear",
    "time of day",
    "morning",
    "evening",
    "signs",
    "symptoms",
    "allergies",
    "thunderstorm",
    "storm",
    "air quality",
    "wildfire smoke",
    "indoor play",
    "outside",
    "sensitive",
    "sensitivity",
    "puppy",
    "puppies",
    "older dog",
    "short-nosed",
    "short nosed",
    "breed-specific"
]

@app.route("/chat", methods = ["POST"])
def chat():
    data = request.json
    weather = data.get("weather", {})
    question = data.get("question", "")
    unrelated_response = ("""
        I'm here to help with dog weather safety and walking advice! 
        For other questions, please check with a relevant expert or resource. 
        How can I assist you with your dog's outdoor activities today?
    """
    )
    weather_content = f"""
        You are WagBot, a cheerful and helpful weather safety assistant for dog owners. 
        Based on the current weather in {weather['city']}, {weather['state']}, {weather['country']}, provide a personalized short paragraph answering the user's question. 
        Then give a second short paragraph with clear advice for walking dogs outdoors. 
        Remind users to use their own judgment. 
        Current conditions: temperature {weather['temp']}°F (feels like {weather['feel_temp']}°F), humidity {weather['humidity']}%, {weather['condition']} with {weather['desc']}. 
        Wind speed: {weather['wind']}, gusts up to {weather['wind_gust']}. 
        Limit your response to 200 words, plain text only, no formatting or asterisks.
    """

    
    if any(word in question for word in keywords):
        answer = get_gemini_response(weather_content, question)
        return jsonify({"chat_answer": answer})
    answer = unrelated_response
    return jsonify({"chat_answer": answer})
    
# home page
@app.route("/", methods=["POST", "GET"])
def index():
    current_weather = None
    error = ""
    weather_condition= ""
    dog_warning = ""
    color_message = ""
    dog_data = None
    weather_api_data = None
    timezone = ""
    condition_message = ""
    weather_content = ""
    form_type = ""
    
    # absolute path to directory
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # loads content from states.json and stores it in states
    states_json_path = os.path.join(base_dir, 'data', 'states.json')
    with open(states_json_path) as f:
        states = json.load(f)
    
    # loads content from safety_tips.json and stores it in tips
    tips_json_path = os.path.join(base_dir, 'data', 'safety_tips.json')
    with open(tips_json_path) as f:
        safety_tips = json.load(f)
    
    # loads content from amazon_products.json and stores it in amazon_products
    amazon_products_path = os.path.join(base_dir, 'data', 'amazon_products.json')
    with open(amazon_products_path) as f:
        amazon_products = json.load(f)
    
    
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        state = request.form.get("states", "") 
        timezone = request.form.get("timezone", "")
        user_submits_form = True
    else:
        timezone = "America/Los_Angeles"
        city = default_city
        state = default_state
        user_submits_form  = False

    weather_api_result = fetch_weather_details(city, state, WEATHER_API_KEY, user_submits_form)
    
    if(isinstance(weather_api_result, tuple)):
        if None in weather_api_result:
            error = weather_api_result[1]
            return error
        weather_api_data, error = weather_api_result
    else:
        weather_api_data = weather_api_result

    # converting utc to user local time
    utc_timestamp = weather_api_data["dt"]
    user_local_time = convert_utc_to_local_time(utc_timestamp, timezone)
    
    utc_sunrise_time = weather_api_data["sys"]["sunrise"]
    utc_sunset_time = weather_api_data["sys"]["sunset"]

    sunrise_time = convert_utc_to_local_time(utc_sunrise_time, timezone)
    sunset_time = convert_utc_to_local_time(utc_sunset_time, timezone)
    
    # variables we consider when checking if it's comfortable for your dog to walk.
    feels_like_temp = round(weather_api_data["main"]["feels_like"])
    humidity = weather_api_data["main"]["humidity"]
    weather_condition= weather_api_data["weather"][0]["main"]
    
    if weather_condition== "Rain":
        condition_message = "It's raining. Shorten walks and dry your dog thoroughly afterwards."

    if feels_like_temp < 20:
        color_message = "dark-blue"
        dog_warning = "Extreme cold may increase the risk of frostbite. Consider bundling up your dog or limiting outdoor time."
    elif 20 <= feels_like_temp < 32:
        color_message = "dark-blue"
        dog_warning = "Very cold outside. It’s best to keep walks short. Consider dressing small, short-haired, or elderly dogs warmly."
    elif 32 <= feels_like_temp < 45:
        color_message = "blue"
        dog_warning = "Cold weather, it's best to keep walk shorts. Consider dressing small, short-haired, or elderly dogs warmly."
    elif 45 <= feels_like_temp < 55:
        color_message = "cool"
        dog_warning = "Mildly cool weather. Most dogs are comfortable, but watch small, thin-coated, or elderly dogs closely."
    elif 55 <= feels_like_temp < 70:
        if humidity <= 60:
            color_message = "green"
            dog_warning = "Conditions appear comfortable for most dogs. Please monitor your dog and use caution during outdoor activities."
        else:
            color_message = "orange"
            dog_warning = "Mild temperature but higher humidity. Take precautions to keep your dog comfortable, including breaks and hydration."
    elif 70 <= feels_like_temp < 85:
        if humidity <= 60:
            color_message = "green"
            dog_warning = "Conditions appear comfortable for most dogs. Please monitor your dog and use caution during outdoor activities."
        else:
            color_message = "orange"
            dog_warning = "The weather is warm with higher humidity. Take precautions to keep your dog comfortable, including breaks and hydration."
    elif 85 <= feels_like_temp < 90:
        color_message = "orange"
        dog_warning = "It's getting warm. Keep walks shorts and stay hyrdated. Avoid midday heat."
    elif 90 <= feels_like_temp < 95:
        color_message = "red"
        dog_warning = "Very hot weather. Walk early or late. Watch for signs of overheating."
    elif feels_like_temp > 95:
        color_message = "dark-red"
        dog_warning = "Extreme heat warning. Limit outdoor activity and keep your dog cool and hydrated."
        
    if condition_message != "":
        dog_warning += f" * Note: {condition_message}"
    product_recommendation = amazon_products[color_message]
    
    if color_message in ["orange", "cool"]:
        selected_safety_tips = safety_tips["green"]
    else:
        selected_safety_tips = safety_tips[color_message]
    
    random_num = random.randint(0, len(selected_safety_tips)-1)
    random_safety_tip = selected_safety_tips[random_num]
    
    # pass these data to the HTML template
    dog_data = {
        "dog_warning": dog_warning,
        "color_message": color_message,
        "dog_tip_message": random_safety_tip,
    }
        
    current_weather = {
        "country": weather_api_data["sys"]["country"],
        "city": weather_api_data["name"],
        "temperature": round(weather_api_data["main"]["temp"]),
        "feels_temp": round(weather_api_data["main"]["feels_like"]),
        "humidity": weather_api_data["main"]["humidity"],
        "condition": weather_api_data["weather"][0]["main"],
        "description": weather_api_data["weather"][0]["description"],
        "icon": weather_api_data["weather"][0]["icon"],
        "wind": round(weather_api_data["wind"]["speed"]),
        "wind_gust": round(weather_api_data["wind"].get("gust", 0)),
        "sunrise": sunrise_time,
        "sunset": sunset_time,
        "time": user_local_time 
    }
    location_details ={
        "lon": weather_api_data["coord"]["lon"],
        "lat": weather_api_data["coord"]["lat"]
    }
    weather_condition = current_weather["condition"].lower()
    
    return render_template(
        "index.html",
        dog=dog_data,
        weather=current_weather,
        error=error,
        condition=weather_condition,
        state=state,
        states = states,
        product_recom = product_recommendation,
        GOOGLE_API_KEY = GOOGLE_API_KEY,
        location = location_details
    )

@app.route("/about", methods=["GET"])
def about():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    states_json_path = os.path.join(base_dir, 'data', 'states.json')
    
    with open(states_json_path) as f:
        states = json.load(f)
        
    return render_template(
        "about.html",
        states = states,
        body_class = 'about-bg'
    )
@app.route("/contact", methods=["GET", "POST"])
def contact():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    states_json_path = os.path.join(base_dir, 'data', 'states.json')
    message_sent = False
    
    with open(states_json_path) as f:
        states = json.load(f)

    # if the user submits the form
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()


        body = (
            f"From: {first_name} {last_name}\n"
            f"Email: {email}\n\n"
            f"Message:\n{message}"
        )

        
        msg = Message(
            subject = "WeatherWag-Message",
            sender = os.getenv("MAIL_USERNAME"),
            recipients = [os.getenv("MAIL_USERNAME")],
            body = body
        )
        mail.send(msg)
        message_sent = True
    else:
        message_sent = False
        
    return render_template(
        "contact.html",
        states = states,
        body_class = 'about-bg',
        message_sent = message_sent
    )
    

if __name__ in "__main__":
    app.run(debug=True, port=5001)
