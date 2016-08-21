# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: charts.py
# This module calculates and organizes data for the Charts feature.
#
################################################################################


# Import collections.Counter for getting the mode of the data.
from collections import Counter

# Import application modules.
import weatherlog_resources.datasets as datasets
import weatherlog_resources.calculations as calculations


def temp_chart(data, units):
    """"Gets the temperature chart data."""
    
    # Get the data.
    temp_data = datasets.convert_float(datasets.get_column(data, 1))
    temp_low = min(temp_data)
    temp_high = max(temp_data)
    temp_avg = calculations.mean(temp_data)
    temp_median = calculations.median(temp_data)
    
    # Calculate and add the data.
    data2 = []
    for i in range(0, len(data)):
        
        temp = [data[i][0], "%.2f %s" % (temp_data[i], units["temp"])]
        temp += build_chart(temp_data[i], temp_low, temp_high, temp_avg, temp_median, units["temp"])
        data2.append(temp)
    
    return data2


def chil_chart(data, units):
    """"Gets the wind chill chart data."""
    
    # Get the data.
    chil_data = datasets.convert_float(datasets.get_column(data, 2))
    chil_low = min(chil_data)
    chil_high = max(chil_data)
    chil_avg = calculations.mean(chil_data)
    chil_median = calculations.median(chil_data)
    
    # Calculate and add the data.
    data2 = []
    for i in range(0, len(data)):
        
        chil = [data[i][0], "%.2f %s" % (chil_data[i], units["temp"])]
        chil += build_chart(chil_data[i], chil_low, chil_high, chil_avg, chil_median, units["temp"])
        data2.append(chil)
    
    return data2


def prec_chart(data, units):
    """"Gets the precipitation chart data."""
    
    # Get the data.
    prec_data1, prec_data2 = datasets.split_list(datasets.get_column(data, 3))
    prec_split = datasets.split_list2(datasets.get_column(data, 3))
    prec_data1 = datasets.none_to_zero(prec_data1)
    prec_data1 = datasets.convert_float(prec_data1)
    prec_low = min(prec_data1)
    prec_high = max(prec_data1)
    prec_avg = calculations.mean(prec_data1)
    prec_median = calculations.median(prec_data1)
    
    # Calculate and add the data.
    data2 = []
    for i in range(0, len(data)):
        
        prec = [data[i][0], "%.2f %s" % (prec_data1[i], units["prec"])]
        prec += build_chart(prec_data1[i], prec_low, prec_high, prec_avg, prec_median, units["prec"])
        data2.append(prec)
    
    return data2


def wind_chart(data, units):
    """"Gets the wind chart data."""
    
    # Get the data.
    wind_data1, wind_data2 = datasets.split_list(datasets.get_column(data, 4))
    wind_data1 = datasets.none_to_zero(wind_data1)
    wind_data1 = datasets.convert_float(wind_data1)
    wind_low = min(wind_data1)
    wind_high = max(wind_data1)
    wind_avg = calculations.mean(wind_data1)
    wind_median = calculations.median(wind_data1)
    
    # Calculate and add the data.
    data2 = []
    for i in range(0, len(data)):
        
        wind = [data[i][0], "%.2f %s" % (wind_data1[i], units["wind"])]
        wind += build_chart(wind_data1[i], wind_low, wind_high, wind_avg, wind_median, units["wind"])
        data2.append(wind)
    
    return data2


def humi_chart(data, units):
    """"Gets the humidity chart data."""
    
    # Get the data.
    humi_data = datasets.convert_float(datasets.get_column(data, 5))
    humi_low = min(humi_data)
    humi_high = max(humi_data)
    humi_avg = calculations.mean(humi_data)
    humi_median = calculations.median(humi_data)
    
    # Calculate and add the data.
    data2 = []
    for i in range(0, len(data)):
        
        humi = [data[i][0], "%.2f%%" % (humi_data[i])]
        humi += build_chart(humi_data[i], humi_low, humi_high, humi_avg, humi_median, "%", unit_space = False)
        data2.append(humi)
    
    return data2


def airp_chart(data, units):
    """"Gets the air pressure chart data."""
    
    # Get the data.
    airp_data1, airp_data2 = datasets.split_list(datasets.get_column(data, 6))
    airp_data1 = datasets.convert_float(airp_data1)
    airp_low = min(airp_data1)
    airp_high = max(airp_data1)
    airp_avg = calculations.mean(airp_data1)
    airp_median = calculations.median(airp_data1)
    
    # Calculate and add the data.
    data2 = []
    for i in range(0, len(data)):
        
        airp = [data[i][0], "%.2f %s" % (airp_data1[i], units["airp"])]
        airp += build_chart(airp_data1[i], airp_low, airp_high, airp_avg, airp_median, units["airp"])
        data2.append(airp)
    
    return data2


def visi_chart(data, units):
    """"Gets the visibility chart data."""
    
    # Get the data.
    visi_data = datasets.convert_float(datasets.get_column(data, 7))
    visi_low = min(visi_data)
    visi_high = max(visi_data)
    visi_avg = calculations.mean(visi_data)
    visi_median = calculations.median(visi_data)
    
    # Calculate and add the data.
    data2 = []
    for i in range(0, len(data)):
        
        visi = [data[i][0], "%.2f %s" % (visi_data[i], units["visi"])]
        visi += build_chart(visi_data[i], visi_low, visi_high, visi_avg, visi_median, units["visi"])
        data2.append(visi)
    
    return data2


def build_chart(value, min_val, max_val, avg_val, med_val, unit, unit_space = True):
    """Builds a chart row."""
    
    row = []
    
    if value == avg_val:
        avg = "Average"
    else:
        avg = avg_val - value
        avg = "%s %.2f%s%s" % ("+" if avg_val < value else "-", abs(avg), " " if unit_space else "", unit)
    row.append(avg)
    
    if value == min_val:
        low = "Low"
    else:
        low = min_val - value
        low = "%s %.2f%s%s" % ("+" if min_val < value else "-", abs(low), " " if unit_space else "", unit)
    row.append(low)
    
    if value == max_val:
        high = "High"
    else:
        high = max_val - value
        high = "%s %.2f%s%s" % ("+" if max_val < value else "-", abs(high), " " if unit_space else "", unit)
    row.append(high)
    
    if value == med_val:
        median = "Median"
    else:
        median = med_val - value
        median = "%s %.2f%s%s" % ("+" if med_val < value else "-", abs(median), " " if unit_space else "", unit)
    row.append(median)
    
    return row
