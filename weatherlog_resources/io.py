# -*- coding: utf-8 -*-


# This file defines the functions for reading and writing profiles.


# Import json for loading and saving the data.
import json
# Import os for creating directories.
import os


def write_profile(main_dir, name, data):
    """Writes the data to the profile file."""
    
    # Write the data.
    try:
        # This should save to ~/.weatherlog/[profile name]/weather.json on Linux.
        data_file = open("%s/profiles/%s/weather.json" % (main_dir, name), "w")
        json.dump(data, data_file)
        data_file.close()
        return true
        
    except IOError:
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error writing to the file.
        print("Error saving data file (IOError).")
        return false
    
    except (TypeError, ValueError):
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error with the data type.
        print("Error saving data file (TypeError or ValueError).")
        return false


def read_profile(main_dir = "", name = "", filename = ""):
    """Reads the data from the profile file."""
    
    # Get the filename.
    filename = filename if filename != "" else "%s/profiles/%s/weather.json" % (main_dir, name)
    
    # Load the data.   
    try:
        
        # This should be ~/.weatherlog/[profile name]/weather.json on Linux.
        data_file = open(filename, "r")
        data = json.load(data_file)
        data_file.close()
        
    except IOError:
        # Show the error message, and close the application.
        # This one shows if there was a problem reading the file.
        print("Error importing data (IOError).")
        data = []
    
    except (TypeError, ValueError):
        # Show the error message, and close the application.
        # This one shows if there was a problem with the data type.
        print("Error importing data (TypeError or ValueError).")
        data = []
    
    return data


def write_blank_profile(main_dir, name):
    """Writes a blank profile file."""
    
    # Create the directory and file.
    os.makedirs("%s/profiles/%s" % (main_dir, name))
    new_prof_file = open("%s/profiles/%s/weather.json" % (main_dir, name), "w")
    new_prof_file.write("[]")
    new_prof_file.close()
