# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: calculations.py
# This module contains functions for basic info calculations.
#
################################################################################

# Import sys for version checking.
import sys
# Import the math module for rounding numbers.
import math
# Import the collections module for getting the mode of a list of numbers.
import collections
# Import statistics for getting the median of a list of numbers.
# Only available on more recent version of Python 3.x.
try:
    import statistics
except ImportError:
    statistics = None


def mean(numbers):
    """Finds the mean of a list of numbers."""
    
    return sum(numbers) / len(numbers)


def median(numbers2):
    """Finds the median of a list of numbers."""
    
    # If running in Python 3, use statistics module.
    if sys.version_info >= (3, 0):
        return statistics.median(numbers2)
    
    numbers = sorted(numbers2)
    
    if len(numbers) % 2:
        return numbers[int(math.floor(len(numbers) / 2))]
    else:
        return (numbers[len(numbers) / 2] + numbers[(len(numbers) / 2) - 1]) / 2


def range(numbers):
    """Finds the range of a list of numbers."""
    
    return max(numbers) - min(numbers)


def mode(numbers):
    """Finds the mode of a list of numbers."""
    
    collect = collections.Counter(numbers)
    return collect.most_common(1)[0]
