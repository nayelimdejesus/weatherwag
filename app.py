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
    color_message = ""
            
    city = "san jose"
    state = "ca"
    
    if request.method == "POST":
        city = request.form.get("city", "").strip() 
        state = request.form.get("state", "").strip()
     
    else:
        error = "Enter a valid city, and country code. Please try again."
    
    print(city, state)
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},us&appid={API_key}&units=imperial"
    response = requests.get(url)
    data = response.json()
    
        
    if response.status_code == 200:
        sunrise_time = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p')
        sunset_time = datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p')
    
        weather_temp = round(data["main"]["temp"])
        
        humidity = data["main"]["humidity"]
        if weather_temp <= 85 and humidity <= 60:
            color_message = "green"
            dog_warning = "Weather looks safe for your dog's walk. Enjoy your time outside!"
        elif weather_temp > 85 and weather_temp <= 90 and humidity > 60 and humidity <= 70:
            color_message = "orange"
            dog_warning = "It's getting warm. Keep walks shorts and stay hyrdated. Avoid midday heat."
        elif weather_temp > 85 and humidity > 70:
            color_message = "Red"
            dog_warning = "Warning: High heat and humidity. Limit activity and watch for signs of overheating."
        elif weather_temp > 90 and weather_temp <= 95:
            color_message = "Red"
            dog_warning = "It's very hot. Avoid long walks and stick to early morning or evenings."
        elif weather_temp > 95:
            color_message = "Red"
            dog_warning = "Danger: Too hot for dogs to walk safely. Please stay indoors."
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
        
    return render_template("index.html", color_message = color_message, dog_warning = dog_warning, weather = weather_data, error = error, condition = condition)

if __name__ in "__main__":
    app.run(debug=True, port = 5001)