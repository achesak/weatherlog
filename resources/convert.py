# -*- coding: utf-8 -*-


# This file defines the function to converting data to different units.


# Import this so dividing works correctly.
from __future__ import division


def convert(data2, units):
    """Converts the data."""
    
    # Make a copy of the data. The original list should remain unchanged.
    data = data2[:]
    
    # Convert the temperature.
    # Metric to imperial:
    if units == "imperial":
        
        for i in range(0, len(data)):
            
            # Celsius to Fahrenheit:
            # F = 9/5C + 32
            data[i][1] = "%.2f" % ((float(data[i][1]) * (9 / 5)) + 32)
    
    # Imperial to metric:
    elif units == "metric":
        
        for i in range(0, len(data)):
            
            # Fahrenheit to Celsius:
            # C = 5/9(F + 32)
            data[i][1] = "%.2f" % ((float(data[i][1]) - 32) * (5 / 9))
    
    # Convert the precipitation.
    # Metric to imperial:
    if units == "imperial":
        
        for i in range(0, len(data)):
            
            # Centimeters to inches:
            # in = cm / 2.54
            # Skip "None" values.
            if data[i][2] != "None":
                
                split = data[i][2].split(" ")
            
                split[0] = "%.2f" % (float(split[0]) / 2.54)
                
                data[i][2] = " ".join(split)
    
    # Imperial to metric:
    elif units == "metric":
        
        for i in range(0, len(data)):
            
            # Inches to centimeters:
            # cm = in * 2.54
            # Skip "None" values.
            if data[i][2] != "None":
                
                split = data[i][2].split(" ")
            
                split[0] = "%.2f" % (float(split[0]) * 2.54)
                
                data[i][2] = " ".join(split)
    
    # Convert the wind.
    # Metric to imperial:
    if units == "imperial":
        
        for i in range(0, len(data)):
            
            # Kilometers per hour to miles per hour:
            # mph = kph / 1.60934
            # Skip "None" values.
            if data[i][3] != "None":
                
                split = data[i][3].split(" ")
            
                split[0] = "%.2f" % (float(split[0]) / 1.60934)
                
                data[i][3] = " ".join(split)
    
    # Imperial to metric:
    elif units == "metric":
        
        for i in range(0, len(data)):
            
            # Miles per hour to kilometers per hour:
            # kph = mph * 1.60934
            # Skip "None" values.
            if data[i][3] != "None":
                
                split = data[i][3].split(" ")
            
                split[0] = "%.2f" % (float(split[0]) * 1.60934)
                
                data[i][3] = " ".join(split)
    
    # Return the new data.
    return data
