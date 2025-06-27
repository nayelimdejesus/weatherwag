from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from datetime import datetime
import os
import json


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
    default_state = "CA"

    city = default_city
    state = default_state
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    json_path = os.path.join(basedir, 'data', 'states.json')
    
    with open(json_path) as f:
        all_states = json.load(f)
        
    # if the user submits the form
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "")
                
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
    
    products = {
        "okay": [
            {
                "name": "Dog Chew Toy",
                "image_url": "/static/img/okay/dog_toy.jpg",
                "affiliate_url": "https://amzn.to/46fclJo"
            },
            {
                "name": "ChomChom Roller | Hair Remover and Reusable Lint Roller",
                "image_url": "/static/img/okay/dog_roller.jpg",
                "affiliate_url": "https://amzn.to/4lijtJX"
            },
            {
                "name": "WINGOIN | Tactical Dog Harness",
                "image_url": "/static/img/okay/dog_harness.jpg",
                "affiliate_url": "https://amzn.to/3THDMUI"
            },
            {
                "name": "ICEFANG | Tactical Dog Harness",
                "image_url": "/static/img/okay/dog_harness2.jpg",
                "affiliate_url": "https://amzn.to/4liH38M"
            },
            {
                "name": "Comfort Expression | Orthopedic Foam Dog Beds",
                "image_url": "/static/img/okay/dog_bed.jpg",
                "affiliate_url": "https://amzn.to/3TcRBud"
            },
        ],
        "cold": [
            {
                "name": "Bedsure Store | Dog Blanket",
                "image_url": "/static/img/cold/dog_blanket.jpg",
                "affiliate_url": "https://amzn.to/46d5Jew"
            },
            {
                "name": "Musher's Secret Store | Dog Paw Wax",
                "image_url": "/static/img/cold/dog_paw.jpg",
                "affiliate_url": "https://amzn.to/4nnCQCG",
            },
            {
                "name": "JayDaog Store | Warm Dog Jacket",
                "image_url": "/static/img/cold/dog_jacket.jpg",
                "affiliate_url": "https://amzn.to/40mMprq"
            },
            {
                "name": "QBLEEV | Warm Dog Coat",
                "image_url": "/static/img/cold/dog_coat.jpg",
                "affiliate_url": "https://amzn.to/4l5oWng"
            },
            {
                "name": "Finn Paw Hero | Dog Paw Balm",
                "image_url": "/static/img/cold/dog_paw_balm.jpg",
                "affiliate_url": "https://amzn.to/44fKsyd"
            }
        ],
        "hot": [
            {
                "name": "Hcpet | Dog Shoes",
                "image_url": "/static/img/hot/dog_booties.jpg",
                "affiliate_url": "https://amzn.to/4lrhG4K",
            },
            {
                "name": "ALL FOR PAWS | Dog Ice Bandana",
                "image_url": "/static/img/hot/dog_band.jpg",
                "affiliate_url": "https://amzn.to/44kuKlF"
            },
            {
                "name": "ARF Pets | Dog Cooling Mat",
                "image_url": "/static/img/hot/dog_mat.jpg",
                "affiliate_url": "https://amzn.to/3GfoFij"
            },
            {
                "name": "Jasonwell | Foldable Dog Pet Bath Pool",
                "image_url": "/static/img/hot/dog_pool.jpg",
                "affiliate_url": "https://amzn.to/3ZOKV9r"
            },
            {
                "name": "QUMY | Dog Shoes",
                "image_url": "/static/img/hot/dog_booties2.jpg",
                "affiliate_url": "https://amzn.to/4lcqH1G"
            }
        ],
                "danger": [
            {
                "name": "Yipetor | Frozen Treat Dispensing Dog Toy",
                "image_url": "/static/img/danger/dog_enrich.jpg",
                "affiliate_url": "https://amzn.to/44wWlkJ",
            },
            {
                "name": "Furhaven | Cooling Gel Dog Bed",
                "image_url": "/static/img/danger/dog_cooling_bed.jpg",
                "affiliate_url": "https://amzn.to/4kuuzdD"
            },
            {
                "name": "WOOF | Party Pupsicle - Long Lasting",
                "image_url": "/static/img/danger/dog_pupsicle.jpg",
                "affiliate_url": "https://amzn.to/44323KZ"
            },
            {
                "name": "Rundik | Snuffle Mat for Dogs",
                "image_url": "/static/img/danger/dog_sniff_mat.jpg",
                "affiliate_url": "https://amzn.to/444vL2j"
            },
            {
                "name": "Race&Herd | Herd Dog Scent Training Kit",
                "image_url": "/static/img/danger/dog_training.jpg",
                "affiliate_url": "https://amzn.to/4k4uT2d"
            }
        ],
    }

    # convert suntime, sunset data to time
    sunrise_time = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p")
    sunset_time = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")


    weather_temp = round(data["main"]["feels_like"])
    humidity = data["main"]["humidity"]
    weather_product = ""
    
    if 32 > weather_temp <= 45:
        weather_product = "cold"
        color_message = "orange"
        dog_warning = "Cold weather, limit walks to 15-30 min. Use a coat or booties for small, thin-coated, or elderly dogs."
    elif 20 > weather_temp <= 32:
        weather_product = "cold"
        color_message = "red"
        dog_warning = "Very cold, most dogs should only go out for quick potty breaks. Dress small, short haired, or elderly dogs warmly."
    elif weather_temp < 20:
        weather_product = "cold"
        color_message = "red"
        dog_warning = "Dangerously cold, limit time outdoors. Risk of frostbite and hypothermia. Bundle up or stay indoors."
    elif weather_temp < 16:
        weather_product = "cold"
        color_message = "danger"
        dog_warning = "Extreme cold, avoid outdoor walks. Only bring out with full winter gear and direct supervision."
    elif weather_temp <= 85 and humidity <= 60:
        weather_product = "okay"
        color_message = "green"
        dog_warning = "Conditions appear comfortable for most dogs. Please monitor your dog and use caution during outdoor activities."
    elif 85 < weather_temp <= 90:
        weather_product = "warm"
        color_message = "orange"
        dog_warning = "It's getting warm. Keep walks shorts and stay hyrdated. Avoid midday heat."
    elif 90 < weather_temp <= 95:
        weather_product = "hot"
        color_message = "red"
        dog_warning = "Very hot weather. Walk early or late. Watch your dog for signs of overheating."
    elif weather_temp > 95:
        weather_product = "danger"
        color_message = "danger"
        dog_warning = "Danger: Too hot for dogs to walk safely. Please stay indoors."
    elif 50 < weather_temp <= 85 and humidity > 60:
        weather_product = "hot"
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
    product_recommendation = products[weather_product]
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
        "time": datetime.fromtimestamp(data["dt"]).strftime("%I:%M %p")    }
    condition = weather_data["condition"].lower()
    
    return render_template(
        "index.html",
        dog=dog_data,
        weather=weather_data,
        error=error,
        condition=condition,
        state=state,
        all_states = all_states,
        product_recom = product_recommendation,
    )


if __name__ in "__main__":
    app.run(debug=True, port=5001)
