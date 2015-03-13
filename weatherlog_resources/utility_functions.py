# -*- coding: utf-8 -*-


# This file defines functions for various tasks.


# Import this so dividing works correctly.
from __future__ import division
# Import re for pattern matching.
import re
# Import os.path for checking if a directory exists.
import os.path


def extract_numbers(data):
    """Extracts the numbers from the list items."""
    
    # Loop through the list, getting the numbers and converting them to floats.
    numbers = data[:]
    for i in range(0, len(numbers)):
        numbers[i] = float(numbers[i].split()[0])
    return numbers


def convert_float(data):
    """Converts the list items to floats."""
    
    # Loop through the list, converting the items to floats.
    numbers = []
    for i in range(0, len(data)):
        if data[i] != "None":
            numbers.append(float(data[i]))
    return numbers


def get_column(data, col):
    """Gets a column of the data."""
    
    # Loop through the list, getting the specified value and appending it to the new list.
    column = []
    for i in data:
        column.append(i[col])
    return column
 

def split_list(data):
    """Splits the list items, and returns them as two lists. "None" is ignored."""
    
    # Loop through the list, splitting the items and adding them to the new lists.
    data2 = data[:]
    n_list1 = []
    n_list2 = []
    for i in data2:
        
        # Split the item and append the first one.
        i_split = i.split(" ")
        n_list1.append(i_split[0])
        
        # If the second one is "None", append an empty string.
        if i == "None":
            n_list2.append("")
        # Otherwise, append the second value.
        else:
            n_list2.append(i_split[1])
    
    return [n_list1, n_list2]


def split_list2(data):
    """Splits the list items, and returns them as lists within the main one. "None" is ignored."""
    
    # Loop through the list, splitting the items and adding them to the new list.
    data2 = data[:]
    n_list = []
    for i in data2:
        # If the value is "None" don't split it, but use an empty string as the first value.
        if i == "None":
            n_list.append(["", "None"])
        # Otherwise, split the value.
        else:
            n_list.append(i.split(" "))
    
    return n_list


def none_to_zero(data):
    """Changes any "None" values to "0" (zero)."""
    
    # Loop through the list, and change values as needed.
    n_list = []
    for i in data:
        if i == "None":
            n_list.append("0")
        else:
            n_list.append(i)
    return n_list


def split_date(date):
    """Splits the date into it's components."""
    
    # Split the date.
    days, months, years = date.split("/")
    days = int(days)
    months = int(months) - 1
    years = int(years)
    return (days, months, years)


def date_to_iso(day, month, year):
    """Formats a date in ISO notation."""
    
    return str(year) + "-" + (str(month) if month > 9 else "0" + str(month)) + "-" + (str(day) if day > 9 else "0" + str(day))


def validate_profile(main_dir, name):
    """Validates a profile name."""
    
    if re.compile("[^a-zA-Z1-90 \.\-\+\(\)\?\!]").match(name) or not name or name.lstrip().rstrip() == "" or name.startswith("."):
        return "The dataset name \"%s\" is not valid.\n\n1. Dataset names may not be blank.\n2. Dataset names may not be all spaces.\n3. Dataset names may only be letters, numbers, and spaces.\n4. Dataset names may not start with a period (\".\")." % name
    
    elif os.path.isdir("%s/profiles/%s" % (main_dir, name)):
        return "The dataset name \"%s\" is already in use." % name
    
    else:
        return ""


def validate_data(data):
    """Validates imported data."""
    
    # Test 1: must be a list.
    if not isinstance(data, list):
        return False
    
    # Test 2: each item must be a list.
    # Test 3: each item must have the correct length (8).
    # Test 4: each item of this list must be a string.
    for i in data:
        if not isinstance(i, list):
            return False
        if len(i) != 10:
            return False
        for j in i:
            if not isinstance(j, str):
                return False
    
    return True


def degree_to_direction(deg):
    """Convert degrees to wind direction."""
    
    # Each direction gets 22.5 degreees, or 11.25 degrees away from the exact direction.
    # For example, exact North is 0 degrees, but anything larger than or equal to 348.75
    # or smaller than 11.25 is also considered North.
    
    # N < 11.25
    if deg < 11.25:
        return "N"
    # 11.25 <= NNE < 33.75
    elif deg >= 11.25 and deg < 33.75:
        return "NNE"
    # 33.75 <= NE < 56.25
    elif deg >= 33.75 and deg < 56.25:
        return "NE"
    # 56.25 <= ENE < 78.75
    elif deg >= 56.25 and deg < 78.75:
        return "ENE"
    # 78.75 <= E < 101.25
    elif deg >= 78.75 and deg < 101.25:
        return "E"
    # 101.25 <= ESE < 123.75
    elif deg >= 101.25 and deg < 123.75:
        return "ESE"
    # 123.75 <= SE < 146.25
    elif deg >= 123.75 and deg < 146.25:
        return "SE"
    # 146.25 <= SSE < 168.75
    elif deg >= 146.25 and deg < 168.75:
        return "SSE"
    # 168.75 <= S < 191.25
    elif deg >= 168.75 and deg < 191.25:
        return "S"
    # 191.25 <= SSW < 213.75
    elif deg >= 191.25 and deg < 213.75:
        return "SSW"
    # 213.75 <= SW < 236.25
    elif deg >= 213.75 and deg < 236.25:
        return "SW"
    # 236.25 <= WSW < 258.75
    elif deg >= 236.25 and deg < 258.75:
        return "WSW"
    # 258.75 <= W < 281.25
    elif deg >= 258.75 and deg < 281.25:
        return "W"
    # 281.25 <= WNW < 303.75
    elif deg >= 281.25 and deg < 303.75:
        return "WNW"
    # 303.75 <= NW < 326.25
    elif deg >= 303.75 and deg < 326.25:
        return "NW"
    # 326.25 <= NNW < 348.75
    elif deg >= 326.25 and deg < 348.75:
        return "NNW"
    # 348.75 <= N
    else:
        return "N"


def convert(data2, units):
    """Converts the data."""
    
    data = data2[:]
    for i in range(0, len(data)):
        
        # Convert from imperial to metric:
        if units == "metric":
            
            # Convert the temperature.
            # C = 5/9(F + 32)
            data[i][1] = "%.2f" % ((float(data[i][1]) - 32) * (5 / 9))
            
            # Convert the precipitation amount.
            # cm = in * 2.54
            if data[i][2] != "None":
                split = data[i][2].split(" ")
                split[0] = "%.2f" % (float(split[0]) * 2.54)
                data[i][2] = " ".join(split)
            
            # Convert the wind speed.
            # kph = mph * 1.60934
            if data[i][3] != "None":
                split = data[i][3].split(" ")
                split[0] = "%.2f" % (float(split[0]) * 1.60934)
                data[i][3] = " ".join(split)
        
        # Convert from metric to imperial:
        elif units == "imperial":
            
            # Convert the temperature.
            # F = 9/5C + 32
            data[i][1] = "%.2f" % ((float(data[i][1]) * (9 / 5)) + 32)
            
            # Convert the precipitation amount.
            # in = cm / 2.54
            if data[i][2] != "None":
                split = data[i][2].split(" ")
                split[0] = "%.2f" % (float(split[0]) / 2.54)
                data[i][2] = " ".join(split)
            
            # Convert the wind speed.
            # mph = kph / 1.60934
            if data[i][3] != "None":
                split = data[i][3].split(" ")
                split[0] = "%.2f" % (float(split[0]) / 1.60934)
                data[i][3] = " ".join(split)
    
    return data
