# -*- coding: utf-8 -*-


# This file defines the functions for building the CSV and HTML.


def html(data2):
    """Converts the data to HTML."""
    
    # Create a copy of the data. The original list should remain unchanged.
    data = data2[:]
    
    # Build the string.
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
<title>Data exported from Weather Or Not</title>
<meta charset="utf-8" />
</head>
<body>
<table>
<tr>
<th>Date</th>
<th>Temperature (°C)</th>
<th>Precipitation (cm)</th>
<th>Wind (kph)</th>
<th>Humidity (%)</th>
<th>Air Pressure (hPa)</th>
<th>Cloud Cover</th>
<th>Notes</th>
</tr>"""
    
    # Add the data. Loop through each list, and add it as a table row.
    for i in data:
        
        # Convert the data to utf-8. This will cause an error otherwise,
        # for reasons I don't quite understand.
        for j in range(0, len(i)):
            i[j] = i[j].encode("utf-8")
        
        # Add the row of data.
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
    
    # Return the HTML.
    return html.lstrip()


def csv(data2):
    """Converts the data to CSV."""
    
    # Create a copy of the data. The original list should remain unchanged.
    data = data2[:]
    
    # Build the string.
    csv = """"Date","Temperature (°C)","Precipitation (cm)","Wind (kph)","Humidity (%)","Air Pressure (hPa)","Cloud Cover","Notes"\n"""
    
    # Add the data. Loop through each list, and add it as a row.
    for i in data:
        
        # Convert the data to utf-8. This will cause an error otherwise,
        # for reasons I don't quite understand.
        for j in range(0, len(i)):
            i[j] = i[j].encode("utf-8")
        
        # Add the row of data.
        csv += """"%s","%s","%s","%s","%s","%s","%s","%s"\n""" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
    
    # Remove the last newline character.
    csv = csv[:-1]
    
    # Return the CSV.
    return csv
