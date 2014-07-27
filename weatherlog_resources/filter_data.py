# -*- coding: utf-8 -*-


# This file defines the functions for filtering the data based
# on the user-specified conditions.


# Import the utility functions.
import utility_functions
# Import datetime for sorting the data.
import datetime


# condition parameter is a list with the format:
# [field, operator, value]
def filter_data(data, condition):
    """Filters the data based on the user's conditions."""
    
    # Create the list for the filtered data.
    filtered = []
    
    # Get the column of the data that is being filtered.
    string_compare = False
    col = []
    if condition[0] == "temperature":
        col = utility_functions.convert_float(utility_functions.get_column(data, 1))
    elif condition[0] == "precipitation amount":
        col = utility_functions.get_column(data, 2)
        col = utility_functions.convert_float(utility_functions.none_to_zero(utility_functions.split_list(col)[0]))
    elif condition[0] == "precipitation type":
        string_compare = True
        ncol = utility_functions.get_column(data, 2)
        col = []
        for i in ncol:
            if i == "None":
                col.append(i)
            else:
                i_split = i.split(" ")
                col.append(i_split[1])
    elif condition[0] == "wind speed":
        col = utility_functions.get_column(data, 3)
        col = utility_functions.convert_float(utility_functions.none_to_zero(utility_functions.split_list(col)[0]))
    elif condition[0] == "wind direction":
        string_compare = True
        ncol = utility_functions.get_column(data, 3)
        col = []
        for i in ncol:
            if i == "None":
                col.append(i)
            else:
                i_split = i.split(" ")
                col.append(i_split[1])
    elif condition[0] == "humidity":
        col = utility_functions.convert_float(utility_functions.get_column(data, 4))
    elif condition[0] == "air pressure":
        col = utility_functions.convert_float(utility_functions.split_list(utility_functions.get_column(data, 5))[0])
    elif condition[0] == "air pressure change":
        string_compare = True
        col = utility_functions.split_list(utility_functions.get_column(data, 5))[1]
    elif condition[0] == "cloud cover":
        string_compare = True
        col = utility_functions.get_column(data, 6)
    
    # Loop through the data, and add it to the filtered list if it matches the condition.
    for i in range(0, len(data)):
        matches = filter_compare(col[i], condition[1], condition[2], string_compare)
        if matches:
            filtered.append(data[i])
    
    return filtered


def filter_compare(item, operator, value, string_compare):
    """Checks whether the item matches the condition. Returns true if it does, and false otherwise."""
    
    # Remove all whitespace from the value and the item to compare.
    value = "".join(value.split())
    value = [value]
    
    # If there are multiple values specified, split them.
    if "," in value[0]:
        value = value[0].split(",")
    
    # If this is not a string comparison, convert the value(s) to floats.
    if not string_compare:
        for i in range(0, len(value)):
            value[i] = float(value[i])
    
    # If this is a string comparison, convert everything to lowercase.
    if string_compare:
        for i in range(0, len(value)):
            value[i] = value[i].lower()
        item = "".join(item.split())
        item = item.lower()
    
    matches = False
    
    # Compare the item: equal to.
    if operator == "equal to":
        for i in value:
            if item == i:
                matches = True
    
    # Compare the item: not equal to.
    if operator == "not equal to":
        for i in value:
            if item != i:
                matches = True
    
    # Compare the item: greater than.
    if operator == "greater than":
        if item > value[0]:
            matches = True
    
    # Compare the item: less than.
    if operator == "less than":
        if item < value[0]:
            matches = True
    
    # Compare the item: greater than or equal to.
    if operator == "greater than or equal to":
        if item >= value[0]:
            matches = True
    
    # Compare the item: less than or equal to.
    if operator == "less than or equal to":
        if item <= value[0]:
            matches = True
    
    # Compare the item: between.
    if operator == "between":
        if item > value[0] and item < value[1]:
            matches = True
    
    # Compare the item: between (inclusive).
    if operator == "between (inclusive)":
        if item >= value[0] and item <= value[1]:
            matches = True
    
    # Compare the item: outside.
    if operator == "outside":
        if item < value[0] or item > value[1]:
            matches = True
    
    # Compare the item: outside (inclusive).
    if operator == "outside (inclusive)":
        if item <= value[0] or item >= value[1]:
            matches = True
    
    return matches


def filter_and(set1, set2):
    """Returns a list of the items that are in both set1 and set2."""
    
    # Get the date column of the second list for the comparison.
    filtered = []
    date_list = utility_functions.get_column(set2, 0)
    
    # Loop through the first set, and only add the item to the filtered list if it's also in the second set.
    for i in set1:
        if i[0] in date_list:
            filtered.append(i)
    
    return filtered


def filter_not(set1, data):
    """Returns a list of the items in data that are not in set1."""
    
    # Get the date column of the set for the comparison.
    filtered = []
    date_list = utility_functions.get_column(set1, 0)
    
    # Loop through the data list, and only add the item to the filtered list if it's not in the other set.
    for i in data:
        if i[0] not in date_list:
            filtered.append(i)
    
    return filtered


def filter_or(set1, set2):
    """Returns a list of the items that are in either set1 or set2."""
    
    # Get the date column of the first set for the comparison.
    date_list = utility_functions.get_column(set1, 0)
    
    # Set the filtered list to all of the items of the first set.
    filtered = set1[:]
    
    # Loop through the second list, and add the item if it isn't already in the first list.
    for i in set2:
        if i[0] not in date_list:
            filtered.append(i)
    
    # Sort the filtered list.
    filtered = sorted(filtered, key = lambda x: datetime.datetime.strptime(x[0], "%d/%m/%Y"))
    
    return filtered
