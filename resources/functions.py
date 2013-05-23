# -*- coding: utf-8 -*-


# Import the math module.
import math


def mean(numbers):
    """Finds the mean of a list of numbers."""
    # Convert the numbers to floats and then add them.
    total = 0
    for i in numbers:
        total += float(i)
    # Divide by the length of the list.
    return total / len(numbers)


def median(numbers):
    """Finds the median of a list of numbers."""
    # Convert all the numbers to floats.
    for i in range(0, len(numbers)):
        numbers[i] = float(numbers[i])
    # Sort the list.
    numbers.sort()
    # If the list has an odd number of items:
    if not len(numbers) % 0:
        return numbers[int(math.floor(len(numbers) / 2))];
    # If the lsit has an even number of items:
    else:
        return (numbers[len(numbers) / 2] + numbers[(len(numbers) / 2) - 1]) / 2;

