# -*- coding: utf-8 -*-


# This file defines functions working with datasets.


def convert_float(data):
    """Converts the list items to floats."""
    
    return [float(x) for x in data if x != "None"]


def get_column(data, col):
    """Gets a column of the data."""
    
    return [x[col] for x in data]
 

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
    
    return [x if x != "None" else "0" for x in data]


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
