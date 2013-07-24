# -*- coding: utf-8 -*-


# This file defines the function to converting data to different units.


# THIS IS NOT YET DONE! IT NEEDS TO HANDLE STRINGS, None VALUES, AND DIRECTION/TYPE COLUMNS.


def convert(data2, units):
    """Converts the data."""
    
    # Make a copy of the data. The original list should remain unchanged.
    data = data2[:]
    
    # Convert the temperature.
    # Metric to imperial:
    if units == "imperial":
        
        for i in range(0, len(data[1])):
            data[1][i] = float("%.2f" % (data[1][i] * (9 / 5)) + 32)
    
    # Imperial to metric:
    elif units == "metric":
        
        for i in range(0, len(data[1])):
            data[1][i] = float("%.2f" % (data[1][i] - 32) * (5 / 9))
    
    # Convert the precipitation.
    # Metric to imperial:
    if units == "imperial":
        
        for i in range(0, len(data[2])):
            data[2][i] = float("%.2f" % data[2][i] / 2.54)
    
    # Imperial to metric:
    elif units == "metric":
        
        for i in range(0, len(data[2])):
            data[2][i] = float("%.2f" % data[2][i] * 2.54)
    
    # Convert the wind.
    # Metric to imperial:
    if units == "imperial":
        
        for i in range(0, len(data[3])):
            data[3][i] = float("%.2f" % data[3][i] / 1.60934)
    
    # Imperial to metric:
    elif units == "metric":
        
        for i in range(0, len(data[3])):
            data[3][i] = float("%.2f" % data[3][i] * 1.60934)
    
    # Return the new data.
    return data
