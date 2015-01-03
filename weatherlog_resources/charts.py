# -*- coding: utf-8 -*-


# This file defines the functions for getting the chart data.


# Import collections.Counter for getting the mode of the data.
from collections import Counter

# Import the utility functions.
import weatherlog_resources.utility_functions as utility_functions
# Import the info functions.
import weatherlog_resources.info_functions as info_functions


def temp_chart(data, units):
    """"Gets the temperature chart data."""
    
    # Get the data.
    temp_data = utility_functions.convert_float(utility_functions.get_column(data, 1))
    temp_low = min(temp_data)
    temp_high = max(temp_data)
    temp_avg = info_functions.mean(temp_data)
    temp_median = info_functions.median(temp_data)
    
    # Calculate and add the data.
    data2 = []
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
    
    return data2


def prec_chart(data, units):
    """"Gets the precipitation chart data."""
    
    # Get the data.
    prec_data1, prec_data2 = utility_functions.split_list(utility_functions.get_column(data, 2))
    prec_split = utility_functions.split_list2(utility_functions.get_column(data, 2))
    prec_data1 = utility_functions.none_to_zero(prec_data1)
    prec_data1 = utility_functions.convert_float(prec_data1)
    prec_low = min(prec_data1)
    prec_high = max(prec_data1)
    prec_avg = info_functions.mean(prec_data1)
    prec_median = info_functions.median(prec_data1)
    
    # Calculate and add the data.
    data2 = []
    for i in range(0, len(data)):
        
        prec = [data[i][0], "%.2f %s" % (prec_data1[i], units["prec"])]
        if prec_avg == prec_data1[i]:
            average = "Average Value"
        else:
            average = prec_avg - prec_data1[i]
            average = "%.2f %s %s" % (abs(average), units["prec"], "above" if prec_avg < prec_data1[i] else "below")
        prec.append(average)
        if prec_low == prec_data1[i]:
            low = "Lowest Value"
        else:
            low = prec_low - prec_data1[i]
            low = "%.2f %s %s" % (abs(low), units["prec"], "above" if prec_low < prec_data1[i] else "below")
        prec.append(low)
        if prec_high == prec_data1[i]:
            high = "Highest Value"
        else:
            high = prec_high - prec_data1[i]
            high = "%.2f %s %s" % (abs(high), units["prec"], "above" if prec_high < prec_data1[i] else "below")
        prec.append(high)
        if prec_median == prec_data1[i]:
            median = "Median Value"
        else:
            median = prec_median - prec_data1[i]
            median = "%.2f %s %s" % (abs(median), units["prec"], "above" if prec_median < prec_data1[i] else "below")
        prec.append(median)
        
        data2.append(prec)
    
    return data2


def wind_chart(data, units):
    """"Gets the wind chart data."""
    
    # Get the data.
    wind_data1, wind_data2 = utility_functions.split_list(utility_functions.get_column(data, 3))
    wind_data1 = utility_functions.none_to_zero(wind_data1)
    wind_data1 = utility_functions.convert_float(wind_data1)
    wind_low = min(wind_data1)
    wind_high = max(wind_data1)
    wind_avg = info_functions.mean(wind_data1)
    wind_median = info_functions.median(wind_data1)
    
    # Calculate and add the data.
    data2 = []
    for i in range(0, len(data)):
        
        wind = [data[i][0], "%.2f %s" % (wind_data1[i], units["wind"])]
        if wind_avg == wind_data1[i]:
            average = "Average Value"
        else:
            average = wind_avg - wind_data1[i]
            average = "%.2f %s %s" % (abs(average), units["wind"], "above" if wind_avg < wind_data1[i] else "below")
        wind.append(average)
        if wind_low == wind_data1[i]:
            low = "Lowest Value"
        else:
            low = wind_low - wind_data1[i]
            low = "%.2f %s %s" % (abs(low), units["wind"], "above" if wind_low < wind_data1[i] else "below")
        wind.append(low)
        if wind_high == wind_data1[i]:
            high = "Highest Value"
        else:
            high = wind_high - wind_data1[i]
            high = "%.2f %s %s" % (abs(high), units["wind"], "above" if wind_high < wind_data1[i] else "below")
        wind.append(high)
        if wind_median == wind_data1[i]:
            median = "Median Value"
        else:
            median = wind_median - wind_data1[i]
            median = "%.2f %s %s" % (abs(median), units["wind"], "above" if wind_median < wind_data1[i] else "below")
        wind.append(median)
        
        data2.append(wind)
    
    return data2


def humi_chart(data, units):
    """"Gets the humidity chart data."""
    
    # Get the data.
    humi_data = utility_functions.convert_float(utility_functions.get_column(data, 4))
    humi_low = min(humi_data)
    humi_high = max(humi_data)
    humi_avg = info_functions.mean(humi_data)
    humi_median = info_functions.median(humi_data)
    
    # Calculate and add the data.
    data2 = []
    for i in range(0, len(data)):
        
        humi = [data[i][0], "%.2f%%" % (humi_data[i])]
        if humi_avg == humi_data[i]:
            average = "Average Value"
        else:
            average = humi_avg - humi_data[i]
            average = "%.2f%% %s" % (abs(average), "above" if humi_avg < humi_data[i] else "below")
        humi.append(average)
        if humi_low == humi_data[i]:
            low = "Lowest Value"
        else:
            low = humi_low - humi_data[i]
            low = "%.2f%% %s" % (abs(low), "above" if humi_low < humi_data[i] else "below")
        humi.append(low)
        if humi_high == humi_data[i]:
            high = "Highest Value"
        else:
            high = humi_high - humi_data[i]
            high = "%.2f%% %s" % (abs(high), "above" if humi_high < humi_data[i] else "below")
        humi.append(high)
        if humi_median == humi_data[i]:
            median = "Median Value"
        else:
            median = humi_median - humi_data[i]
            median = "%.2f%% %s" % (abs(median), "above" if humi_median < humi_data[i] else "below")
        humi.append(median)
        
        data2.append(humi)
    
    return data2


def airp_chart(data, units):
    """"Gets the air pressure chart data."""
    
    # Get the data.
    airp_data1, airp_data2 = utility_functions.split_list(utility_functions.get_column(data, 5))
    airp_data1 = utility_functions.convert_float(airp_data1)
    airp_low = min(airp_data1)
    airp_high = max(airp_data1)
    airp_avg = info_functions.mean(airp_data1)
    airp_median = info_functions.median(airp_data1)
    
    # Calculate and add the data.
    data2 = []
    for i in range(0, len(data)):
        
        airp = [data[i][0], "%.2f %s" % (airp_data1[i], units["airp"])]
        if airp_avg == airp_data1[i]:
            average = "Average Value"
        else:
            average = airp_avg - airp_data1[i]
            average = "%.2f %s %s" % (abs(average), units["airp"], "above" if airp_avg < airp_data1[i] else "below")
        airp.append(average)
        if airp_low == airp_data1[i]:
            low = "Lowest Value"
        else:
            low = airp_low - airp_data1[i]
            low = "%.2f %s %s" % (abs(low), units["airp"], "above" if airp_low < airp_data1[i] else "below")
        airp.append(low)
        if airp_high == airp_data1[i]:
            high = "Highest Value"
        else:
            high = airp_high - airp_data1[i]
            high = "%.2f %s %s" % (abs(high), units["airp"], "above" if airp_high < airp_data1[i] else "below")
        airp.append(high)
        if airp_median == airp_data1[i]:
            median = "Median Value"
        else:
            median = airp_median - airp_data1[i]
            median = "%.2f %s %s" % (abs(median), units["airp"], "above" if airp_median < airp_data1[i] else "below")
        airp.append(median)
        
        data2.append(airp)
    
    return data2
