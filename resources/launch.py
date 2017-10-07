# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: launch.py
# This module sets up and launches the application.
#
################################################################################


# Import json for loading and saving the data.
import json
# Import platform for getting the user's operating system.
import platform
# Import os for creating a directory and other tasks.
import os
# Import sys for closing the application.
import sys
# Import pickle for loading and saving the data.
import pickle
    
# Import application modules.
from resources.openweathermap.codes import codes
import resources.io as io
import resources.datasets as datasets


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
        ui_file = open("resources/appdata/ui.json", "r")
        ui_data = json.load(ui_file)
        ui_file.close()
    
    except IOError as e: 
        print("get_ui_info(): Error reading UI file (IOError):\n%s" % e)
        sys.exit()
    
    except (TypeError, ValueError) as e:
        print("get_ui_info(): Error reading UI file (TypeError or ValueError):\n%s" % e)
        sys.exit()
    
    try:
        menu_file = open("resources/appdata/menu.xml", "r")
        menu_data = menu_file.read()
        menu_file.close()

    except IOError as e:
        print("get_ui_info(): Error reading menu file (IOError):\n%s" % e)
        sys.exit()

    except (TypeError, ValueError) as e:
        print("get_ui_info(): Error reading menu file (TypeError or ValueError):\n%s" % e)
        sys.exit()

    try:
        style_file = open("resources/appdata/style.css", "r")
        style_data = style_file.read()
        style_file.close()

    except IOError as e:
        print("get_ui_info(): Error reading style file (IOError):\n%s" % e)
        sys.exit()

    except (TypeError, ValueError) as e:
        print("get_ui_info(): Error reading style file (TypeError or ValueError):\n%s" % e)
        sys.exit()
    
    version = ui_data["version"]
    title = ui_data["title"]
    icon_small = ui_data["icon_small"]
    icon_medium = ui_data["icon_medium"]
    default_width = ui_data["default_width"]
    default_height = ui_data["default_height"]
    help_link = ui_data["help_link"]
    return version, title, menu_data, style_data, icon_small, icon_medium, default_width, default_height, help_link


def get_weather_codes():
    """Get the weather codes."""
    
    return codes


def ensure_files_exist(main_dir, conf_dir):
    """Checks to see if the base files exist, and create them if they don't."""

    # Dataset directory and files:
    if not os.path.exists(main_dir) or not os.path.isdir(main_dir):

        os.makedirs(main_dir)
        os.makedirs("%s/datasets/Main Dataset" % main_dir)
        last_prof_data = open("%s/datasets/Main Dataset/weather" % main_dir, "w")
        pickle.dump([], last_prof_data)
        last_prof_data.close()
        io.write_metadata(main_dir, "Main Dataset", now=True)

    # Configuration directory and files:
    if not os.path.exists(conf_dir) or not os.path.isdir(conf_dir):

        os.makedirs(conf_dir)


def get_config(conf_dir, get_default=False):
    """Loads the settings."""
    
    # Get the default configuration.
    try:
        default_config_file = open("resources/appdata/default_config.json", "r")
        default_config = json.load(default_config_file)
        default_config_file.close()
    
    except IOError as e:
        print("get_config(): Error reading default config file (IOError):\n%s" % e)
        sys.exit()
    
    except (TypeError, ValueError) as e:
        print("get_config(): Error reading default config file (TypeError or ValueError):\n%s" % e)
        sys.exit()

    # Get the configuration.
    try:
        config_file = open("%s/config.json" % conf_dir, "r")
        config = json.load(config_file)
        config_file.close()

    except IOError as e:
        print("get_config(): Error reading config file (IOError):\n%s\nContinuing with default..." % e)
        config = default_config
    
    except (TypeError, ValueError) as e:
        print("get_config(): Error reading config file (TypeError or ValueError):\n%s\nContinuing with default..." % e)
        config = default_config
    
    if get_default:
        config = default_config
    
    return config


def get_restore_data(main_dir, conf_dir, config, default_width, default_height, default_dataset="Main Dataset"):
    """Gets the last window size."""

    try:
        rest_file = open("%s/application_restore.json" % conf_dir, "r")
        rest_data = json.load(rest_file)
        rest_file.close()
        last_width = rest_data["window_width"]
        last_height = rest_data["window_height"]
        last_dataset = rest_data["last_dataset"]

    except IOError as e:
        print("get_window_size(): Error reading restore file (IOError):\n%s" % e,
              "Continuing with default...")
        last_width = default_width
        last_height = default_height
        last_dataset = default_dataset
    
    except (TypeError, ValueError) as e:
        print("get_window_size(): Error reading restore file (TypeError or ValueError):\n%s" % e,
              "Continuing with default...")
        last_width = default_width
        last_height = default_height
        last_dataset = default_dataset
    
    # Check if the dataset exists. 
    dataset_list = datasets.get_column(io.get_dataset_list(main_dir, "", False), 0)
    if last_dataset in dataset_list:
        dataset_exists = True
        original_dataset = ""
    else:
        dataset_exists = False
        original_dataset = last_dataset
    
    # If the dataset doesn't exist, switch or make one that does:
    if not dataset_exists:

        # If the default dataset exists, switch to that.
        if "Main Dataset" in dataset_list:
            last_dataset = "Main Dataset"

        # Otherwise, create the default dataset.
        else:
            ensure_files_exist(main_dir, conf_dir)
    
    # If the user doesn't want to restore the window size, set the size to the defaults.
    if not config["restore"]:
        return last_dataset, original_dataset, dataset_exists, default_width, default_height

    return last_dataset, original_dataset, dataset_exists, last_width, last_height


def get_units(config):
    """Gets the units."""
    
    try:
        units_file = open("resources/appdata/units.json", "r")
        units = json.load(units_file)
        units_file.close()
    
    except IOError as e:
        print("get_units(): Error reading units file (IOError):\n%s" % e)
        sys.exit()
    
    except (ValueError, TypeError) as e:
        print("get_units(): Error reading units file (ValueError or TypeError):\n%s" % e)
        sys.exit()
    
    return units[config["units"]]


def get_pastebin_constants():
    """Gets the Pastebin constants."""
    
    try:
        paste_file = open("resources/appdata/pastebin.json", "r")
        paste_constants = json.load(paste_file)
        paste_file.close()
    
    except IOError as e:
        print("get_pastebin_constants(): Error reading pastebin constants file (IOError):\n%s" % e)
        sys.exit()
    
    except (ValueError, TypeError) as e:
        print("get_pastebin_constants(): Error reading pastebin constants file (ValueError or TypeError):\n%s" % e)
        sys.exit()
    
    return paste_constants


def get_graph_data():
    """Gets the graph line and hatch data."""
    
    try:
        graph_file = open("resources/appdata/graphs.json", "r")
        graph_data = json.load(graph_file)
        graph_file.close()
    
    except IOError as e:
        print("get_graph_data(): Error reading graph data file (IOError):\n%s" % e)
        sys.exit()
    
    except (ValueError, TypeError) as e:
        print("get_graph_data(): Error reading graph data file (ValueError or TypeError):\n%s" % e)
        sys.exit()
    
    return graph_data
