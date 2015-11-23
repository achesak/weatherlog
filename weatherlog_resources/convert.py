# -*- coding: utf-8 -*-


# This file defines the function for converting between units.


# Import this so dividing works correctly.
from __future__ import division


def convert(data2, units):
    """Converts the data."""
    
    data = data2[:]
    for i in range(0, len(data)):
        
        # Convert from imperial to metric:
        if units == "metric":
            
            # Convert the temperature.
            # C = 5/9(F + 32)
            data[i][1] = "%.2f" % ((float(data[i][1]) - 32) * (5 / 9))
            
            # Convert the wind chill
            # C = 5/9(F + 32)
            data[i][2] = "%.2f" % ((float(data[i][2]) - 32) * (5 / 9))
            
            # Convert the precipitation amount.
            # cm = in * 2.54
            if data[i][3] != "None":
                split = data[i][3].split(" ")
                split[0] = "%.2f" % (float(split[0]) * 2.54)
                data[i][3] = " ".join(split)
            
            # Convert the wind speed.
            # kph = mph * 1.60934
            if data[i][4] != "None":
                split = data[i][4].split(" ")
                split[0] = "%.2f" % (float(split[0]) * 1.60934)
                data[i][4] = " ".join(split)
            
            # Convert the visibility.
            # km = mi * 1.60934
            data[i][7] = "%.2f" % (float(data[1][7]) * 1.60934)
        
        # Convert from metric to imperial:
        elif units == "imperial":
            
            # Convert the temperature.
            # F = 9/5C + 32
            data[i][1] = "%.2f" % ((float(data[i][1]) * (9 / 5)) + 32)
            
            # Convert the wind chill.
            # F = 9/5C + 32
            data[i][2] = "%.2f" % ((float(data[i][2]) * (9 / 5)) + 32)
            
            # Convert the precipitation amount.
            # in = cm / 2.54
            if data[i][3] != "None":
                split = data[i][3].split(" ")
                split[0] = "%.2f" % (float(split[0]) / 2.54)
                data[i][3] = " ".join(split)
            
            # Convert the wind speed.
            # mph = kph / 1.60934
            if data[i][4] != "None":
                split = data[i][4].split(" ")
                split[0] = "%.2f" % (float(split[0]) / 1.60934)
                data[i][4] = " ".join(split)
            
            # Convert the visibility.
            # mi = km / 1.60934
            data[i][7] = "%.2f" % (float(data[1][7]) / 1.60934)
    
    return data


def new_convert(units_main, data2, units):
    """Converts the data from the Add New and Edit dialogs."""
    
    data = data2[:]
    mode = "metric" if units_main["prec"] == "cm" else "imperial"
    
    # Convert everything to metric:
    if mode == "metric":
        
        # Temperature:
        if units[0].endswith("F"):
            data[0] = (float(data[0]) - 32) * (5 / 9)
        
        # Wind Chill:
        if units[1].endswith("F"):
            data[1] = (float(data[1]) - 32) * (5 / 9)
        
        # Precipitation:
        if units[2] == "in":
            data[2] = float(data[2]) * 2.54
        
        # Wind Speed:
        if units[3] == "mph":
            data[3] = float(data[3]) * 1.60934
        
        # Visibility:
        if units[4] == "mi":
            data[4] = float(data[4]) / 0.62137
    
    # Convert everything to imperial:
    elif mode == "imperial":
        
        # Temperature:
        if units[0].endswith("C"):
            data[0] = (float(data[0]) * (9 / 5)) + 32
        
        # Wind Chill:
        if units[1].endswith("C"):
            data[1] = (float(data[1]) * (9 / 5)) + 32
        
        # Precipitation:
        if units[2] == "cm":
            data[2] = float(data[2]) / 2.54
        
        # Wind Speed:
        if units[3] == "kph":
            data[3] = float(data[3]) / 1.60934
        
        # Visibility:
        if units[4] == "km":
            data[4] == float(data[4]) * 0.62137
    
    return data


def rgba_to_hex(rgba_color):
    """Converts RGBA as given by a GdkRGBA instance into hex."""
    
    red = int(rgba_color.red * 255)
    green = int(rgba_color.green * 255)
    blue = int(rgba_color.blue * 255)
    return "#{r:02x}{g:02x}{b:02x}".format(r = red,g = green,b = blue)
