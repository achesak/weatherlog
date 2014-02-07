# -*- coding: utf-8 -*-


# This file defines the functions for getting the chart data.


# Import collections.Counter for getting the mode of the data.
from collections import Counter

# Import the utility functions.
import utility_functions
# Import the info functions.
import info_functions


def temp_chart(data, units):
    """"Gets the temperature chart data."""
    
    # Get the data.
    temp_data = utility_functions.convert_float(utility_functions.get_column(data, 1))
    temp_low = min(temp_data)
    temp_high = max(temp_data)
    temp_avg = info_functions.mean(temp_data)
    temp_median = info_functions.median(temp_data)
    
    # Create the data list.
    data2 = []
    
    # Calculate and add the data.
    for i in range(0, len(data)):
        
        temp = [data[i][0], "%.2f %s" % (temp_data[i], units["temp"])]
        if temp_avg == temp_data[i]:
            average = "Average Value"
        else:
            average = temp_avg - temp_data[i]
            average = "%.2f %s %s" % (abs(average), units["temp"], "above" if temp_avg < temp_data[i] else "below")
        temp.append(average)
        if temp_low == temp_data[i]:
            low = "Lowest Value"
        else:
            low = temp_low - temp_data[i]
            low = "%.2f %s %s" % (abs(low), units["temp"], "above" if temp_low < temp_data[i] else "below")
        temp.append(low)
        if temp_high == temp_data[i]:
            high = "Highest Value"
        else:
            high = temp_high - temp_data[i]
            high = "%.2f %s %s" % (abs(high), units["temp"], "above" if temp_high < temp_data[i] else "below")
        temp.append(high)
        if temp_median == temp_data[i]:
            median = "Median Value"
        else:
            median = temp_median - temp_data[i]
            median = "%.2f %s %s" % (abs(median), units["temp"], "above" if temp_median < temp_data[i] else "below")
        temp.append(median)
        
        data2.append(temp)
    
    # Return the data list.
    return data2
