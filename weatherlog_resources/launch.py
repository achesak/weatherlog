# -*- coding: utf-8 -*-


# This file defines the functions for launching and setting up the application.


# Import json for loading and saving the data.
import json
# Import platform for getting the user's operating system.
import platform
# Import os for creating a directory and other tasks.
import os
# Import os.path for seeing if a directory exists and other tasks.
import os.path
# Import sys for closing the application.
import sys
# Import glob for getting a list of directories.
import glob


def get_main_dir():
    """Returns the main directory."""
    
    # The main directory is C:\.weatherlog on Windows,
    # and /home/[username]/.weatherlog on Linux.
    if platform.system().lower() == "windows":
        return "C:\\.weatherlog"
    else:
        return "%s/.weatherlog" % os.path.expanduser("~")


def check_files_exist(main_dir):
    """Checks to see if the base files exist, and create them if they don't."""
    
    # Check to see if the directory exists, and create it if it doesn't.
    if not os.path.exists(main_dir) or not os.path.isdir(main_dir):
        
        # Create the directory.
        os.makedirs(main_dir)
        
        # Create the last profile file.
        last_prof = open("%s/lastprofile" % main_dir, "w")
        last_prof.write("Main Profile")
        last_prof.close()
        
        # Create the Main Profile directory and data file.
        os.makedirs("%s/profiles/Main Profile" % main_dir)
        last_prof_data = open("%s/profiles/Main Profile/weather.json" % main_dir, "w")
        last_prof_data.write("[]")
        last_prof_data.close()


def get_last_profile(main_dir):
    """Returns the last profile, the original profile to be loaded, and whether the profile exists. Creates the profile if it doesn't exist."""
    
    # Get the last profile.
    try:
        # Load the last profile file.
        prof_file = open("%s/lastprofile" % main_dir, "r")
        last_profile = prof_file.read().rstrip()
        prof_file.close()
        
        # Check to make sure the profile exists:
        # Remember the currect directory and switch to where the profiles are stored.
        current_dir = os.getcwd()
        os.chdir("%s/profiles" % main_dir)
        
        # Get the list of profiles.
        profiles_list = glob.glob("*")
        
        # Switch back to the previous directory.
        os.chdir(current_dir)
        
        # Check if the profile exists:
        if last_profile in profiles_list:
            profile_exists = True
            original_profile = ""
        else:
            profile_exists = False
            original_profile = last_profile
    
    except IOError:
        # Show the error message, and close the application.
        # This one shows if there was a problem reading the file.
        print("Error reading profile file (IOError).")
        sys.exit()
    
    # If the profile doesn't exist, switch or make one that does:
    if not profile_exists:
        
        # If the default profile exists, switch to that.
        if "Main Profile" in profiles_list:
            last_profile = "Main Profile"
        
        # Otherwise, create the profile:
        else:
            
            # Create the Main Profile directory and data file.
            os.makedirs("%s/profiles/Main Profile" % main_dir)
            last_prof_data = open("%s/profiles/Main Profile/weather.json" % main_dir, "w")
            last_prof_data.write("[]")
            last_prof_data.close()
            
            # Set the profile name.
            last_profile = "Main Profile"
    
    return last_profile, original_profile, profile_exists


def get_config(main_dir):
    """Loads the settings."""
    
    # Get the configuration.
    try:
        config_file = open("%s/config" % main_dir, "r")
        config = json.load(config_file)
        config_file.close()
    
    except IOError:
        # Continue.
        config = {"pre-fill": False,
                  "restore": True,
                  "location": "",
                  "units": "metric",
                  "pastebin": "d2314ff616133e54f728918b8af1500e",
                  "show_units": True,
                  "show_dates": True,
                  "escape_fullscreen": "exit fullscreen",
                  "escape_windowed": "minimize",
                  "auto_save": True,
                  "confirm_del": True,
                  "show_pre-fill": True,
                  "confirm_exit": False}
    
    # If there are missing configuration options, then add them.
    # This is for compatability with upgrades from previous versions.
    if not "restore" in config:
        config["restore"] = True
    if not "show_units" in config:
        config["show_units"] = True
    if not "show_dates" in config:
        config["show_dates"] = True
    if not "escape_windowed" in config:
        config["escape_windowed"] = "minimize"
    if not "escape_fullscreen" in config:
        config["escape_fullscreen"] = "exit fullscreen"
    if not "auto_save" in config:
        config["auto_save"] = True
    if not "confirm_del" in config: 
        config["confirm_del"] = True
    if not "show_pre-fill" in config:
        config["show_pre-fill"] = True
    if not "confirm_exit" in config:
        config["confirm_exit"] = False
    
    return config


def get_window_size(main_dir, config):
    """Gets the last window size."""
    
    # Get the previous window size.
    try:
        wins_file = open("%s/window_size" % main_dir, "r")
        last_width = int(wins_file.readline())
        last_height = int(wins_file.readline())
        wins_file.close()
    
    except IOError:
        # Continue.
        last_width = 900
        last_height = 500
    
    # If the user doesn't want to restore the window size, set the size to the defaults.
    if not config["restore"]:
        last_width = 900
        last_height = 500
    
    return last_width, last_height


def get_units(config):
    """Gets the units."""
    
    # Configure the units.
    # Metric:
    if config["units"] == "metric":
        
        # Temperature is Celsius.
        # Precipitation is centimeters.
        # Wind speed is kilometers per hour.
        # Air pressure is hecto-pascals.
        units = {"temp": "°C",
                 "prec": "cm",
                 "wind": "kph",
                 "airp": "hPa"}
    
    # Imperial:
    elif config["units"] == "imperial":
        
        # Temperature is Fahrenheit.
        # Precipitation is inches.
        # Wind speed is miles per hour
        # Air pressure is millibars.
        units = {"temp": "°F",
                 "prec": "in",
                 "wind": "mph",
                 "airp": "mbar"}
    
    return units


def get_data(main_dir, last_profile):
    """Gets the data."""
    
    # Load the data.   
    try:
        # This should be ~/.weatherlog/[profile name]/weather.json on Linux.
        data_file = open("%s/profiles/%s/weather.json" % (main_dir, last_profile), "r")
        data = json.load(data_file)
        data_file.close()
        
    except IOError:
        # Show the error message, and close the application.
        # This one shows if there was a problem reading the file.
        print("Error importing data (IOError).")
        sys.exit()
        
    except (TypeError, ValueError):
        # Show the error message, and close the application.
        # This one shows if there was a problem with the data type.
        print("Error importing data (TypeError or ValueError).")
        sys.exit()
    
    return data
    
