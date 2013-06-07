# -*- coding: utf-8 -*-


# This file defines the function used for validating the data.


# Import re for validating the data.
import re


def validate(date, temp, prec, prec_type, wind, wind_dir, humi, airp, clou):
    """Validates the data."""
    
    # Create the message string.
    missing_msg = ""
    
    # If the date is missing or of the wrong type:
    if not date:
        missing_msg += "Date is missing.\n"
    elif not re.compile("^\d{1,2}/\d{1,2}/\d{2}$").match(date):
        missing_msg += "Date does not match the pattern DD/MM/YY.\n"
    
    # If the temperature is missing or of the wrong type:
    if not temp:
        missing_msg += "Temperature is missing.\n"
    elif not re.compile("^\d+$").match(temp):
        missing_msg += "Temperature must be a number.\n"
    
    # If the precipitation amount is missing or of the wrong type:
    if not prec:
        missing_msg += "Precipitation amount is missing.\n"
    elif not re.compile("^\d+$").match(prec):
        missing_msg += "Precipitation amount must be a number.\n"
    
    # If the precipitation type is missing or not a valid value:
    if not prec_type:
        missing_msg += "Precipitation type is missing.\n"
    elif prec_type not in ["Rain", "Snow", "Hail", "Sleet"]:
        missing_msg += "Precipitation type is not a valid value. (This should never happen.)\n"
    
    # If the wind speed is missing or of the wrong type:
    if not wind:
        missing_msg += "Wind speed is missing.\n"
    elif not re.compile("^\d+$").match(wind):
        missing_msg += "Wind speed must be a number.\n"
    
    # If the wind direction is missing or not a valid value:
    if not wind_dir:
        missing_msg += "Wind direction is missing.\n"
    elif wind_dir not in ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]:
        missing_msg += "Wind direction is not a valid value. (This should never happen.)\n"
    
    # If the humidity is missing or of the wrong type:
    if not humi:
        missing_msg += "Humidity is missing.\n"
    elif not re.compile("^\d+$").match(humi):
        missing_msg += "Humidity must be a number.\n"
    
    # If the air pressure is missing or of the wrong type:
    if not airp:
        missing_msg += "Air pressure is missing.\n"
    elif not re.compile("^\d+$").match(airp):
        missing_msg += "Air pressure must be a number.\n"
    
    # If the cloud cover is missing or not a valid value:
    if not clou:
        missing_msg += "Cloud cover is missing.\n"
    elif clou not in ["Sunny", "Mostly Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy"]:
        missing_msg += "Cloud cover is not a valud value. (This should never happen.)\n"
    
    # Return the message string.
    return missing_msg.rstrip()