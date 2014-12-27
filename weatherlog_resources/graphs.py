# -*- coding: utf-8 -*-


# This file defines the functions for getting the data for the graphs.


# Import datetime for date calculations.
import datetime

# Import the utility functions.
import utility_functions
# Import the info functions.
import info_functions
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
    data = [date_data, new_dates, temp_data, prec_data, wind_data, humi_data, airp_data]
    
    return data
