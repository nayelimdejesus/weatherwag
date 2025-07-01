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

default_city = "san jose"
default_state = "CA"

# amazon recommendation products
products = {
        "green": [
            {
                "name": "Dog Chew Toy",
                "image_url": "/static/img/green/dog_toy.jpg",
                "affiliate_url": "https://amzn.to/46fclJo"
            },
            {
                "name": "ChomChom Roller | Hair Remover and Reusable Lint Roller",
                "image_url": "/static/img/green/dog_roller.jpg",
                "affiliate_url": "https://amzn.to/4lijtJX"
            },
            {
                "name": "WINGOIN | Tactical Dog Harness",
                "image_url": "/static/img/green/dog_harness.jpg",
                "affiliate_url": "https://amzn.to/3THDMUI"
            },
            {
                "name": "ICEFANG | Tactical Dog Harness",
                "image_url": "/static/img/green/dog_harness2.jpg",
                "affiliate_url": "https://amzn.to/4liH38M"
            },
            {
                "name": "Comfort Expression | Orthopedic Foam Dog Beds",
                "image_url": "/static/img/green/dog_bed.jpg",
                "affiliate_url": "https://amzn.to/3TcRBud"
            },
        ],  
        "orange": [
            {
                "name": "Hcpet | Dog Shoes",
                "image_url": "/static/img/orange/dog_booties.jpg",
                "affiliate_url": "https://amzn.to/4lrhG4K",
            },
            {
                "name": "ChomChom Roller | Hair Remover and Reusable Lint Roller",
                "image_url": "/static/img/orange/dog_roller.jpg",
                "affiliate_url": "https://amzn.to/4lijtJX"
            },
            {
                "name": "ARF Pets | Dog Cooling Mat",
                "image_url": "/static/img/orange/dog_mat.jpg",
                "affiliate_url": "https://amzn.to/3GfoFij"
            },
            {
                "name": "ICEFANG | Tactical Dog Harness",
                "image_url": "/static/img/orange/dog_harness2.jpg",
                "affiliate_url": "https://amzn.to/4liH38M"
            },
            {
                "name": "Amazon Basics | Cooling Breathable Elevated Dog Bed",
                "image_url": "/static/img/orange/orange_dog.jpg",
                "affiliate_url": "https://amzn.to/4ltyY1a"
            },
        ], 
        "cool": [
            {
                "name": "KYEESE Store | 2 Pack Dog Sweater",
                "image_url": "/static/img/cool/cool_jacket.jpg",
                "affiliate_url": "https://amzn.to/3GcDVMU"
            },
            {
                "name": "Vecomfy Store | Fleece Lining Extra Warm Dog Hoodie",
                "image_url": "/static/img/cool/cool_fleece.jpg",
                "affiliate_url": "https://amzn.to/40rGTDW",
            },
            {
                "name": "Hcpet Store | Hcpet Dog Shoes",
                "image_url": "/static/img/cool/dog_booties.jpg",
                "affiliate_url": "https://amzn.to/3ZRT9xr"
            },
            {
                "name": "Fitwarm Store | Lightweight Fleece Dog Pajamas",
                "image_url": "/static/img/cool/cool_sweater.jpg",
                "affiliate_url": "https://amzn.to/4kaQB4D"
            },
            {
                "name": "Finn Paw Hero | Dog Paw Balm",
                "image_url": "/static/img/cool/dog_paw_balm.jpg",
                "affiliate_url": "https://amzn.to/44fKsyd"
            }
        ],
        "blue": [
            {
                "name": "Bedsure Store | Dog Blanket",
                "image_url": "/static/img/blue/dog_blanket.jpg",
                "affiliate_url": "https://amzn.to/46d5Jew"
            },
            {
                "name": "Musher's Secret Store | Dog Paw Wax",
                "image_url": "/static/img/blue/dog_paw.jpg",
                "affiliate_url": "https://amzn.to/4nnCQCG",
            },
            {
                "name": "JayDaog Store | Warm Dog Jacket",
                "image_url": "/static/img/blue/dog_jacket.jpg",
                "affiliate_url": "https://amzn.to/40mMprq"
            },
            {
                "name": "QBLEEV | Warm Dog Coat",
                "image_url": "/static/img/blue/dog_coat.jpg",
                "affiliate_url": "https://amzn.to/4l5oWng"
            },
            {
                "name": "Finn Paw Hero | Dog Paw Balm",
                "image_url": "/static/img/blue/dog_paw_balm.jpg",
                "affiliate_url": "https://amzn.to/44fKsyd"
            }
        ],
            "dark-blue": [
            {
                "name": "K&H Pet Products | Microwavable Pet Bed Warmer",
                "image_url": "/static/img/dark-blue/micro_warmer.jpg",
                "affiliate_url": "https://amzn.to/3Gktln2"
            },
            {
                "name": "Femont Store | Snuffle Mat",
                "image_url": "/static/img/dark-blue/snuffle_mat.jpg",
                "affiliate_url": "https://amzn.to/44u76Dh",
            },
            {
                "name": "JoyDaog Store | Warm Fleece Dog Coats",
                "image_url": "/static/img/dark-blue/dark_blue_jacket.jpg",
                "affiliate_url": "https://amzn.to/3GncMH5"
            },
            {
                "name": "Furhaven Store | Waterproof Throw Blanket for Dogs",
                "image_url": "/static/img/dark-blue/throw_blanket.jpg",
                "affiliate_url": "https://amzn.to/40tPEgT"
            },
            {
                "name": "LaSyl Store | Weighted Blanket for Pets",
                "image_url": "/static/img/dark-blue/weighted_blanket.jpg",
                "affiliate_url": "https://amzn.to/3I21A3a"
            }
        ],
        "red": [
            {
                "name": "Hcpet | Dog Shoes",
                "image_url": "/static/img/red/dog_booties.jpg",
                "affiliate_url": "https://amzn.to/4lrhG4K",
            },
            {
                "name": "ALL FOR PAWS | Dog Ice Bandana",
                "image_url": "/static/img/red/dog_band.jpg",
                "affiliate_url": "https://amzn.to/44kuKlF"
            },
            {
                "name": "ARF Pets | Dog Cooling Mat",
                "image_url": "/static/img/red/dog_mat.jpg",
                "affiliate_url": "https://amzn.to/3GfoFij"
            },
            {
                "name": "Jasonwell | Foldable Dog Pet Bath Pool",
                "image_url": "/static/img/red/dog_pool.jpg",
                "affiliate_url": "https://amzn.to/3ZOKV9r"
            },
            {
                "name": "QUMY | Dog Shoes",
                "image_url": "/static/img/red/dog_booties2.jpg",
                "affiliate_url": "https://amzn.to/4lcqH1G"
            }
        ],
            "dark-red": [
            {
                "name": "Yipetor | Frozen Treat Dispensing Dog Toy",
                "image_url": "/static/img/dark-red/dog_enrich.jpg",
                "affiliate_url": "https://amzn.to/44wWlkJ",
            },
            {
                "name": "Furhaven | Cooling Gel Dog Bed",
                "image_url": "/static/img/dark-red/dog_cooling_bed.jpg",
                "affiliate_url": "https://amzn.to/4kuuzdD"
            },
            {
                "name": "WOOF | Party Pupsicle - Long Lasting",
                "image_url": "/static/img/dark-red/dog_pupsicle.jpg",
                "affiliate_url": "https://amzn.to/44323KZ"
            },
            {
                "name": "Rundik | Snuffle Mat for Dogs",
                "image_url": "/static/img/dark-red/dog_sniff_mat.jpg",
                "affiliate_url": "https://amzn.to/444vL2j"
            },
            {
                "name": "Race&Herd | Herd Dog Scent Training Kit",
                "image_url": "/static/img/dark-red/dog_training.jpg",
                "affiliate_url": "https://amzn.to/4k4uT2d"
            }
        ],
    }

def fetch_weather(city, state, key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},us&appid={key}&units=imperial"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
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
    
# home page
@app.route("/", methods=["POST", "GET"])
def index():
    weather_data = None
    error = ""
    condition = ""
    dog_warning = ""
    color_message = ""
    dog_data = None
    data = None
    
    # setting city and state
    city = default_city
    state = default_state
    
    # getting information from states.json
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

    result = fetch_weather(city, state, API_key)
    if(isinstance(result, tuple)):
        if None in result:
            error = result[1]
            return error
        data = result[0]
        error = result[1]
    else:
        data = result

    # convert suntime, sunset data to time
    sunrise_time = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p")
    sunset_time = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")

    weather_temp = round(data["main"]["feels_like"])
    humidity = data["main"]["humidity"]
    condition = data["weather"][0]["main"]
    condition_message = ""
    
    if condition == "Rain":
        condition_message = "It's raining. Shorten walks and dry your dog thoroughly afterwards."

    if weather_temp < 20:
        color_message = "dark-blue"
        dog_warning = "Extreme cold may increase the risk of frostbite. Consider bundling up your dog or limiting outdoor time."
    elif 20 <= weather_temp < 32:
        color_message = "dark-blue"
        dog_warning = "Very cold outside. It’s best to keep walks short. Consider dressing small, short-haired, or elderly dogs warmly."
    elif 32 <= weather_temp < 45:
        color_message = "blue"
        dog_warning = "Cold weather, it's best to keep walk shorts. Consider dressing small, short-haired, or elderly dogs warmly."
    elif 45 <= weather_temp < 55:
        color_message = "cool"
        dog_warning = "Mildly cool weather. Most dogs are comfortable, but watch small, thin-coated, or elderly dogs closely."
    elif 55 <= weather_temp < 70:
        if humidity <= 60:
            color_message = "green"
            dog_warning = "Conditions appear comfortable for most dogs. Please monitor your dog and use caution during outdoor activities."
        else:
            color_message = "orange"
            dog_warning = "Mild temperature but higher humidity. Take precautions to keep your dog comfortable, including breaks and hydration."
    elif 70 <= weather_temp < 85:
        if humidity <= 60:
            color_message = "green"
            dog_warning = "Conditions appear comfortable for most dogs. Please monitor your dog and use caution during outdoor activities."
        else:
            color_message = "orange"
            dog_warning = "The weather is warm with higher humidity. Take precautions to keep your dog comfortable, including breaks and hydration."
    elif 85 <= weather_temp < 90:
        color_message = "orange"
        dog_warning = "It's getting warm. Keep walks shorts and stay hyrdated. Avoid midday heat."
    elif 90 <= weather_temp < 95:
        color_message = "red"
        dog_warning = "Very hot weather. Walk early or late. Watch for signs of overheating."
    elif weather_temp > 95:
        color_message = "dark-red"
        dog_warning = "Extreme heat warning. Limit outdoor activity and keep your dog cool and hydrated."
        
    if condition_message != "":
        dog_warning += f" * Note: {condition_message}"
    product_recommendation = products[color_message]
    dog_data = {
        "dog_warning": dog_warning,
        "color_message": color_message,
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
