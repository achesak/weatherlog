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

    return result["location"]["city"], data, prefill_data
