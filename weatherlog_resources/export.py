# -*- coding: utf-8 -*-


# This file defines the functions for exporting data to HTML and CSV.


# Import the functions for writing to files.
import weatherlog_resources.io as io


# Constants for use with the converting.
HTML_HEADER = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <title>Data exported from WeatherLog</title>
    <meta charset="utf-8" />
    <link rel="stylesheet" type="text/css" href="http://achesak.github.io/weatherlog/minimal.css" />
    <!-- Replace above link with your own stylesheet. -->
    </head>
    <body>"""
HTML_FOOTER = """</body>
    </html>"""
HTML_START = """<h1>%s</h1>
    <table>"""
HTML_END = """</table>"""


def html_cell(cell):
    """Converts each table cell data to UTF-8 and escapes greater and less than signs."""
    
    new_cell = cell
    
    try:
        new_cell = new_cell.replace("<", "&lt;").replace(">", "&gt;")
        new_cell = new_cell.encode("utf-8")
    except:
        pass
    
    return new_cell


def html_generic(data_list, filename = None):
    """Converts the data to HTML and exports it.
    
    * filename is the file to write to.
    * data_list is a list of data to populate the tables with. The first
      index of each list should be a string containing the table title,
      and the remaining rows should contain the table data.
    """
    
    # Start the HTML.
    html = HTML_HEADER
    
    # Loop through each table in the data list.
    for table in data_list:
        html += HTML_START % table[0]
        
        table_data = table[1:]
        num_columns = len(table_data[0])
        
        # Create the table header.
        html += "<tr>"
        for table_header in table_data[0]:
            html += "<th>" + html_cell(table_header) + "</th>"
        html += "</tr>"
        
        # Create the table rows.
        table_data = table_data[1]
        for table_row in table_data:
            html += "<tr>"
            for cell in table_row:
                html += "<td>" + html_cell(cell) + "</td>"
            html += "</tr>"
        
        # End the table.
        html += HTML_END
    
    # End the HTML and write to the file.
    html += HTML_FOOTER
    if filename:
        io.write_standard_file(filename, html)
    else:
        return html


def csv(data2, units, filename = ""):
    """Converts the data to CSV."""
    
    # Create a copy of the data. The original list should remain unchanged.
    data = data2[:]
    
    # Build the string.
    csv = """"Date","Temperature (%s)","Wind Chill (%s)","Precipitation (%s)","Wind (%s)","Humidity (%%)","Air Pressure (%s)","Visibility (%s","Cloud Cover","Notes"\n""" % (units["temp"], units["temp"], units["prec"], units["wind"], units["airp"], units["visi"])
    
    # Add the data. Loop through each list, and add it as a row.
    for i in data:
        for j in range(0, len(i)):
            i[j] = i[j].encode("utf-8")
        csv += """"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n""" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9])
    
    # Remove the last newline character.
    csv = csv[:-1]
    
    # Write to the file.
    if filename:
        io.write_standard_file(filename, csv)
    else:
        return csv
