# -*- coding: utf-8 -*-


# This file defines the functions for filtering the data based
# on the user-specified conditions.


# Import the dataset functions.
import weatherlog_resources.datasets as datasets
# Import datetime for sorting the data.
import datetime


# condition parameter is a list with the format:
# [field, operator, value]
def filter_data(data, condition, insensitive):
    """Filters the data based on the user's conditions."""
    
    # Create the list for the filtered data.
    filtered = []
    
    # Get the column of the data that is being filtered.
    string_compare = False
    col = []
    field = condition[0].lower()
    if field == "temperature":
        col = datasets.convert_float(datasets.get_column(data, 1))
    elif field == "wind chill":
        col = datasets.convert_float(datasets.get_column(data, 2))
    elif field == "precipitation amount":
        col = datasets.get_column(data, 3)
        col = datasets.convert_float(datasets.none_to_zero(datasets.split_list(col)[0]))
    elif field == "precipitation type":
        string_compare = True
        ncol = datasets.get_column(data, 3)
        col = []
        for i in ncol:
            if i == "None":
                col.append(i)
            else:
                i_split = i.split(" ")
                col.append(i_split[1])
    elif field == "wind speed":
        col = datasets.get_column(data, 4)
        col = datasets.convert_float(datasets.none_to_zero(datasets.split_list(col)[0]))
    elif field == "wind direction":
        string_compare = True
        ncol = datasets.get_column(data, 4)
        col = []
        for i in ncol:
            if i == "None":
                col.append(i)
            else:
                i_split = i.split(" ")
                col.append(i_split[1])
    elif field == "humidity":
        col = datasets.convert_float(datasets.get_column(data, 5))
    elif field == "air pressure":
        col = datasets.convert_float(datasets.split_list(datasets.get_column(data, 6))[0])
    elif field == "air pressure change":
        string_compare = True
        col = datasets.split_list(datasets.get_column(data, 6))[1]
    elif field == "visibility":
        col = datasets.convert_float(datasets.get_column(data, 7))
    elif field == "cloud cover":
        string_compare = True
        col = datasets.split_list3(datasets.get_column(data, 8))[0]
    elif field == "cloud type":
        string_compare = True
        col = datasets.strip_items(datasets.split_list3(datasets.get_column(data, 8))[1], ["(", ")"])
    elif field == "notes":
        string_compare = True
        col = datasets.get_column(data, 9)
    
    # Loop through the data, and add it to the filtered list if it matches the condition.
    for i in range(0, len(data)):
        matches = filter_compare(col[i], condition[1].lower(), condition[2], string_compare, insensitive)
        if matches:
            filtered.append(data[i])
    
    return filtered


def filter_compare(item, operator, value, string_compare, insensitive):
    """Checks whether the item matches the condition. Returns true if it does, and false otherwise."""
    
    # Remove all whitespace from the value and the item to compare.
    value = "".join(value.split())
    value = [value]
    # If there are multiple values specified, split them.
    if "," in value[0]:
        value = [x.strip() for x in value[0].split(',')]
    
    # If this is not a string comparison, convert the value(s) to floats.
    if not string_compare:
        for i in range(0, len(value)):
            value[i] = float(value[i])
    
    # If this is a string comparison and the user wants insensitive comparison, convert everything to lowercase.
    if string_compare and insensitive:
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
    
    # Compare the item: starts with
    if operator == "starts with":
        if item.startswith(value[0]):
            matches = True
    
    # Compare the item: does not start with
    if operator == "does not start with":
        if not item.startswith(value[0]):
            matches = True
    
    # Compare the item: ends with
    if operator == "ends with":
        if item.endswith(value[0]):
            matches = True
    
    # Compare the item: does not end with
    if operator == "does not end with":
        if not item.endswith(value[0]):
            matches = True
    
    # Compare the item: contains
    if operator == "contains":
        if value[0] in item:
            matches = True
    
    # Compare the item: does not contain
    if operator == "does not contain":
        if value[0] not in item:
            matches = True
    
    return matches


def filter_and(set1, set2):
    """Returns a list of the items that are in both set1 and set2."""
    
    # Get the date column of the second list for the comparison.
    filtered = []
    date_list = datasets.get_column(set2, 0)
    
    # Loop through the first set, and only add the item to the filtered list if it's also in the second set.
    for i in set1:
        if i[0] in date_list:
            filtered.append(i)
    
    return filtered


def filter_not(set1, data):
    """Returns a list of the items in data that are not in set1."""
    
    # Get the date column of the set for the comparison.
    filtered = []
    date_list = datasets.get_column(set1, 0)
    
    # Loop through the data list, and only add the item to the filtered list if it's not in the other set.
    for i in data:
        if i[0] not in date_list:
            filtered.append(i)
    
    return filtered


def filter_or(set1, set2):
    """Returns a list of the items that are in either set1 or set2."""
    
    # Get the date column of the first set for the comparison.
    date_list = datasets.get_column(set1, 0)
    
    # Loop through the second list, and add the item if it isn't already in the first list.
    filtered = set1[:]
    for i in set2:
        if i[0] not in date_list:
            filtered.append(i)
    
    filtered = sorted(filtered, key = lambda x: datetime.datetime.strptime(x[0], "%d/%m/%Y"))
    return filtered


def filter_quick(data, search_term, case_insensitive):
    """Filters the data based on a search term and given options."""
    
    filtered = []
    
    # Convert the case of the data if needed. TODO: this is quite inefficient
    if case_insensitive:
        new_data = []
        for row in data:
            new_data.append(map(str.lower, row))
    else:
        new_data = data[:]
        
    # Filter the data.
    for index in range(0, len(new_data)):
        if filter_quick_compare(new_data[index], search_term):
            filtered.append(data[index])
    
    return filtered


def filter_quick_compare(row, search_term):
    """Returns whether or not the search term is contained in the row for a quick search."""
    
    for item in row:
        if search_term in item:
            return True
