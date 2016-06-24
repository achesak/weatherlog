# -*- coding: utf-8 -*-


# This file defines functions used for getting the current weather.


# Import the weather API.
import weatherlog_resources.openweathermap.api as api
# Import the functions for converting degrees to a direction.
import weatherlog_resources.degrees as degrees
# Import application constants.
from weatherlog_resources.constants import *


# Define day dictionary.
days = {"Sun": "Sunday", "Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday",
        "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday"}


def get_weather(location, config, units, weather_codes):
    """Gets the current weather for the specified location."""

    # Get the current weather and organize it.
    result = pywapi.get_weather_from_yahoo(location, config["units"])
    if isinstance(result, str):
        return result, False, False
    elif "error" in result:
        return result["error"], False, False
    if units["airp"] == "mbar":
        result["atmosphere"]["pressure"] = str(float(result["atmosphere"]["pressure"]) * 33.86389)
    data = []

    # Note: the conversion from int back to str for the temperature is necessary due
    # to encoding issues.
    data1 = [
        ["Condition", weather_codes[result["condition"]["code"]]],
        ["Temperature", "%d %s" % (int(result["condition"]["temp"]), units["temp"])],
        ["Wind speed", "%s %s" % (result["wind"]["speed"], units["wind"])],
        ["Wind direction", degrees.degree_to_direction(int(result["wind"]["direction"]))],
        ["Wind chill", "%d %s" % (int(result["wind"]["chill"]), units["temp"])],
        ["Humidity", "%s%%" % result["atmosphere"]["humidity"]],
        ["Air pressure", "%s %s" % (result["atmosphere"]["pressure"], units["airp"])],
        ["Air pressure change", ["Steady", "Rising", "Falling"][int(result["atmosphere"]["rising"])]],
        ["Visibility", "%s %s" % (result["atmosphere"]["visibility"], result["units"]["distance"])],
        ["Sunrise", result["astronomy"]["sunrise"]],
        ["Sunset", result["astronomy"]["sunset"]]
    ]
    data2 = [
        ["City", result["location"]["city"]],
        ["Region", result["location"]["region"]],
        ["Country", result["location"]["country"]],
        ["Latitude", result["geo"]["lat"]],
        ["Longitude", result["geo"]["long"]]
    ]
    data3 = [
    ]
    for j in range(0, len(result["forecasts"])):
        i = result["forecasts"][j]
        data3.append(["Date", i["date"]])
        data3.append(["Day", days[i["day"]]])
        data3.append(["Condition", weather_codes[i["code"]]])
        data3.append(["Low", "%d %s" % (int(i["low"]), units["temp"])])
        data3.append(["High", "%d %s" % (int(i["high"]), units["temp"])])
        if j != len(result["forecasts"]) - 1:
            data3.append(["", ""])

    data.append(data1)
    data.append(data2)
    data.append(data3)

    # Get the prefill data.
    prefill_data = [
        float(result["condition"]["temp"]),
        float(result["wind"]["chill"]),
        float(result["wind"]["speed"]),
        degrees.degree_to_direction(int(result["wind"]["direction"])),
        float(result["atmosphere"]["humidity"]),
        float(result["atmosphere"]["pressure"]),
        ["Steady", "Rising", "Falling"][int(result["atmosphere"]["rising"])],
        float(result["atmosphere"]["visibility"])
    ]

    return result["location"]["city"], data, prefill_data, int(result["condition"]["code"])


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
    data = api.get_current_weather(config["openweathermap"], units = ("metric" if units["prec"] == "cm" else "imperial"), zipcode = config["zipcode"],
                                   location = config["location"], country = config["country"])
    
    
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
