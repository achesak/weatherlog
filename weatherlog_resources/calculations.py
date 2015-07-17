# -*- coding: utf-8 -*-


# This file defines functions used for getting the data.


# Import the math module for rounding numbers.
import math
# Import the collections module for getting the mode of a list of numbers.
import collections


def mean(numbers):
    """Finds the mean of a list of numbers."""
    
    total = 0
    for i in numbers:
        total += i
    return total / len(numbers)


def median(numbers2):
    """Finds the median of a list of numbers."""
    
    numbers = numbers2[:]
    numbers.sort()
    
    # If the list has an odd number of items:
    if len(numbers) % 2:
        return numbers[int(math.floor(len(numbers) / 2))];
    
    # If the list has an even number of items:
    else:
        return (numbers[len(numbers) / 2] + numbers[(len(numbers) / 2) - 1]) / 2;


def range(numbers):
    """Finds the range of a list of numbers."""
    
    return max(numbers) - min(numbers)


def mode(numbers):
    """Finds the mode of a list of numbers."""
    
    collect = collections.Counter(numbers)
    return collect.most_common(1)[0]
