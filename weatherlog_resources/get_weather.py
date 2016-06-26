# -*- coding: utf-8 -*-


# This file defines functions used for getting the current weather.


# Import datetime for time conversions.
import datetime
# Import URLError for error checking
try:
    # Python 2
    from urllib2 import URLError
except:
    # Python 3
    from urllib.request import URLError
# Import the weather API.
import weatherlog_resources.openweathermap.api as api
import weatherlog_resources.degrees as degrees
import weatherlog_resources.clouds as clouds
# Import application constants.
from weatherlog_resources.constants import *


# Define day dictionary.
days = {"Sun": "Sunday", "Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday",
        "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday"}


def get_weather(config, units, weather_codes):
    """Gets the current weather for the specified location."""
    
    # Get the location to use.
    if config["location_type"] == "city":
        zipcode = None
        city = config["city"]
    elif config["location_type"] == "zip":
        zipcode = config["zipcode"]
        city = None

    # Get the current weather and forecasts.
    result = api.get_current_weather(config["openweathermap"], units = ("metric" if units["prec"] == "cm" else "imperial"), zipcode = zipcode,
                                     location = city, country = config["country"])
    forecast = api.get_forecast(config["openweathermap"], units = ("metric" if units["prec"] == "cm" else "imperial"), zipcode = zipcode,
                                location = city, country = config["country"])
    
    if result["cod"] == 401 or forecast["cod"] == 401:
        return "Invalid API key. Please check Options and enter a valid API key", False, False
    data = []
    
    # Build the data lists.
    conditions = []
    for cond in result["weather"]:
        conditions.append(weather_codes[int(cond["id"])])
    data1 = [
        ["Condition", "\n".join(conditions)],
        ["Temperature", "%d %s" % (result["main"]["temp"], units["temp"])],
        ["Temperature (minimum)", "%d %s" % (result["main"]["temp_min"], units["temp"])],
        ["Temperature (maximum)", "%d %s" % (result["main"]["temp_max"], units["temp"])],
        ["Wind speed", "%s %s" % (result["wind"]["speed"], units["wind"])],
        ["Wind direction", degrees.degree_to_direction(int(result["wind"]["deg"]))],
        ["Humidity", "%d%%" % result["main"]["humidity"]],
        ["Air pressure", "%d %s" % (result["main"]["pressure"], units["airp"])],
        ["Cloud cover", ["Sunny", "Mostly sunny", "Partly cloudy", "Mostly cloudy", "Cloudy"][clouds.percent_to_term(result["clouds"]["all"])]],
        ["Sunrise", datetime.datetime.fromtimestamp(result["sys"]["sunrise"]).strftime("%H:%M:%S")],
        ["Sunset", datetime.datetime.fromtimestamp(result["sys"]["sunset"]).strftime("%H:%M:%S")]
    ]
    data2 = [
        ["Location", result["name"]],
        ["Country", result["sys"]["country"]],
        ["Latitude", str(result["coord"]["lat"])],
        ["Longitude", str(result["coord"]["lon"])]
    ]
    data3 = [
    ]
    for i in range(0, len(forecast["list"])):
        fc = forecast["list"][i]
        conditions = []
        for cond in fc["weather"]:
            conditions.append(weather_codes[int(cond["id"])])
        data3.append(["Date", datetime.datetime.fromtimestamp(fc["dt"]).strftime("%d/%m/%Y")])
        data3.append(["Condition", "\n".join(conditions)])
        data3.append(["Temperature", "%d %s" % (fc["temp"]["day"], units["temp"])])
        data3.append(["Temperature (minimum)", "%d %s" % (fc["temp"]["min"], units["temp"])])
        data3.append(["Temperature (maximum)", "%d %s" % (fc["temp"]["max"], units["temp"])])
        data3.append(["Temperature (morning)", "%d %s" % (fc["temp"]["morn"], units["temp"])])
        data3.append(["Temperature (evening)", "%d %s" % (fc["temp"]["eve"], units["temp"])])
        data3.append(["Temperature (night)", "%d %s" % (fc["temp"]["night"], units["temp"])])
        data3.append(["Wind speed", "%s %s" % (fc["speed"], units["wind"])])
        data3.append(["Wind direction", degrees.degree_to_direction(int(fc["deg"]))])
        data3.append(["Humidity", "%d%%" % fc["humidity"]])
        data3.append(["Air pressure", "%d %s" % (fc["pressure"], units["airp"])])
        data3.append(["Cloud cover", ["Sunny", "Mostly sunny", "Partly cloudy", "Mostly cloudy", "Cloudy"][clouds.percent_to_term(fc["clouds"])]])
        if "rain" in fc:
            data3.append(["Precipitation (rain)", "%d %s" % (fc["rain"], units["prec"])])
        if "snow" in fc:
            data3.append(["Precipitation (snow)", "%d %s" % (fc["snow"], units["prec"])])
        if i != len(forecast["list"]) - 1:
            data3.append(["", ""])

    data.append(data1)
    data.append(data2)
    data.append(data3)

    # Get the prefill data.
    prefill_data = [
        float(result["main"]["temp"]),
        float(result["main"]["temp"]),
        float(result["wind"]["speed"]),
        degrees.degree_to_direction(float(result["wind"]["deg"])),
        float(result["main"]["humidity"]),
        float(result["main"]["pressure"]),
        int(result["clouds"]["all"])
    ]

    return result["name"], data, prefill_data, result["weather"][0]["id"]


def get_weather_image(code):
    """Gets the path to the image to display for the given code. Uses Yahoo Weather codes."""
    
    base_url = "weatherlog_resources/images/weather_icons/"
    img_url = "error.png"
    
    # Sunny:
    if code in WeatherCondition.SUNNY:
        img_url = "sunny.png"
    
    # Cloudy:
    if code in WeatherCondition.CLOUDY:
        img_url = "cloudy.png"
    
    # Clear (night):
    if code in WeatherCondition.CLEAR_NIGHT:
        img_url = "clear_night.png"
    
    # Partly cloudy and similar:
    if code in WeatherCondition.PARTLY_CLOUDY:
        img_url = "partly_cloudy.png"
    
    # Fog and similar:
    if code in WeatherCondition.FOG:
        img_url = "fog.png"
    
    # Windy and similar:
    if code in WeatherCondition.WIND:
        img_url = "windy.png"
    
    # Light rain and similar:
    if code in WeatherCondition.RAIN_LIGHT:
        img_url = "rain_little.png"
    
    # Rain and similar:
    if code in WeatherCondition.RAIN:
        img_url = "rain.png"
    
    # Heavy rain and similar:
    if code in WeatherCondition.RAIN_HEAVY:
        img_url = "rain_lots.png"
    
    # Thunderstorms and similar:
    if code in WeatherCondition.THUNDERSTORM:
        img_url = "rain_thunder.png"
    
    # Heavy thunderstorms and similar:
    if code in WeatherCondition.THUNDERSTORM_HEAVY:
        img_url = "rain_thunder_lots.png"
    
    # Mixed snow - rain and similar:
    if code in WeatherCondition.MIXED:
        img_url = "rain_snow.png"
    
    # Light snow and similar:
    if code in WeatherCondition.SNOW_LIGHT:
        img_url = "snow_little.png"
    
    # Snow and similar:
    if code in WeatherCondition.SNOW:
        img_url = "snow.png"
    
    # Heavy snow and similar:
    if code in WeatherCondition.SNOW_HEAVY:
        img_url = "snow_lots.png"
    
    return base_url + img_url


def get_prefill_data(user_location, units, config):
    """Gets the data used to automatically fill Add New dialog."""
    
    # Get the data.
    try:
        data = api.get_current_weather(config["openweathermap"], units = ("metric" if units["prec"] == "cm" else "imperial"), zipcode = config["zipcode"],
                                       location = config["city"], country = config["country"])
    except URLError:
        return False, "Cannot get current weather; no internet connection."
    
    if data["cod"] == 401:
        return False, "Invalid API key. Please check Options and enter a valid API key"
    
    pre = {
        "temp": float(data["main"]["temp"]),
        "chil": float(data["main"]["temp"]),
        "wind": float(data["wind"]["speed"]),
        "wind_dir": float(data["wind"]["deg"]),
        "humi": float(data["main"]["humidity"]),
        "airp": float(data["main"]["pressure"]),
        "clou": int(data["clouds"]["all"])
    }
    
    location = "%s, %s" % (data["name"], data["sys"]["country"])
    
    return location, pre
