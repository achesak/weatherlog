# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dates.py
# This module works with dates.
#
################################################################################


# Import datetime for date calculations.
import datetime
# Import date2num for converting dates to numbers.
try:
    from matplotlib.dates import date2num
except ImportError:
    date2num = None


def split_date(date):
    """Splits the date into it's components."""
    
    # Split the date.
    days, months, years = date.split("/")
    days = int(days)
    months = int(months) - 1
    years = int(years)
    return days, months, years


def date_list_datetime(dates):
    """Converts a list of dates (as dd/mm/yy) to datetimes."""
    
    datelist = []
    
    for i in dates:
        date_split = i.split("/")
        date = datetime.datetime(int(date_split[2]), int(date_split[1]), int(date_split[0]))
        datelist.append(date)
    
    return datelist


def date_above(date, datelist):
    """Returns the position of the date in datelist that's the least greatest than date. Returns -1 if not found."""
    
    # Calculate a list of date differences.
    delta_list = []
    for i in datelist:
        delta_list.append((i - date).total_seconds())
    
    index = -1
    for i in range(0, len(delta_list)):
        
        # If there is no difference, this index is an exact match.
        if delta_list[i] == 0:
            index = i
            break
        
        # If the difference is negative, this index is less.
        if delta_list[i] < 0:
            continue
        
        # If the difference is positive, this is the first index above.
        if delta_list[i] > 0:
            index = i
            break
    
    return index


def date_below(date, datelist):
    """Returns the position of the date in datelist that's the highest least than date. Returns -1 if not found."""
    
    # Calculate a list of date differences.
    delta_list = []
    for i in datelist:
        delta_list.append((date - i).total_seconds())
    
    index = -1
    for i in reversed(range(0, len(delta_list))):
        
        # If there is no difference, this index is an exact match.
        if delta_list[i] == 0:
            index = i
            break
        
        # If the difference if negative, this index is greater.
        if delta_list[i] < 0:
            continue
        
        # If the difference is positive, this is the first index below.
        if delta_list[i] > 0:
            index = i
            break
    
    return index


def get_datetimes(dates):
    """Changes the dates to the datetime representation."""
    
    new_dates = []
    for i in dates:
        new_dates.append(date2num(datetime.datetime.strptime(i, "%d/%m/%Y")))
    
    return new_dates
