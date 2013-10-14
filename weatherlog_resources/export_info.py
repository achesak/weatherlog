# -*- coding: utf-8 -*-


# This file defines the function for exporting info data.


# Import the functions for exporting data.
import export


def export_info(data, filename):
    """"Exports info data."""
    
    # Convert the data to HTML.
    data2 = export.info_html(data)
    
    # Save the data.
    try:
        # Write to the specified file.
        data_file = open(filename, "w")
        data_file.write(data2)
        data_file.close()
        
    except IOError:
        # Show the error message.
        # This only shows if the error occurred when writing to the file.
        print("Error exporting data (IOError).")
    
    except (TypeError, ValueError):
        # Show the error message.
        # This one is shown if there was an error with the data type.
        print("Error exporting data (TypeError or ValueError).")
