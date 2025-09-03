import pytest
from app import fetch_weather_details, convert_utc_to_local_time
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

load_dotenv()

# API key
API_key = os.getenv("WEATHER_KEY")

# test that my function returns correct default city, and error after invalid input
def test_invalid_city():
    data, error =  fetch_weather_details("thisCity", "CA", API_key)
    assert data["name"] == "San Jose"
    assert error == "Invalid city or state code. Please try again."
    
# test that my function returns the correct error after a timeout
def test_api_timeout(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.exceptions.Timeout()
    
    monkeypatch.setattr("requests.get", fake_get)
    result = fetch_weather_details("Greenfield", "CA", API_key)
    assert result == "OpenWeather API timed out. Please try again later." 
    
 # test that my function returns a request failure message if a general RequestException occurs.
def test_connection(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.exceptions.RequestException()
    
    monkeypatch.setattr("requests.get", fake_get)    
    result = fetch_weather_details("Greenfield", "CA", API_key)
    assert result.startswith("Request Failed: ")
    
# tests that my function returns the correct error when ValueError is raised.
def test_value_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise ValueError()
    
    monkeypatch.setattr("requests.get", fake_get)
    result = fetch_weather_details("Greenfield", "CA", API_key)
    assert result == "Error parsing response from OpenWeather."
    
    
def test_empty_timzone():
    utc_timestamp = 1721083451
    utc_dt = datetime.fromtimestamp(utc_timestamp, tz = ZoneInfo("UTC"))
    expected = utc_dt.strftime("%I:%M %p")
    result = convert_utc_to_local_time(utc_timestamp, "")

    assert result == expected
