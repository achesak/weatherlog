#!/usr/bin/env python
# -*- coding: utf-8 -*-


# weatherlog-openweathermap: codes module


__all__ = ["codes"]


# All codes are from http://openweathermap.org/weather-conditions
codes = {

    # Codes 2xx: Thunderstorm
    200: "Thunderstorm with light rain",
    201: "Thunderstorm with rain",
    202: "Thunderstorm with heavy rain",
    210: "Light thunderstorm",
    211: "Thunderstorm",
    212: "Heavy thunderstorm",
    221: "Ragged thunderstorm",
    230: "Thunderstorm with light drizzle",
    231: "Thunderstorm with drizzle",
    232: "Thunderstorm with heavy drizzle",
    
    # Codes 3xx: Drizzle
    300: "Light intensity drizzle",
    301: "Drizzle",
    302: "Heavy intensity drizzle",
    310: "Light intensity drizzle rain",
    311: "Drizzle rain",
    312: "Heavy intensity drizzle rain",
    313: "Shower rain and drizzle",
    314: "Heavy shower rain and drizzle",
    321: "Shower drizzle",
    
    # Codes 5xx: Rain
    500: "Light rain",
    501: "Moderate rain",
    502: "Heavy intensity rain",
    503: "Very heavy rain",
    504: "Extreme rain",
    511: "Freezing rain",
    520: "Light intensity shower rain",
    521: "Shower rain",
    522: "Heavy intensity shower rain",
    531: "Ragged shower rain",
    
    # Codes 6xx: Snow
    600: "Light snow",
    601: "Snow",
    602: "Heavy snow",
    611: "Sleet",
    612: "Shower sleet",
    615: "Light rain and snow",
    616: "Rain and snow",
    620: "Light shower snow",
    621: "Shower snow",
    622: "Heavy shower snow",
    
    # Codes 7xx: Atmosphere
    701: "Mist",
    711: "Smoke",
    721: "Haze",
    731: "Sand with dust whirls",
    741: "Fog",
    751: "Sand",
    761: "Dust",
    762: "Volcanic ash",
    771: "Squalls",
    781: "Tornado",
    
    # Codes 800: Clear
    800: "Clear sky",
    
    # Codes 80x: Clouds
    801: "Few clouds",
    802: "Scattered clouds",
    803: "Broken clouds",
    804: "Overcast clouds",
    
    # Codes 90x: Extreme
    900: "Tornado",
    901: "Tropical storm",
    902: "Hurricane",
    903: "Cold",
    904: "Hot",
    905: "Windy",
    906: "Hail",
    
    # Codes 9xx: Additional
    951: "Calm",
    952: "Light breeze",
    953: "Gentle breeze",
    954: "Moderate breeze",
    955: "Fresh breeze",
    956: "Strong breeze",
    957: "High winds near gale",
    958: "Gale",
    959: "Severe gale",
    960: "Storm",
    961: "Violent storm",
    962: "Hurricane"
}
