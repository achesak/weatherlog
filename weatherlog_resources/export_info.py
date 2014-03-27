# -*- coding: utf-8 -*-


# This file defines the function for exporting info data.


# Import the functions for exporting data.
import export
# Import the functions for writing to files.
import io


def export_info(data, filename):
    """"Exports info data."""
    
    # Convert the data to HTML.
    data2 = export.info_html(data)
    
    # Save the data.
    io.write_standard_file(filename, data2)


def export_chart(data, filename):
    """Exports chart data."""
    
    # Convert the data to HTML.
    data2 = export.chart_html(data)
    
    # Save the data.
    io.write_standard_file(filename, data2)
