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
    if request.method == "POST":
        city = request.form.get("city").strip()
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            print(f"\nYou chose: {city}")
            print(f"The weather at {city} is: {data}")
            print(data)
        else:
            print(f"{city} not found.")
        
    return render_template("index.html")

if __name__ in "__main__":
    app.run(debug=True, port = 5001)