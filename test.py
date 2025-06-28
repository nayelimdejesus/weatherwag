import pytest
from app import fetch_weather
from dotenv import load_dotenv
import os
import requests

load_dotenv()

# API key
API_key = os.getenv("WEATHER_KEY")

# test that my function returns correct default city, and error after invalid input
def test_invalid_city():
    data, error =  fetch_weather("thisCity", "CA", API_key)
    assert data["name"] == "San Jose"
    assert error == "Invalid city or state code. Please try again."
    
# test that my function returns the correct error after a timeout
def test_api_timeout(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.exceptions.Timeout()
    
    monkeypatch.setattr("requests.get", fake_get)
    result = fetch_weather("Greenfield", "CA", API_key)
    assert result == "OpenWeather API timed out. Please try again later." 
    
 # test that my function returns a request failure message if a general RequestException occurs.
def test_connection(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.exceptions.RequestException()
    
    monkeypatch.setattr("requests.get", fake_get)    
    result = fetch_weather("Greenfield", "CA", API_key)
    assert result.startswith("Request Failed: ")
    
# tests that my function returns the correct error when ValueError is raised.
def test_value_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise ValueError()
    
    monkeypatch.setattr("requests.get", fake_get)
    result = fetch_weather("Greenfield", "CA", API_key)
    assert result == "Error parsing response from OpenWeather."
    
