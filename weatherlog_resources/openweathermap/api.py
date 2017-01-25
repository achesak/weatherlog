# -*- coding: utf-8 -*-


################################################################################
#
# weatherlog-openweathermap: api module
#
# This library is used by WeatherLog to get data from Open Weather Map: http://openweathermap.org/
#
# Released under the MIT open source license:
"""
Copyright (c) 2016 Adam Chesak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
#
################################################################################


import json
try:
    # Python 2
    from urllib2 import urlopen
    from urllib import quote_plus
except ImportError:
    # Python 3
    from urllib.request import urlopen
    from urllib.parse import quote_plus
    

__all__ = ["get_current_weather", "get_forecast"]


class OpenWeatherMap:
    BASE = "http://api.openweathermap.org/data/2.5/"
    WEATHER = "http://api.openweathermap.org/data/2.5/weather?"
    FORECAST = "http://api.openweathermap.org/data/2.5/forecast/daily?"


def build_api_url(devkey, mode, units, zipcode, location, country):
    """Internal function. Builds the API URL."""
    
    api_url = mode
    api_url += "APPID=%s&" % devkey
    api_url += "units=%s&" % units
    
    if zipcode:
        api_url += "zip=%s" % quote_plus(zipcode)
    
    elif location:
        api_url += "q=%s" % quote_plus(location)
    
    if country:
        api_url += ",%s" % quote_plus(country)
    
    return api_url


def get_current_weather(devkey, units="metric", zipcode=None, location=None, country=None):
    """Gets the current weather for the given location."""
    
    api_url = build_api_url(devkey, OpenWeatherMap.WEATHER, units, zipcode, location, country)
    
    request = urlopen(api_url)
    result = request.read()
    request.close()
    
    return json.loads(result)


def get_forecast(devkey, units="metric", zipcode=None, location=None, country=None, days="7"):
    """Gets the forecast for the given location."""
    
    api_url = build_api_url(devkey, OpenWeatherMap.FORECAST, units, zipcode, location, country)
    api_url += "&cnt=%s" % days
    
    request = urlopen(api_url)
    result = request.read()
    request.close()
    
    return json.loads(result)
