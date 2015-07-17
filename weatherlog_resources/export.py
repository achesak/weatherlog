# -*- coding: utf-8 -*-


# This file defines the functions for exporting data to HTML and CSV.


# Import the functions for writing to files.
import weatherlog_resources.io as io


# Constants for use with the converting.
HTML_HEADER = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <title>Data exported from WeatherLog</title>
    <meta charset="utf-8">
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
        new_cell = new_cell.encode("utf-8")
        new_cell = new_cell.replace("<", "&lt;").replace(">", "&gt;")
    except:
        pass
    
    return new_cell


def html_generic(title_list, data_list, filename = ""):
    """Converts the data to HTML and exports it.
    
    * filename is the file to write to.
    * title_list is a list of titles for the tables.
    * data_list is a list of data to populate the tables with. The first
      index of this list should be another list containing the table headers.
      The second index should be another list containing the data rows.
    """
    
    # Start the HTML.
    html = HTML_HEADER
    
    # Loop through each title and start the table.
    for i in range(0, len(title_list)):
        html += HTML_START % title_list[i]
        
        data = data_list[i]
        rows = len(data[0])
        
        # Create the table header.
        html += "<tr>"
        for table_title in data[0]:
            html += "<th>" + table_title + "</th>"
        html += "</tr>"
        
        # Create the table rows.
        for j in range(1, rows):
            html += "<tr>"
            print(rows)
            print(j)
            for cell in data[j]:
                html += "<td>" + html_cell(cell) + "</td>"
            html += "</tr>"
        
        # Add the table end.
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


def html(data2, units):
    """Converts the data to HTML."""
    
    # Create a copy of the data. The original list should remain unchanged.
    data = data2[:]
    
    # Build the string.
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
<title>Data exported from WeatherLog</title>
<meta charset="utf-8" />
</head>
<body>
<table>
<tr>
<th>Date</th>
<th>Temperature (%s)</th>
<th>Wind Chill (%s)</th>
<th>Precipitation (%s)</th>
<th>Wind (%s)</th>
<th>Humidity (%%)</th>
<th>Air Pressure (%s)</th>
<th>Visibility (%s)</th>
<th>Cloud Cover</th>
<th>Notes</th>
</tr>""" % (units["temp"], units["temp"], units["prec"], units["wind"], units["airp"], units["visi"])
    
    # Add the data. Loop through each list, and add it as a table row.
    for i in data:
        for j in range(0, len(i)):
            i[j] = i[j].encode("utf-8")
        html += """
<tr>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
</tr>""" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9].replace("<", "&lt;").replace(">", "&gt;"))
    
    # Add the closing tags.
    html += """
</table>
</body>
</html>"""
    
    return html.lstrip()





def info_html(data):
    """Converts the info data to HTML."""
    
    title_list = ["General Info", "Temperature Info", "Wind Chill Info", "Precipitation Info", "Wind Info",
                  "Humidity Info", "Air Pressure Info", "Visibility Info", "Cloud Cover Info", "Notes Info"]
    
    # Build the string.
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
<title>Data exported from WeatherLog</title>
<meta charset="utf-8" />
</head>
<body>"""
    
    # Add the data. Loop through the list, and add each sublist as a new table.
    for j in range(0, len(data)):
        html += """
<h1>""" + title_list[j] + """</h1>
<table>
<tr>
<th>Field</th>
<th>Value</th>
</tr>"""
    
        # Add the data. Loop through each list, and add it as a table row.
        for i in data[j]:
            try:
                i[0] = i[0].encode("utf-8")
                i[1] = i[1].encode("utf-8")
            except:
                pass
            html += """
<tr>
<td>%s</td>
<td>%s</td>
</tr>""" % (i[0], i[1])
        
        # Close the table.
        html += """
</table>"""
    
    # Add the closing tags.
    html += """
</body>
</html>"""
    
    return html.lstrip()


def chart_html(data):
    """Converts the chart data to HTML."""
    
    title_list = ["Temperature Chart", "Wind Chill Chart", "Precipitation Chart", "Wind Chart",
                  "Humidity Chart", "Air Pressure Chart", "Visibility Chart"]
    
    # Build the string.
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
<title>Data exported from WeatherLog</title>
<meta charset="utf-8" />
</head>
<body>"""
    
        # Add the data. Loop through the list, and add each sublist as a new table.
    for j in range(0, len(data)):
        html += """
<h1>""" + title_list[j] + """</h1>
<table>
<tr>
<th>Day</th>
<th>Value</th>
<th>Average Difference</th>
<th>Low Difference</th>
<th>High Difference</th>
<th>Median Difference</th>
</tr>"""
    
        # Add the data. Loop through each list, and add it as a table row.
        for i in data[j]:
            try:
                i[0] = i[0].encode("utf-8")
                i[1] = i[1].encode("utf-8")
                i[2] = i[2].encode("utf-8")
                i[3] = i[3].encode("utf-8")
                i[4] = i[4].encode("utf-8")
                i[5] = i[5].encode("utf-8")
            except:
                pass
            html += """
<tr>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
</tr>""" % (i[0], i[1], i[2], i[3], i[4], i[5])
        
        # Close the table.
        html += """
</table>"""
    
    # Add the closing tags.
    html += """
</body>
</html>"""
    
    return html.lstrip()


def weather_html(data):
    """Converts the weather data to HTML."""
    
    title_list = ["Weather", "Location", "Forecast"]
    
    # Build the string.
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
<title>Data exported from WeatherLog</title>
<meta charset="utf-8" />
</head>
<body>"""
    
    # Add the data. Loop through the list, and add each sublist as a new table.
    for j in range(0, len(data)):
        html += """
<h1>""" + title_list[j] + """</h1>
<table>
<tr>
<th>Field</th>
<th>Value</th>
</tr>"""
    
        # Add the data. Loop through each list, and add it as a table row.
        for i in data[j]:
            try:
                i[0] = i[0].encode("utf-8")
                i[1] = i[1].encode("utf-8")
            except:
                pass
            html += """
<tr>
<td>%s</td>
<td>%s</td>
</tr>""" % (i[0], i[1])
        
        # Close the table.
        html += """
</table>"""
    
    # Add the closing tags.
    html += """
</body>
</html>"""
    
    return html.lstrip()
