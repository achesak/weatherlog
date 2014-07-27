# -*- coding: utf-8 -*-


# This file defines the functions for converting data to HTML and CSV.


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
<th>Precipitation (%s)</th>
<th>Wind (%s)</th>
<th>Humidity (%%)</th>
<th>Air Pressure (%s)</th>
<th>Cloud Cover</th>
<th>Notes</th>
</tr>""" % (units["temp"], units["prec"], units["wind"], units["airp"])
    
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
</tr>""" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7].replace("<", "&lt;").replace(">", "&gt;"))
    
    # Add the closing tags.
    html += """
</table>
</body>
</html>"""
    
    return html.lstrip()


def csv(data2, units):
    """Converts the data to CSV."""
    
    # Create a copy of the data. The original list should remain unchanged.
    data = data2[:]
    
    # Build the string.
    csv = """"Date","Temperature (%s)","Precipitation (%s)","Wind (%s)","Humidity (%%)","Air Pressure (%s)","Cloud Cover","Notes"\n""" % (units["temp"], units["prec"], units["wind"], units["airp"])
    
    # Add the data. Loop through each list, and add it as a row.
    for i in data:
        for j in range(0, len(i)):
            i[j] = i[j].encode("utf-8")
        csv += """"%s","%s","%s","%s","%s","%s","%s","%s"\n""" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
    
    # Remove the last newline character.
    csv = csv[:-1]
    
    return csv


def info_html(data):
    """Converts the info data to HTML."""
    
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
<th>Field</th>
<th>Value</th>
</tr>"""
    
    # Add the data. Loop through each list, and add it as a table row.
    for i in data:
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
    
    # Add the closing tags.
    html += """
</table>
</body>
</html>"""
    
    return html.lstrip()


def chart_html(data):
    """Converts the chart data to HTML."""
    
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
<th>Day</th>
<th>Value</th>
<th>Average Difference</th>
<th>Low Difference</th>
<th>High Difference</th>
<th>Median Difference</th>
</tr>"""
    
    # Add the data. Loop through each list, and add it as a table row.
    for i in data:
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
    
    # Add the closing tags.
    html += """
</table>
</body>
</html>"""
    
    return html.lstrip()
