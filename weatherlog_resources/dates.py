# -*- coding: utf-8 -*-


# This file defines functions for working with dates.


def split_date(date):
    """Splits the date into it's components."""
    
    # Split the date.
    days, months, years = date.split("/")
    days = int(days)
    months = int(months) - 1
    years = int(years)
    return (days, months, years)


def date_to_iso(day, month, year):
    """Formats a date in ISO notation."""
    
    return str(year) + "-" + (str(month) if month > 9 else "0" + str(month)) + "-" + (str(day) if day > 9 else "0" + str(day))
