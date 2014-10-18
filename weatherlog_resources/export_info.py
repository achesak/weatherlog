# -*- coding: utf-8 -*-


# This file defines the function for exporting info data.


# Import the functions for exporting data.
import export
# Import the functions for writing to files.
import io


def export_info(data, filename):
    """"Exports info data."""
    
    data2 = export.info_html(data)
    io.write_standard_file(filename, data2)


def export_chart(data, filename):
    """Exports chart data."""
    
    data2 = export.chart_html(data)
    io.write_standard_file(filename, data2)


def export_subset(data, units, filename):
    """Exports subset data."""
    
    data2 = export.html(data, units)
    io.write_standard_file(filename, data2)


def export_weather(data, filename):
    """Exports weather data."""
    
    data2 = export.weather_html(data)
    io.write_standard_file(filename, data2)
