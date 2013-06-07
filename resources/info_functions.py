# -*- coding: utf-8 -*-


# This file defines functions used for getting the data.


# Import the math module.
import math
# Import the collections module.
import collections


def mean(numbers):
    """Finds the mean of a list of numbers."""
    
    # Add the numbers
    total = 0
    for i in numbers:
        total += i
    
    # Divide by the length of the list.
    return total / len(numbers)


def median(numbers):
    """Finds the median of a list of numbers."""
    
    # Sort the list.
    numbers.sort()
    
    # If the list has an odd number of items:
    if not len(numbers) % 2:
        return numbers[int(math.floor(len(numbers) / 2))];
    
    # If the list has an even number of items:
    else:
        return (numbers[len(numbers) / 2] + numbers[(len(numbers) / 2) - 1]) / 2;


def range(numbers):
    """Finds the range of a list of numbers."""
    
    # Range is maximum - minimum.
    return max(numbers) - min(numbers)


def mode(numbers):
    """Finds the mode of a list of numbers."""
    
    # Put the numbers in a collection.
    collect = collections.Counter(numbers)
    
    # Get the mode of the numbers.
    return collect.most_common(1)[0][0]