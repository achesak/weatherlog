# -*- coding: utf-8 -*-


# This file defines the functions for getting the info.


# Import future to make division work properly.
from __future__ import division
# Import datetime for date calculations.
import datetime
# Import collections.Counter for getting the mode of the data.
from collections import Counter

# Import the dataset functions.
import weatherlog_resources.datasets as datasets
# Import the calculation functions.
import weatherlog_resources.calculations as calculations


def general_info(data, units):
    """Gets the general info."""
    
    # Get the date data.
    date_data = datasets.get_column(data, 0)
    date_first = date_data[0]
    date_last = date_data[len(date_data) - 1]
    date_first2 = datetime.datetime.strptime(date_first, "%d/%m/%Y")
    date_last2 = datetime.datetime.strptime(date_last, "%d/%m/%Y")
    date_num = (date_last2 - date_first2).days + 1
    day_num = len(data)
    
    # Get the temperature data.
    temp_data = datasets.convert_float(datasets.get_column(data, 1))
    temp_low = min(temp_data)
    temp_high = max(temp_data)
    temp_avg = calculations.mean(temp_data)
    
    # Get the wind chill data.
    chil_data = datasets.convert_float(datasets.get_column(data, 2))
    chil_low = min(chil_data)
    chil_high = max(chil_data)
    chil_avg = calculations.mean(chil_data)
    
    # Get the precipitation data.
    prec_data1, prec_data2 = datasets.split_list(datasets.get_column(data, 3))
    prec_data1 = datasets.convert_float(datasets.none_to_zero(prec_data1))
    try:
        prec_low = min(prec_data1)
        prec_high = max(prec_data1)
        prec_avg = calculations.mean(prec_data1)
    except:
        prec_low = "None"
        prec_high = "None"
        prec_avg = "None"
    
    # Get the wind data.
    wind_data1, wind_data2 = datasets.split_list(datasets.get_column(data, 4))
    wind_data1 = datasets.convert_float(datasets.none_to_zero(wind_data1))
    try:
        wind_low = min(wind_data1)
        wind_high = max(wind_data1)
        wind_avg = calculations.mean(wind_data1)
    except:
        wind_low = "None"
        wind_high = "None"
        wind_avg = "None"
    
    # Get the humidity data.
    humi_data = datasets.convert_float(datasets.get_column(data, 5))
    humi_low = min(humi_data)
    humi_high = max(humi_data)
    humi_avg = calculations.mean(humi_data)
    
    # Get the air pressure data.
    airp_data1, airp_data2 = datasets.split_list(datasets.get_column(data, 6))
    airp_data1 = datasets.convert_float(airp_data1)
    airp_low = min(airp_data1)
    airp_high = max(airp_data1)
    airp_avg = calculations.mean(airp_data1)
    
    # Get the visibility data.
    visi_data = datasets.convert_float(datasets.get_column(data, 7))
    visi_low = min(visi_data)
    visi_high = max(visi_data)
    visi_avg = calculations.mean(visi_data)
    
    # Get the cloud cover data.
    clou_data = datasets.split_list3(datasets.get_column(data, 8))
    clou_data1 = Counter(clou_data[0])
    clou_data2 = Counter(datasets.strip_items(clou_data[1], ["(", ")"]))
    clou_data1_counter = clou_data1.most_common(1)[0]
    clou_data2_counter = clou_data2.most_common(1)[0]
    clou_mode1 = clou_data1_counter[0]
    clou_mode1_count = clou_data1_counter[1]
    clou_mode2 = clou_data2_counter[0]
    clou_mode2_count = clou_data2_counter[1]
    
    # Change any values, if needed.
    prec_low = "None" if prec_low == "None" else ("%.2f %s" % (prec_low, units["prec"]))
    prec_high = "None" if prec_high == "None" else ("%.2f %s" % (prec_high, units["prec"]))
    prec_avg = "None" if prec_avg == "None" else ("%.2f %s" % (prec_avg, units["prec"]))
    wind_low = "None" if wind_low == "None" else ("%.2f %s" % (wind_low, units["wind"]))
    wind_high = "None" if wind_high == "None" else ("%.2f %s" % (wind_high, units["wind"]))
    wind_avg = "None" if wind_avg == "None" else ("%.2f %s" % (wind_avg, units["wind"]))
    
    # Create the data list.
    data2 = [
        ["First date", "%s" % date_first],
        ["Last date", "%s" % date_last],
        ["Number of days", "%d days" % day_num],
        ["Range of days", "%d days" % date_num],
        ["Lowest temperature", "%.2f %s" % (temp_low, units["temp"])], 
        ["Highest temperature", "%.2f %s" % (temp_high, units["temp"])],
        ["Average temperature", "%.2f %s" % (temp_avg, units["temp"])],
        ["Lowest wind chill", "%.2f %s" % (chil_low, units["temp"])], 
        ["Highest wind chill", "%.2f %s" % (chil_high, units["temp"])],
        ["Average wind chill", "%.2f %s" % (chil_avg, units["temp"])],
        ["Lowest precipitation", prec_low],
        ["Highest precipitation", prec_high],
        ["Average precipitation", prec_avg],
        ["Lowest wind speed", wind_low],
        ["Highest wind speed", wind_high],
        ["Average wind speed", wind_avg],
        ["Lowest humidity", "%.2f%%" % humi_low], 
        ["Highest humidity", "%.2f%%" % humi_high],
        ["Average humidity", "%.2f%%" % humi_avg],
        ["Lowest air pressure", "%.2f %s" % (airp_low, units["airp"])],
        ["Highest air pressure", "%.2f %s" % (airp_high, units["airp"])],
        ["Average air pressure", "%.2f %s" % (airp_avg, units["airp"])],
        ["Lowest visibility", "%.2f %s" % (visi_low, units["visi"])], 
        ["Highest visibility", "%.2f %s" % (visi_high, units["visi"])],
        ["Average visibility", "%.2f %s" % (visi_avg, units["visi"])],
        ["Most common cloud cover", "%s (%d occurrences)" % (clou_mode1, clou_mode1_count)],
        ["Most common cloud type", "%s (%d occurrences)" % (clou_mode2, clou_mode2_count)]
    ]
    
    return data2


def temp_info(data, units):
    """"Gets the temperature info."""
    
    # Get the data.
    temp_data = datasets.convert_float(datasets.get_column(data, 1))
    temp_low = min(temp_data)
    temp_high = max(temp_data)
    temp_avg = calculations.mean(temp_data)
    temp_median = calculations.median(temp_data)
    temp_range = calculations.range(temp_data)
    temp_mode, temp_mode_count = calculations.mode(temp_data)
    
    # Create the data list.
    data2 = [
        ["Lowest temperature", "%.2f %s" % (temp_low, units["temp"])],
        ["Highest temperature", "%.2f %s" % (temp_high, units["temp"])],
        ["Average temperature", "%.2f %s" % (temp_avg, units["temp"])],
        ["Median temperature", "%.2f %s" % (temp_median, units["temp"])],
        ["Range of temperatures", "%.2f %s" % (temp_range, units["temp"])],
        ["Most common temperature", "%.2f %s (%d occurrences)" % (temp_mode, units["temp"], temp_mode_count)]
    ]
    
    return data2


def chil_info(data, units):
    """"Gets the wind chill info."""
    
    # Get the data.
    chil_data = datasets.convert_float(datasets.get_column(data, 2))
    chil_low = min(chil_data)
    chil_high = max(chil_data)
    chil_avg = calculations.mean(chil_data)
    chil_median = calculations.median(chil_data)
    chil_range = calculations.range(chil_data)
    chil_mode, chil_mode_count = calculations.mode(chil_data)
    
    # Create the data list.
    data2 = [
        ["Lowest wind chill", "%.2f %s" % (chil_low, units["temp"])],
        ["Highest wind chill", "%.2f %s" % (chil_high, units["temp"])],
        ["Average wind chill", "%.2f %s" % (chil_avg, units["temp"])],
        ["Median wind chill", "%.2f %s" % (chil_median, units["temp"])],
        ["Range of wind chills", "%.2f %s" % (chil_range, units["temp"])],
        ["Most common wind chill", "%.2f %s (%d occurrences)" % (chil_mode, units["temp"], chil_mode_count)]
    ]
    
    return data2


def prec_info(data, units):
    """"Gets the precipitation info."""
    
    # Get the data.
    num_days = len(data)
    prec_data1, prec_data2 = datasets.split_list(datasets.get_column(data, 3))
    prec_split = datasets.split_list2(datasets.get_column(data, 3))
    prec_data1 = datasets.none_to_zero(prec_data1)
    prec_data1 = datasets.convert_float(prec_data1)
    try:
        prec_low = min(prec_data1)
        prec_high = max(prec_data1)
        prec_avg = calculations.mean(prec_data1)
        prec_median = calculations.median(prec_data1)
        prec_range = calculations.range(prec_data1)
    except:
        prec_low = "None"
        prec_high = "None"
        prec_avg = "None"
        prec_median = "None"
        prec_range = "None"
    prec_total = 0
    prec_total_rain = 0
    prec_total_snow = 0
    prec_total_hail = 0
    prec_total_sleet = 0
    prec_none = 0
    prec_rain = 0
    prec_snow = 0
    prec_hail = 0
    prec_sleet = 0
    for i in prec_split:
        if i[1] != "None":
            prec_total += float(i[0])
        if i[1] == "None":
            prec_none += 1
        elif i[1] == "Rain":
            prec_total_rain += float(i[0])
            prec_rain += 1
        elif i[1] == "Snow":
            prec_total_snow += float(i[0])
            prec_snow += 1
        elif i[1] == "Hail":
            prec_total_hail += float(i[0])
            prec_hail += 1
        elif i[1] == "Sleet":
            prec_total_sleet += float(i[0])
            prec_sleet += 1
    prec_mode, prec_mode_count = calculations.mode(prec_data2)
    if prec_total == 0:
        prec_per_rain = "0%"
        prec_per_snow = "0%"
        prec_per_hail = "0%"
        prec_per_sleet = "0%"
    else:
        prec_per_rain = "%.2f%%" % ((prec_total_rain / prec_total) * 100)
        prec_per_snow = "%.2f%%" % ((prec_total_snow / prec_total) * 100)
        prec_per_hail = "%.2f%%" % ((prec_total_hail / prec_total) * 100)
        prec_per_sleet = "%.2f%%" % ((prec_total_sleet / prec_total) * 100)
    
    # Change any values, if needed.
    prec_low = "None" if prec_low == "None" else ("%.2f %s" % (prec_low, units["prec"]))
    prec_high = "None" if prec_high == "None" else ("%.2f %s" % (prec_high, units["prec"]))
    prec_avg = "None" if prec_avg == "None" else ("%.2f %s" % (prec_avg, units["prec"]))
    prec_median = "None" if prec_median == "None" else ("%.2f %s" % (prec_median, units["prec"]))
    prec_range = "None" if prec_range == "None" else ("%.2f %s" % (prec_range, units["prec"]))
    
    # Create the data list.
    data2 = [
        ["Lowest precipitation", prec_low],
        ["Highest precipitation", prec_high],
        ["Average precipitation", prec_avg],
        ["Median precipitation", prec_median],
        ["Range of precipitation", prec_range],
        ["Total precipitation", "%.2f %s" % (prec_total, units["prec"])],
        ["Total rain", "%.2f %s (%s)" % (prec_total_rain, units["prec"], prec_per_rain)],
        ["Total snow", "%.2f %s (%s)" % (prec_total_snow, units["prec"], prec_per_snow)],
        ["Total hail", "%.2f %s (%s)" % (prec_total_hail, units["prec"], prec_per_hail)],
        ["Total sleet", "%.2f %s (%s)" % (prec_total_sleet, units["prec"], prec_per_sleet)],
        ["Days with no precipitation", "%d day%s (%.2f%%)" % (prec_none, "" if prec_none == 1 else "s", (prec_none / num_days) * 100)],
        ["Days with rain", "%d day%s (%.2f%%)" % (prec_rain, "" if prec_rain == 1 else "s", (prec_rain / num_days) * 100)],
        ["Days with snow", "%d day%s (%.2f%%)" % (prec_snow, "" if prec_snow == 1 else "s", (prec_snow / num_days) * 100)],
        ["Days with hail", "%d day%s (%.2f%%)" % (prec_hail, "" if prec_hail == 1 else "s", (prec_hail / num_days) * 100)],
        ["Days with sleet", "%d day%s (%.2f%%)" % (prec_sleet, "" if prec_sleet == 1 else "s", (prec_sleet / num_days) * 100)],
        ["Most common precipitation type", "%s (%d occurrences)" % (prec_mode if prec_mode != "" else "None", prec_mode_count)]
    ]
    
    return data2


def wind_info(data, units):
    """Gets the wind info."""
    
    # Get the data.
    wind_data1, wind_data2 = datasets.split_list(datasets.get_column(data, 4))
    wind_data1 = datasets.none_to_zero(wind_data1)
    wind_data1 = datasets.convert_float(wind_data1)
    try:
        wind_low = min(wind_data1)
        wind_high = max(wind_data1)
        wind_avg = calculations.mean(wind_data1)
        wind_median = calculations.median(wind_data1)
        wind_range = calculations.range(wind_data1)
    except:
        wind_low = "None"
        wind_high = "None"
        wind_avg = "None"
        wind_median = "None"
        wind_range = "None"
    wind_mode, wind_mode_count = calculations.mode(wind_data2)
    
    # Change any values, if needed.
    wind_low = "None" if wind_low == "None" else ("%.2f %s" % (wind_low, units["wind"]))
    wind_high = "None" if wind_high == "None" else ("%.2f %s" % (wind_high, units["wind"]))
    wind_avg = "None" if wind_avg == "None" else ("%.2f %s" % (wind_avg, units["wind"]))
    wind_median = "None" if wind_median == "None" else ("%.2f %s" % (wind_median, units["wind"]))
    wind_range = "None" if wind_range == "None" else ("%.2f %s" % (wind_range, units["wind"]))
    
    # Create the data list.
    data2 = [
        ["Lowest wind speed", wind_low],
        ["Highest wind speed", wind_high],
        ["Average wind speed", wind_avg],
        ["Median wind speed", wind_median],
        ["Range of wind speeds", wind_range],
        ["Most common wind direction", "%s (%d occurrences)" % (wind_mode if wind_mode != "" else "None", wind_mode_count)]
    ]
    
    return data2


def humi_info(data, units):
    """Gets the humidity info."""
    
    # Get the data.
    humi_data = datasets.convert_float(datasets.get_column(data, 5))
    humi_low = min(humi_data)
    humi_high = max(humi_data)
    humi_avg = calculations.mean(humi_data)
    humi_median = calculations.median(humi_data)
    humi_range = calculations.range(humi_data)
    humi_mode, humi_mode_count = calculations.mode(humi_data)
    
    # Create the data list.
    data2 = [
        ["Lowest humidity", "%.2f%%" % humi_low],
        ["Highest humidity", "%.2f%%" % humi_high],
        ["Average humidity", "%.2f%%" % humi_avg],
        ["Median humidity", "%.2f%%" % humi_median],
        ["Range of humidity", "%.2f%%" % humi_range],
        ["Most common humidity", "%.2f%% (%d occurrences)" % (humi_mode, humi_mode_count)]
    ]
    
    return data2


def airp_info(data, units):
    """Gets the air pressure info."""
    
    # Get the data.
    airp_data1, airp_data2 = datasets.split_list(datasets.get_column(data, 6))
    airp_data1 = datasets.convert_float(airp_data1)
    airp_low = min(airp_data1)
    airp_high = max(airp_data1)
    airp_avg = calculations.mean(airp_data1)
    airp_median = calculations.median(airp_data1)
    airp_range = calculations.range(airp_data1)
    airp_mode, airp_mode_count = calculations.mode(airp_data1)
    airp_steady = 0
    airp_rising = 0
    airp_falling = 0
    for i in airp_data2:
        if i == "Steady":
            airp_steady += 1
        elif i == "Rising":
            airp_rising += 1
        elif i == "Falling":
            airp_falling += 1
    
    # Create the data list.
    data2 = [
        ["Lowest air pressure", "%.2f %s" % (airp_low, units["airp"])],
        ["Highest air pressure", "%.2f %s" % (airp_high, units["airp"])],
        ["Average air pressure", "%.2f %s" % (airp_avg, units["airp"])],
        ["Median air pressure", "%.2f %s" % (airp_median, units["airp"])],
        ["Range of air pressures", "%.2f %s" % (airp_range, units["airp"])],
        ["Most common air pressure", "%.2f %s (%d occurrences)" % (airp_mode, units["airp"], airp_mode_count)],
        ["Days with steady pressure", "%d day%s" % (airp_steady, "" if airp_steady == 1 else "s")],
        ["Days with rising pressure", "%d day%s" % (airp_rising, "" if airp_rising == 1 else "s")],
        ["Days with falling pressure", "%d day%s" % (airp_falling, "" if airp_falling == 1 else "s")]
    ]
    
    return data2


def visi_info(data, units):
    """"Gets the visibility info."""
    
    # Get the data.
    visi_data = datasets.convert_float(datasets.get_column(data, 2))
    visi_low = min(visi_data)
    visi_high = max(visi_data)
    visi_avg = calculations.mean(visi_data)
    visi_median = calculations.median(visi_data)
    visi_range = calculations.range(visi_data)
    visi_mode, visi_mode_count = calculations.mode(visi_data)
    
    # Create the data list.
    data2 = [
        ["Lowest visibility", "%.2f %s" % (visi_low, units["visi"])],
        ["Highest visibility", "%.2f %s" % (visi_high, units["visi"])],
        ["Average visibility", "%.2f %s" % (visi_avg, units["visi"])],
        ["Median visibility", "%.2f %s" % (visi_median, units["visi"])],
        ["Range of visibility", "%.2f %s" % (visi_range, units["visi"])],
        ["Most common visibility", "%.2f %s (%d occurrences)" % (visi_mode, units["visi"], visi_mode_count)]
    ]
    
    return data2


def clou_info(data, units):
    """Gets the cloud cover info."""
    
    # Get the data.
    clou_data1, clou_data2 = datasets.split_list3(datasets.get_column(data, 8))
    # Get the number of days of each cloud cover.
    clou_cover = Counter(clou_data1)
    m_list1 = clou_cover.most_common()
    m_dict1 = {}
    for i in m_list1:
        m_dict1[i[0]] = i[1]
    # Get the number of days of each cloud type.
    clou_type = Counter(datasets.strip_items(clou_data2, ["(", ")"]))
    m_list2 = clou_type.most_common()
    m_dict2 = {}
    for i in m_list2:
        m_dict2[i[0]] = i[1]
    
    # If any of the items don't appear, add dict items for them, with the values set to 0.
    if not "Sunny" in m_dict1:
        m_dict1["Sunny"] = 0
    if not "Mostly Sunny" in m_dict1:
        m_dict1["Mostly Sunny"] = 0
    if not "Partly Cloudy" in m_dict1:
        m_dict1["Partly Cloudy"] = 0
    if not "Mostly Cloudy" in m_dict1:
        m_dict1["Mostly Cloudy"] = 0
    if not "Cloudy" in m_dict1:
        m_dict1["Cloudy"] = 0
    if not "None" in m_dict2:
        m_dict2["None"] = 0
    if not "Unknown" in m_dict2:
        m_dict2["Unknown"] = 0
    if not "Cirrus" in m_dict2:
        m_dict2["Cirrus"] = 0
    if not "Cirrocumulus" in m_dict2:
        m_dict2["Cirrocumulus"] = 0
    if not "Cirrostratus" in m_dict2:
        m_dict2["Cirrostratus"] = 0
    if not "Cumulonimbus" in m_dict2:
        m_dict2["Cumulonimbus"] = 0
    if not "Altocumulus" in m_dict2:
        m_dict2["Altocumulus"] = 0
    if not "Altostratus" in m_dict2:
        m_dict2["Altostratus"] = 0
    if not "Stratus" in m_dict2:
        m_dict2["Stratus"] = 0
    if not "Cumulus" in m_dict2:
        m_dict2["Cumulus"] = 0
    if not "Stratocumulus" in m_dict2:
        m_dict2["Stratocumulus"] = 0
    
    # Create the data list.
    data2 = [
        ["Most common cloud cover", "%s (%s occurrences)" % (m_list1[0][0], m_list1[0][1])],
        ["Most common cloud type", "%s (%s occurrences)" % (m_list2[0][0], m_list2[0][1])],
        ["Days sunny", "%s day%s" % (m_dict1["Sunny"], "" if m_dict1["Sunny"] == 1 else "s")],
        ["Days mostly sunny", "%s day%s" % (m_dict1["Mostly Sunny"], "" if m_dict1["Mostly Sunny"] == 1 else "s")],
        ["Days partly cloudy", "%s day%s" % (m_dict1["Partly Cloudy"], "" if m_dict1["Partly Cloudy"] == 1 else "s")],
        ["Days mostly cloudy", "%s day%s" % (m_dict1["Mostly Cloudy"], "" if m_dict1["Mostly Cloudy"] == 1 else "s")],
        ["Days cloudy", "%s day%s" % (m_dict1["Cloudy"], "" if m_dict1["Cloudy"] == 1 else "s")],
        ["Days with no clouds", "%s day%s" % (m_dict2["None"], "" if m_dict2["None"] == 1 else "s")],
        ["Days with unknown clouds", "%s day%s" % (m_dict2["Unknown"], "" if m_dict2["Unknown"] == 1 else "s")],
        ["Days with cirrus", "%s day%s" % (m_dict2["Cirrus"], "" if m_dict2["Cirrus"] == 1 else "s")],
        ["Days with cirrocumulus", "%s day%s" % (m_dict2["Cirrocumulus"], "" if m_dict2["Cirrocumulus"] == 1 else "s")],
        ["Days with cirrostratos", "%s day%s" % (m_dict2["Cirrostratus"], "" if m_dict2["Cirrostratus"] == 1 else "s")],
        ["Days with cumulonimbus", "%s day%s" % (m_dict2["Cumulonimbus"], "" if m_dict2["Cumulonimbus"] == 1 else "s")],
        ["Days with altocumulus", "%s day%s" % (m_dict2["Altocumulus"], "" if m_dict2["Altocumulus"] == 1 else "s")],
        ["Days with altostratus", "%s day%s" % (m_dict2["Altostratus"], "" if m_dict2["Altostratus"] == 1 else "s")],
        ["Days with stratus", "%s day%s" % (m_dict2["Stratus"], "" if m_dict2["Stratus"] == 1 else "s")],
        ["Days with cumulus", "%s day%s" % (m_dict2["Cumulus"], "" if m_dict2["Cumulus"] == 1 else "s")],
        ["Days with stratocumulus", "%s day%s" % (m_dict2["Stratocumulus"], "" if m_dict2["Stratocumulus"] == 1 else "s")]
    ]
    
    return data2


def note_info(data, units):
    """Gets the notes info."""
    
    # Get the data.
    data2 = []
    
    # Loop through the list, appending the dates and notes.
    for i in range(0, len(data)):
        if data[i][9] != "":
            data2.append([data[i][0], data[i][9]])
    
    return data2
