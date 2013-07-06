# -*- coding: utf-8 -*-


# This file defines functions for various tasks.


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
        i_split = i.split(" ")
        n_list1.append(i_split[0])
        
        if i == "None":
            n_list2.append("")
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
        
        if i == "None":
            n_list.append(["", "None"])
        else:
            n_list.append(i.split(" "))
    
    # Return the new list.
    return n_list


def filter_none(data1, data2):
    """Filters items out of the first list when the corrosponding value in the second list is None."""
    
    # Create the new list.
    n_list = []
    
    # Loop through the list, only appending items if the second item isn't None.
    for i in range(0, len(data1)):
        if data1[i] != "None":
            n_list.append(data1[i])
    
    # Return the new list.
    return n_list