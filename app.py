from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from datetime import datetime
import os


import requests

#to get key
load_dotenv()

app = Flask(__name__) 

#API key
API_key = os.getenv("WEATHER_KEY")
#home page
@app.route("/", methods = ["POST", "GET"])  
def index():
   
    weather_data = None
    error = ""
    condition = ""
    dog_warning = ""
            
    city = "San Jose"
    country = "US"
                
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_key}&units=imperial"

    response = requests.get(url)
    data = response.json()
    sunrise_time = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p')
    sunset_time = datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p')

    if response.status_code == 200:
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
            "sunset": sunset_time
        }
    condition = weather_data["condition"].lower()
    
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        country = request.form.get("country", "").strip()
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={API_key}&units=imperial"
        response = requests.get(url)
        data = response.json()
        sunrise_time = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p')
        sunset_time = datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p')

        # if weather temp is above 85F = message -> be catuious dogs can overheat
        # if weather temp is above 85 and humid is aove 60-75% then be cautious !!!
        # if weather temp is 90 then it's too hot for most dogs
        # if weaher is above 95 -> TOO hot to walk and unsafe!!!
        weather_temp = round(data["main"]["temp"])
        
        humidity = data["main"]["humidity"]
        if weather_temp <= 85 and humidity <= 60:
            dog_warning = "Weather looks safe for your dog's walk. Enjoy your time outside!"
        elif weather_temp > 85 and weather_temp <= 90 and humidity > 60 and humidity <= 70:
            dog_warning = "It's getting warm. Keep walks shorts and stay hyrdated. Avoid midday heat."
        elif weather_temp > 85 and humidity > 70:
            dog_warning = "Warning: High heat and humidity. Limit activity and watch for signs of overheating."
        elif weather_temp > 90 and weather_temp <= 95:
            dog_warning = "It's very hot. Avoid long walks and stick to early morning or evenings."
        elif weather_temp > 95:
            dog_warning = "Danger: Too hot for dogs to walk safely. Please stay indoors."
        
        if response.status_code == 200:
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
                "sunset": sunset_time
            }
            condition = weather_data["condition"].lower()
     
        else:
     
            
            error = "Enter a valid city, and country code. Please try again."
        
    return render_template("index.html", dog_warning = dog_warning, weather = weather_data, error = error, condition = condition)

if __name__ in "__main__":
    app.run(debug=True, port = 5001)