# -*- coding: utf-8 -*-


# This file defines the functions for getting the data for the graphs.


# Import datetime for date calculations.
import datetime

# Import the utility functions.
import weatherlog_resources.utility_functions as utility_functions
# Import date2num for converting dates to numbers.
from matplotlib.dates import date2num


def get_dates(dates):
    """Changes the dates to the datetime representation."""
    
    new_dates = []
    for i in dates:
        new_dates.append(date2num(datetime.datetime.strptime(i, "%d/%m/%Y")))
    
    return new_dates


def get_data(data):
    """Gets the graph data."""
    
    # Get the date data.
    date_data = utility_functions.get_column(data, 0)
    new_dates = get_dates(date_data)
    
    # Get the data.
    temp_data = utility_functions.convert_float(utility_functions.get_column(data, 1))
    prec_data1, prec_data2 = utility_functions.split_list(utility_functions.get_column(data, 2))
    prec_data = utility_functions.convert_float(utility_functions.none_to_zero(prec_data1))
    wind_data1, wind_data2 = utility_functions.split_list(utility_functions.get_column(data, 3))
    wind_data = utility_functions.convert_float(utility_functions.none_to_zero(wind_data1))
    humi_data = utility_functions.convert_float(utility_functions.get_column(data, 4))
    airp_data1, airp_data2 = utility_functions.split_list(utility_functions.get_column(data, 5))
    airp_data = utility_functions.convert_float(airp_data1)
    clou_data = utility_functions.get_column(data, 6)
    
    prec_split = utility_functions.split_list2(utility_functions.get_column(data, 2))
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
            prec_sleet += 1
    prec_amount = [prec_total_rain, prec_total_snow, prec_total_hail, prec_total_sleet]
    prec_days = [prec_none, prec_rain, prec_snow, prec_hail, prec_sleet]
    
    airp_steady = 0
    airp_rising = 0
    airp_falling = 0
    for i in airp_data2:
        if i == "Steady":
            airp_steady += 1
        elif i == "Rising":
            airp_rising += 1
        elif i == "Falling":
            airp_falling += 1
    airp_change = [airp_steady, airp_rising, airp_falling]
    
    clou_sunny = 0
    clou_msunny = 0
    clou_pcloudy = 0
    clou_mcloudy = 0
    clou_cloudy = 0
    for i in clou_data:
        if i == "Sunny":
            clou_sunny += 1
        elif i == "Mostly Sunny":
            clou_msunny += 1
        elif i == "Partly Cloudy":
            clou_pcloudy += 1
        elif i == "Mostly Cloudy":
            clou_mcloudy += 1
        elif i == "Cloudy":
            clou_cloudy += 1
    clou_days = [clou_sunny, clou_msunny, clou_pcloudy, clou_mcloudy, clou_cloudy]
    
    data = [date_data, new_dates, temp_data, prec_data, wind_data, humi_data, airp_data, prec_amount, prec_days, airp_change, clou_days]
    
    return data
