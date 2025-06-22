from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
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
            
    city = "New York City"
    country = "US"
                
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_key}&units=imperial"

    response = requests.get(url)
    data = response.json()

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
            "wind_gust": round(data["wind"].get("gust", 0))
        }
    condition = weather_data["condition"].lower()
    
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        country = request.form.get("country", "").strip()
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={API_key}&units=imperial"
        response = requests.get(url)
        data = response.json()

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
                "wind_gust": round(data["wind"].get("gust", 0))
            }
            condition = weather_data["condition"].lower()
     
        else:
     
            
            error = "Enter a valid city, and country code. Please try again."
        
    return render_template("index.html", weather = weather_data, error = error, condition = condition)

if __name__ in "__main__":
    app.run(debug=True, port = 5001)