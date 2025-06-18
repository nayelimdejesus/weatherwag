from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import os

import requests

#to get key
load_dotenv()

app = Flask(__name__) 

#API key
API_key = os.getenv("WEATHER_KEY")
print(f"this is the key {API_key}")

#home page
@app.route("/", methods = ["POST", "GET"])  
def index():
    weather_data = None
    error = ""
    if request.method == "POST":
        city = request.form.get("city").strip()
        country = request.form.get("country").strip()
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_key}"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather_data = {
                "country": data["sys"]["country"],
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "condition": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
            }
        else:
            error = "Enter a valid city, and country code. Please try again."
        
    return render_template("index.html", weather = weather_data, error = error)

if __name__ in "__main__":
    app.run(debug=True, port = 5001)