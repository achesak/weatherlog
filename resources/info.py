# -*- coding: utf-8 -*-


# This file defines the functions for getting the info.


# Import datetime for date calculations.
import datetime
# Import collections.Counter for getting the mode of the data.
from collections import Counter

# Import the utility functions.
import utility_functions
# Import the info functions.
import info_functions


def general_info(data, units):
    """Gets the general info."""
    
    # Get the date data.
    date_data = utility_functions.get_column(data, 0)
    date_first = date_data[0]
    date_last = date_data[len(date_data) - 1]
    date_first2 = datetime.datetime.strptime(date_first, "%d/%m/%Y")
    date_last2 = datetime.datetime.strptime(date_last, "%d/%m/%Y")
    date_num = (date_last2 - date_first2).days + 1
    day_num = len(data)
    
    # Get the temperature data.
    temp_data = utility_functions.convert_float(utility_functions.get_column(data, 1))
    temp_low = min(temp_data)
    temp_high = max(temp_data)
    temp_avg = info_functions.mean(temp_data)
    
    # Get the precipitation data.
    prec_data1, prec_data2 = utility_functions.split_list(utility_functions.get_column(data, 2))
    prec_data1 = utility_functions.convert_float(utility_functions.none_to_zero(prec_data1))
    try:
        prec_low = min(prec_data1)
        prec_high = max(prec_data1)
        prec_avg = info_functions.mean(prec_data1)
    except:
        prec_low = "None"
        prec_high = "None"
        prec_avg = "None"
    
    # Get the wind data.
    wind_data1, wind_data2 = utility_functions.split_list(utility_functions.get_column(data, 3))
    wind_data1 = utility_functions.convert_float(utility_functions.none_to_zero(wind_data1))
    try:
        wind_low = min(wind_data1)
        wind_high = max(wind_data1)
        wind_avg = info_functions.mean(wind_data1)
    except:
        wind_low = "None"
        wind_high = "None"
        wind_avg = "None"
    
    # Get the humidity data.
    humi_data = utility_functions.convert_float(utility_functions.get_column(data, 4))
    humi_low = min(humi_data)
    humi_high = max(humi_data)
    humi_avg = info_functions.mean(humi_data)
    
    # Get the air pressure data.
    airp_data1, airp_data2 = utility_functions.split_list(utility_functions.get_column(data, 5))
    airp_data1 = utility_functions.convert_float(airp_data1)
    airp_low = min(airp_data1)
    airp_high = max(airp_data1)
    airp_avg = info_functions.mean(airp_data1)
    
    # Get the cloud cover data.
    clou_data = Counter(utility_functions.get_column(data, 6))
    clou_mode = clou_data.most_common(1)[0][0]
    
    # Change any values, if needed.
    prec_low = "None" if prec_low == "None" else ("%.2f %s" % (prec_low, units["prec"]))
    prec_high = "None" if prec_high == "None" else ("%.2f %s" % (prec_high, units["prec"]))
    prec_avg = "None" if prec_avg == "None" else ("%.2f %s" % (prec_avg, units["prec"]))
    wind_low = "None" if wind_low == "None" else ("%.2f %s" % (wind_low, units["wind"]))
    wind_high = "None" if wind_high == "None" else ("%.2f %s" % (wind_high, units["wind"]))
    wind_avg = "None" if wind_avg == "None" else ("%.2f %s" % (wind_avg, units["wind"]))
    
    # Create the data list.
    data2 = [
        ["First day", "%s" % date_first],
        ["Last day", "%s" % date_last],
        ["Number of days", "%d" % day_num],
        ["Range of days", "%d" % date_num],
        ["Lowest temperature", "%.2f %s" % (temp_low, units["temp"])], 
        ["Highest temperature", "%.2f %s" % (temp_high, units["temp"])],
        ["Average temperature", "%.2f %s" % (temp_avg, units["temp"])],
        ["Lowest precipitation", prec_low],
        ["Highest precipitation", prec_high],
        ["Average precipitation", prec_avg],
        ["Lowest wind speed", wind_low],
        ["Highest wind speed", wind_high],
        ["Average wind speed", wind_avg],
        ["Lowest humidity", "%.2f%%" % humi_low], 
        ["Highest humidity", "%.2f%%" % humi_high],
        ["Average humidity", "%.2f%%" % humi_avg],
        ["Lowest air pressure", "%.2f %s" % (airp_low, units["airp"])],
        ["Highest air pressure", "%.2f %s" % (airp_high, units["airp"])],
        ["Average air pressure", "%.2f %s" % (airp_avg, units["airp"])],
        ["Most common cloud cover", "%s" % clou_mode]
    ]
    
    # Return the data list.
    return data2


def temp_info(data, units):
    """"Gets the temperature info."""
    
    # Get the data.
    temp_data = utility_functions.convert_float(utility_functions.get_column(data, 1))
    temp_low = min(temp_data)
    temp_high = max(temp_data)
    temp_avg = info_functions.mean(temp_data)
    temp_median = info_functions.median(temp_data)
    temp_range = info_functions.range(temp_data)
    temp_mode = info_functions.mode(temp_data)
    
    # Create the data list.
    data2 = [
        ["Lowest", "%.2f %s" % (temp_low, units["temp"])],
        ["Highest", "%.2f %s" % (temp_high, units["temp"])],
        ["Average", "%.2f %s" % (temp_avg, units["temp"])],
        ["Median", "%.2f %s" % (temp_median, units["temp"])],
        ["Range", "%.2f %s" % (temp_range, units["temp"])],
        ["Most common", "%.2f %s" % (temp_mode, units["temp"])]
    ]
    
    # Return the data list.
    return data2


def prec_info(data, units):
    """"Gets the precipitation info."""
    
    # Get the data.
    prec_data1, prec_data2 = utility_functions.split_list(utility_functions.get_column(data, 2))
    prec_split = utility_functions.split_list2(utility_functions.get_column(data, 2))
    prec_data1 = utility_functions.none_to_zero(prec_data1)
    prec_data1 = utility_functions.convert_float(prec_data1)
    try:
        prec_low = min(prec_data1)
        prec_high = max(prec_data1)
        prec_avg = info_functions.mean(prec_data1)
        prec_median = info_functions.median(prec_data1)
        prec_range = info_functions.range(prec_data1)
    except:
        prec_low = "None"
        prec_high = "None"
        prec_avg = "None"
        prec_median = "None"
        prec_range = "None"
    prec_total = 0
    prec_total_rain = 0
    prec_total_snow = 0
    prec_total_hail = 0
    prec_total_sleet = 0
    prec_none = 0
    prec_rain = 0
    prec_snow = 0
    prec_hail = 0
    prec_sleet = 0
    for i in prec_split:
        if i[1] != "None":
            prec_total += float(i[0])
        if i[1] == "None":
            prec_none += 1
        elif i[1] == "Rain":
            prec_total_rain += float(i[0])
            prec_rain += 1
        elif i[1] == "Snow":
            prec_total_snow += float(i[0])
            prec_snow += 1
        elif i[1] == "Hail":
            prec_total_hail += float(i[0])
            prec_hail += 1
        elif i[1] == "Sleet":
            prec_total_sleet += float(i[0])
            prec_hail += 1
    prec_mode = info_functions.mode(prec_data2)
    
    # Change any values, if needed.
    prec_low = "None" if prec_low == "None" else ("%.2f %s" % (prec_low, units["prec"]))
    prec_high = "None" if prec_high == "None" else ("%.2f %s" % (prec_high, units["prec"]))
    prec_avg = "None" if prec_avg == "None" else ("%.2f %s" % (prec_avg, units["prec"]))
    prec_median = "None" if prec_median == "None" else ("%.2f %s" % (prec_median, units["prec"]))
    prec_range = "None" if prec_range == "None" else ("%.2f %s" % (prec_range, units["prec"]))
    
    # Create the data list.
    data2 = [
        ["Lowest", prec_low],
        ["Highest", prec_high],
        ["Average", prec_avg],
        ["Median", prec_median],
        ["Range", prec_range],
        ["Total (all)", "%.2f %s" % (prec_total, units["prec"])],
        ["Total (rain)", "%.2f %s" % (prec_total_rain, units["prec"])],
        ["Total (snow)", "%.2f %s" % (prec_total_snow, units["prec"])],
        ["Total (hail)", "%.2f %s" % (prec_total_hail, units["prec"])],
        ["Total (sleet)", "%.2f %s" % (prec_total_sleet, units["prec"])],
        ["None", "%d day%s" % (prec_none, "" if prec_none == 1 else "s")],
        ["Rain", "%d day%s" % (prec_rain, "" if prec_rain == 1 else "s")],
        ["Snow", "%d day%s" % (prec_snow, "" if prec_snow == 1 else "s")],
        ["Hail", "%d day%s" % (prec_hail, "" if prec_hail == 1 else "s")],
        ["Sleet", "%d day%s" % (prec_sleet, "" if prec_sleet == 1 else "s")],
        ["Most common type", "%s" % (prec_mode if prec_mode != "" else "None")]
    ]
    
    # Return the data list.
    return data2
