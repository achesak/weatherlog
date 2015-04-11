# -*- coding: utf-8 -*-


# This file defines functions working with datasets.


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
    n_list1 = []
    n_list2 = []
    for i in data:
        
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
    n_list = []
    for i in data:
        # If the value is "None" don't split it, but use an empty string as the first value.
        if i == "None":
            n_list.append(["", "None"])
        # Otherwise, split the value.
        else:
            n_list.append(i.split(" "))
    
    return n_list


def split_list3(data):
    """Splits the list items, and returns them as two lists.
    
    The last split part of each item is the second part, and all others are joined into the first."""
    
    # Loop through the list, splitting the items and adding them to the new lists.
    n_list1 = []
    n_list2 = []
    for i in data:
        
        # Split the item and rejoin as needed.
        i_split = i.split(" ")
        i1 = i_split[0]
        i2 = i_split[len(i_split) - 1]
        if len(i_split) > 2:
            i1 = " ".join(i_split[:-1])
        n_list1.append(i1)
        n_list2.append(i2)
    
    return [n_list1, n_list2]


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


def strip_items(data, chars):
    """Strips the specified characters from the start and end of the list items."""
    
    n_list = []
    for i in data:
        for j in chars:
            if i.startswith(j):
                i = i[1:]
            if i.endswith(j):
                i = i[:-1]
        n_list.append(i)
    return n_list
