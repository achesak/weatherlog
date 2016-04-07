# -*- coding: utf-8 -*-


# This file defines functions used for getting the current weather.


# Import the weather API.
import weatherlog_resources.dialogs.pywapi.pywapi as pywapi
# Import the functions for converting degrees to a direction.
import weatherlog_resources.degrees as degrees


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
    if code in [32, 34]:
        img_url = "sunny.png"
    
    # Cloudy:
    if code in [26]:
        img_url = "cloudy.png"
    
    # Clear (night):
    if code in [31, 33]:
        img_url = "clear_night.png"
    
    # Partly cloudy and similar:
    if code in [27, 28, 29, 30, 44]:
        img_url = "partly_cloudy.png"
    
    # Fog and similar:
    if code in [19, 20, 21, 22]:
        img_url = "fog.png"
    
    # Windy and similar:
    if code in [23, 24, 0, 2, 15]:
        img_url = "windy.png"
    
    # Light rain and similar:
    if code in [8, 9]:
        img_url = "rain_little.png"
    
    # Rain and similar:
    if code in [10, 11, 12, 40]:
        img_url = "rain.png"
    
    # Heavy rain and similar:
    if code in [1, 6, 17, 18, 35]:
        img_url = "rain_lots.png"
    
    # Thunderstorms and similar:
    if code in [4, 37, 38, 39, 45, 47]:
        img_url = "rain_thunder.png"
    
    # Heavy thunderstorms and similar:
    if code in [3]:
        img_url = "rain_thunder_lots.png"
    
    # Mixed snow - rain and similar:
    if code in [5, 7]:
        img_url = "rain_snow.png"
    
    # Light snow and similar:
    if code in [13, 14]:
        img_url = "snow_little.png"
    
    # Snow and similar:
    if code in [16, 42, 46]:
        img_url = "snow.png"
    
    # Heavy snow and similar:
    if code in [41, 43]:
        img_url = "snow_lots.png"
    
    return base_url + img_url


def get_prefill_data(user_location, units):
    """Gets the data used to automatically fill Add New dialog."""
    
    # Get the data.
    data = pywapi.get_weather_from_yahoo(user_location, units = ("metric" if units["prec"] == "cm" else "imperial"))
    if "error" in data:
        return False, data["error"]
    
    pre = {
        "temp": float(data["condition"]["temp"]),
        "chil": float(data["wind"]["chill"]),
        "wind": float(data["wind"]["speed"]),
        "wind_dir": float(data["wind"]["direction"]),
        "humi": float(data["atmosphere"]["humidity"]),
        "airp": float(data["atmosphere"]["pressure"]),
        "airp_change": int(data["atmosphere"]["rising"])
    }
    
    if units["airp"] == "mbar":
        pre["airp"] *= 33.86389
    
    if data["atmosphere"]["visibility"].lstrip().rstrip() == "":
        pre["visi"] = 0.0
    else:
        pre["visi"] = float(data["atmosphere"]["visibility"])
    
    location = "%s, %s" % (data["location"]["city"], data["location"]["country"])
    
    return location, pre
