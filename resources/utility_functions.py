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
    # Make a copy of the data. The original list should be unmodified.
    numbers = data[:]
    # Loop through the list, converting the items to floats.
    for i in range(0, len(numbers)):
        numbers[i] = float(numbers[i])
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
    """Splits the list items, and returns them as two lists."""
    # Make a copy of the data. The original list should be unmodified.
    data2 = data[:]
    # Create the new lists.
    n_list1 = []
    n_list2 = []
    # Loop through the list, splitting the items and adding them to the new lists.
    for i in data2:
        i_split = i.split(" ")
        n_list.append(i_split[0])
        n_list.append(i_split[1])
    # Return the new lists.
    return [n_list1, n_list2]