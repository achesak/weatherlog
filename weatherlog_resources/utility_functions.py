# -*- coding: utf-8 -*-


# This file defines functions for various tasks.


# Import re for pattern matching.
import re
# Import os.path for checking if a directory exists.
import os.path


def extract_numbers(data):
    """Extracts the numbers from the list items."""
    
    # Make a copy of the data. The original list should be unmodified.
    numbers = data[:]
    
    # Loop through the list, getting the numbers and converting them to floats.
    for i in range(0, len(numbers)):
        numbers[i] = float(numbers[i].split()[0])
    
    # Return the converted list.
    return numbers


def convert_float(data):
    """Converts the list items to floats."""
    
    # Loop through the list, converting the items to floats.
    numbers = []
    for i in range(0, len(data)):
        
        # If the item is "None", skip it.
        if data[i] != "None":
            numbers.append(float(data[i]))
    
    # Return the converted list.
    return numbers


def get_column(data, col):
    """Gets a column of the data."""
    
    # Loop through the list, getting the specified value and appending it to the new list.
    column = []
    for i in data:
        column.append(i[col])
    
    # Return the column.
    return column
 

def split_list(data):
    """Splits the list items, and returns them as two lists. "None" is ignored."""
    
    # Make a copy of the data. The original list should be unmodified.
    data2 = data[:]
    
    # Create the new lists.
    n_list1 = []
    n_list2 = []
    
    # Loop through the list, splitting the items and adding them to the new lists.
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
    
    # Return the new lists.
    return [n_list1, n_list2]


def split_list2(data):
    """Splits the list items, and returns them as lists within the main one. "None" is ignored."""
    
    # Make a copy of the data. The original list should be unmodified.
    data2 = data[:]
    
    # Create the new list.
    n_list = []
    
    # Loop through the list, splitting the items and adding them to the new list.
    for i in data2:
        
        # If the value is "None" don't split it, but use an empty string as the first value.
        if i == "None":
            n_list.append(["", "None"])
        
        # Otherwise, split the value.
        else:
            n_list.append(i.split(" "))
    
    # Return the new list.
    return n_list


def none_to_zero(data):
    """Changes any "None" values to "0" (zero)."""
    
    # Create the new list.
    n_list = []
    
    # Loop through the list, and change values as needed.
    for i in data:
        
        # If the value is "None", change it to "0".
        if i == "None":
            n_list.append("0")
        
        # Otherwise, append it as is.
        else:
            n_list.append(i)
    
    # Return the new list.
    return n_list


def split_date(date):
    """Splits the date into it's components."""
    
    # Split the date
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
        
        return "The profile name \"%s\" is not valid.\n\n1. Profile names may not be blank.\n2. Profile names may not be all spaces.\n3. Profile names may only be letters, numbers, and spaces.\n4. Profile names may not start with a period (\".\")." % name
    
    elif os.path.isdir("%s/profiles/%s" % (main_dir, name)):
        
        return "The profile name \"%s\" is already in use." % name
    
    else:
        
        return ""
