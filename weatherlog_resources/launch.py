# -*- coding: utf-8 -*-


# This file defines the functions for launching and setting up the application.


# Import json for loading and saving the data.
import json
# Import platform for getting the user's operating system.
import platform
# Import os for creating a directory and other tasks.
import os
# Import sys for closing the application.
import sys
# Import glob for getting a list of directories.
import glob
# Import datetime for getting the current time.
import datetime
# Import pickle for loading and saving the data.
try:
    import cPickle as pickle
except ImportError:
    import pickle


def get_main_dir():
    """Returns the main directory."""

    # Windows:
    # * Data: C:\Users\[username]\AppData\Local\weatherlog
    # * Config: C:\Users\[username]\AppData\Local\weatherlog
    # Linux:
    # * Data: /home/[username]/.share/local/weatherlog
    # * Config: /home/[username]/.config/weatherlog/
    # OSX: probably the same as Linux?
    if platform.system().lower() == "windows":
        return os.environ["LOCALAPPDATA"] + "\weatherlog", os.environ["LOCALAPPDATA"] + "\weatherlog"
    else:
        base = os.path.expanduser("~")
        return base + "/.local/share/weatherlog", base + "/.config/weatherlog"


def get_ui_info():
    """Get the application's UI info."""
    
    try:
        ui_file = open("weatherlog_resources/ui.json", "r")
        ui_data = json.load(ui_file)
        ui_file.close()
    
    except IOError as e: 
        print("get_ui_info(): Error reading UI file (IOError):\n%s" % e)
        sys.exit()
    
    try:
        menu_file = open("weatherlog_resources/menu.xml", "r")
        menu_data = menu_file.read()
        menu_file.close()
    
    except IOError as e:
        print("get_ui_info(): Error reading menu file (IOError):\n%s" % e)
        sys.exit()
    
    version = ui_data["version"]
    title = ui_data["title"]
    icon_small = ui_data["icon_small"]
    icon_medium = ui_data["icon_medium"]
    icon_medium_about = ui_data["icon_medium_about"]
    return version, title, menu_data, icon_small, icon_medium


def get_weather_codes():
    """Get the weather codes."""
    
    try:
        codes_file = open("weatherlog_resources/weather_codes.json", "r")
        codes = json.load(codes_file)
        codes_file.close()
    
    except IOError as e: 
        print("get_weather_codes(): Error reading weather codes file (IOError):\n%s" % e)
        sys.exit()
    
    return codes


def check_files_exist(main_dir, conf_dir):
    """Checks to see if the base files exist, and create them if they don't."""

    # Check to see if the data directory exists, and create it if it doesn't.
    if not os.path.exists(main_dir) or not os.path.isdir(main_dir):

        # Create the default data directory and files.
        os.makedirs(main_dir)
        os.makedirs("%s/profiles/Main Dataset" % main_dir)
        last_prof_data = open("%s/profiles/Main Dataset/weather" % main_dir, "w")
        pickle.dump([], last_prof_data)
        last_prof_data.close()
        create_metadata(main_dir, "Main Dataset")

    # Check to see if the configuration directory exists, and create it if it doesn't.
    if not os.path.exists(conf_dir) or not os.path.isdir(conf_dir):

        # Create the default configuration directory and files.
        os.makedirs(conf_dir)
        last_prof = open("%s/lastprofile" % conf_dir, "w")
        last_prof.write("Main Dataset")
        last_prof.close()


def get_last_profile(main_dir, conf_dir):
    """Returns the last dataset, the original dataset to be loaded, and whether the dataset exists. Creates the dataset if it doesn't exist."""

    try:
        # Load the last dataset file.
        prof_file = open("%s/lastprofile" % conf_dir, "r")
        last_profile = prof_file.read().rstrip()
        prof_file.close()

        # Get the list of datasets.
        current_dir = os.getcwd()
        os.chdir("%s/profiles" % main_dir)
        profiles_list = glob.glob("*")
        os.chdir(current_dir)

        # Check if the dataset exists:
        if last_profile in profiles_list:
            profile_exists = True
            original_profile = ""
        else:
            profile_exists = False
            original_profile = last_profile

    except IOError as e:
        print("get_last_profile(): Error reading dataset file (IOError):\n%s" % e)
        sys.exit()

    # If the dataset doesn't exist, switch or make one that does:
    if not profile_exists:

        # If the default dataset exists, switch to that.
        if "Main Dataset" in profiles_list:
            last_profile = "Main Dataset"

        # Otherwise, create the dataset:
        else:

            # Create the Main Dataset directory and data file.
            os.makedirs("%s/profiles/Main Dataset" % main_dir)
            last_prof_data = open("%s/profiles/Main Dataset/weather" % main_dir, "w")
            pickle.dump([], last_prof_data)
            last_prof_data.close()
            create_metadata(main_dir, "Main Dataset")

            # Set the dataset name.
            last_profile = "Main Dataset"

    return last_profile, original_profile, profile_exists


def get_config(conf_dir, get_default = False):
    """Loads the settings."""
    
    default_config  = {"pre-fill": False,
                      "restore": True,
                      "location": "",
                      "units": "metric",
                      "pastebin": "d2314ff616133e54f728918b8af1500e",
                      "show_units": True,
                      "show_dates": True,
                      "confirm_del": True,
                      "show_pre-fill": True,
                      "confirm_exit": False,
                      "import_all": False,
                      "truncate_notes": True,
                      "graph_color": "#0000FF",
                      "line_width": 1,
                      "line_style": "Solid",
                      "hatch_style": "Solid"}

    # Get the configuration.
    try:
        config_file = open("%s/config" % conf_dir, "r")
        config = json.load(config_file)
        config_file.close()

    except IOError as e:
        # If there was an error, use the defaults instead.
        print("get_config(): Error reading config file (IOError):\n%s\nContinuing with default..." % e)
        config = default_config
    
    if get_default:
        config = default_config
    
    return config


def get_window_size(conf_dir, config):
    """Gets the last window size."""

    # If the user doesn't want to restore the window size, set the size to the defaults.
    if not config["restore"]:
        last_width = 900
        last_height = 500

    # Otherwise, get the previous window size.
    else:

        try:
            wins_file = open("%s/window_size" % conf_dir, "r")
            last_width = int(wins_file.readline())
            last_height = int(wins_file.readline())
            wins_file.close()

        except IOError as e:
            # If there was an error, use the default size instead.
            print("get_window_size(): Error reading window size file (IOError):\n%s\nContinuing with default..." % e)
            last_width = 900
            last_height = 500

    return last_width, last_height


def get_units(config):
    """Gets the units."""

    # Metric:
    if config["units"] == "metric":

        # Temperature is Celsius.
        # Precipitation is centimeters.
        # Wind speed is kilometers per hour.
        # Air pressure is hecto-pascals.
        units = {"temp": "°C",
                 "prec": "cm",
                 "wind": "kph",
                 "airp": "hPa",
                 "visi": "km"}

    # Imperial:
    elif config["units"] == "imperial":

        # Temperature is Fahrenheit.
        # Precipitation is inches.
        # Wind speed is miles per hour
        # Air pressure is millibars.
        units = {"temp": "°F",
                 "prec": "in",
                 "wind": "mph",
                 "airp": "mbar",
                 "visi": "mi"}

    return units


def get_data(main_dir, last_profile):
    """Gets the data."""

    try:
        # Load the data.
        data_file = open("%s/profiles/%s/weather" % (main_dir, last_profile), "r")
        data = pickle.load(data_file)
        data_file.close()

    except IOError as e:
        print("get_data(): Error importing data (IOError):\n%s" % e)
        sys.exit()

    except (TypeError, ValueError) as e:
        print("get_data(): Error importing data (TypeError or ValueError):\n%s" % e)
        sys.exit()

    return data


def create_metadata(main_dir, last_profile):
    """Creates the default metadata file."""

    # Get the current time.
    now = datetime.datetime.now()
    modified = "%d/%d/%d" % (now.day, now.month, now.year)

    # Write the metadata to the file.
    try:
        meta_file = open("%s/profiles/%s/metadata" % (main_dir, last_profile), "w")
        meta_file.write("%s\n%s" % (modified, modified))
        meta_file.close()

    except IOError as e:
        print("create_metadata(): Error saving metadata file (IOError):\n%s" % e)
