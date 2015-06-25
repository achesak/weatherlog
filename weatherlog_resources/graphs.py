# -*- coding: utf-8 -*-


# This file defines the functions for getting the data for the graphs.


# Import datetime for date calculations.
import datetime

# Import the dataset functions.
import weatherlog_resources.datasets as datasets
# Import date2num for converting dates to numbers.
try:
    from matplotlib.dates import date2num
except ImportError:
	pass


def get_dates(dates):
    """Changes the dates to the datetime representation."""
    
    new_dates = []
    for i in dates:
        new_dates.append(date2num(datetime.datetime.strptime(i, "%d/%m/%Y")))
    
    return new_dates


def get_data(data):
    """Gets the graph data."""
    
    # Get the date data.
    date_data = datasets.get_column(data, 0)
    new_dates = get_dates(date_data)
    
    # Get the data.
    temp_data = datasets.convert_float(datasets.get_column(data, 1))
    chil_data = datasets.convert_float(datasets.get_column(data, 2))
    prec_data1, prec_data2 = datasets.split_list(datasets.get_column(data, 3))
    prec_data = datasets.convert_float(datasets.none_to_zero(prec_data1))
    wind_data1, wind_data2 = datasets.split_list(datasets.get_column(data, 4))
    wind_data = datasets.convert_float(datasets.none_to_zero(wind_data1))
    humi_data = datasets.convert_float(datasets.get_column(data, 5))
    airp_data1, airp_data2 = datasets.split_list(datasets.get_column(data, 6))
    airp_data = datasets.convert_float(airp_data1)
    visi_data = datasets.convert_float(datasets.get_column(data, 7))
    clou_data1, clou_data2 = datasets.split_list3(datasets.get_column(data, 8))
    clou_data2 = datasets.strip_items(clou_data2, ["(", ")"])
    
    prec_split = datasets.split_list2(datasets.get_column(data, 3))
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
    for i in clou_data1:
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
    
    clou_types = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in clou_data2:
        if i == "None":
            clou_types[0] += 1
        elif i == "Unknown":
            clou_types[1] += 1
        elif i == "Cirrus":
            clou_types[2] += 1
        elif i == "Cirrocumulus":
            clou_types[3] += 1
        elif i == "Cirrostratus":
            clou_types[4] += 1
        elif i == "Cumulonimbus":
            clou_types[5] += 1
        elif i == "Altocumulus":
            clou_types[6] += 1
        elif i == "Altostratus":
            clou_types[7] += 1
        elif i == "Stratus":
            clou_types[8] += 1
        elif i == "Cumulus":
            clou_types[9] += 1
        elif i == "Stratocumulus":
            clou_types[10] += 1
    
    data = [date_data, new_dates, temp_data, prec_data, wind_data, humi_data, airp_data, prec_amount,
            prec_days, airp_change, clou_days, clou_types, chil_data, visi_data]
    
    return data
