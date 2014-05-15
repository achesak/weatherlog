# -*- coding: utf-8 -*-


# This file defines the functions for filtering the data based
# on the user-specified conditions.


# Import the utility functions.
import utility_functions


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
    
    # If the column that is being compared is precipitation type, wind direction, air pressure change, 
    # or cloud cover, and the comparison is numerical, don't continue.
    if condition[0] == "precipitation type" or condition[0] == "wind direction" or condition[0] == "air pressure change" or condition[0] == "cloud cover":
        if condition[1] != "equal to" and condition[1] != "not equal to":
            return False
    
    # Loop through the data, and add it to the filtered list if it matches the condition.
    for i in range(0, len(data)):
        
        # Check if the item matches the criteria, and add it to the filtered list if it does.
        matches = filter_compare(col[i], condition[1], condition[2], string_compare)
        if matches:
            filtered.append(data[i])
    
    # Return the filtered list.
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
        
        # Check if the item is equal to the value(s).
        for i in value:
            if item == i:
                matches = True
    
    # Compare the item: not equal to.
    if operator == "not equal to":
        
        # Check if the item is not equal to the value(s).
        for i in value:
            if item != i:
                matches = True
    
    # Compare the item: greater than.
    if operator == "greater than":
        
        # Check if the item is greater than the value.
        if item > value[0]:
            matches = True
    
    # Compare the item: less than.
    if operator == "less than":
        
        # Check if the item is less than the value.
        if item < value[0]:
            matches = True
    
    # Compare the item: greater than or equal to.
    if operator == "greater than or equal to":
        
        # Check if the item is greater than or equal to the value.
        if item >= value[0]:
            matches = True
    
    # Compare the item: less than or equal to.
    if operator == "less than or equal to":
        
        # Check if the item is less than or equal to the value.
        if item <= value[0]:
            matches = True
    
    # Compare the item: between.
    if operator == "between":
        
        # Check if the item is between the values.
        if item > value[0] and item < value[1]:
            matches = True
    
    # Compare the item: between (inclusive).
    if operator == "between (inclusive)":
        
        # Check if the item is between or equal to the values.
        if item >= value[0] and item <= value[1]:
            matches = True
    
    # Compare the item: outside.
    if operator == "outside":
        
        # Check if the item is outside the values.
        if item < value[0] or item > value[1]:
            matches = True
    
    # Compare the item: outside (inclusive).
    if operator == "outside (inclusive)":
        
        # Check if the item is outside or equal to the values.
        if item <= value[0] or item >= value[1]:
            matches = True
    
    # Return whether the item matches the condition.
    return matches
