# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: degrees.py
# This module converts degrees to compass directions.
#
################################################################################


def degree_to_direction(deg):
    """Convert degrees to compass direction."""
    
    # Each direction gets 22.5 degreees, or 11.25 degrees away from the exact center of the direction.
    # For example, exact North is 0 degrees, but anything larger than or equal to 348.75
    # or smaller than 11.25 is also considered North.
    
    # N < 11.25
    if deg < 11.25:
        return "N"
    # 11.25 <= NNE < 33.75
    elif 11.25 <= deg < 33.75:
        return "NNE"
    # 33.75 <= NE < 56.25
    elif 33.75 <= deg < 56.25:
        return "NE"
    # 56.25 <= ENE < 78.75
    elif 56.25 <= deg < 78.75:
        return "ENE"
    # 78.75 <= E < 101.25
    elif 78.75 <= deg < 101.25:
        return "E"
    # 101.25 <= ESE < 123.75
    elif 101.25 <= deg < 123.75:
        return "ESE"
    # 123.75 <= SE < 146.25
    elif 123.75 <= deg < 146.25:
        return "SE"
    # 146.25 <= SSE < 168.75
    elif 146.25 <= deg < 168.75:
        return "SSE"
    # 168.75 <= S < 191.25
    elif 168.75 <= deg < 191.25:
        return "S"
    # 191.25 <= SSW < 213.75
    elif 191.25 <= deg < 213.75:
        return "SSW"
    # 213.75 <= SW < 236.25
    elif 213.75 <= deg < 236.25:
        return "SW"
    # 236.25 <= WSW < 258.75
    elif 236.25 <= deg < 258.75:
        return "WSW"
    # 258.75 <= W < 281.25
    elif 258.75 <= deg < 281.25:
        return "W"
    # 281.25 <= WNW < 303.75
    elif 281.25 <= deg < 303.75:
        return "WNW"
    # 303.75 <= NW < 326.25
    elif 303.75 <= deg < 326.25:
        return "NW"
    # 326.25 <= NNW < 348.75
    elif 326.25 <= deg < 348.75:
        return "NNW"
    # 348.75 <= N
    else:
        return "N"
