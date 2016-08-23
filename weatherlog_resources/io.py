# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: io.py
# This module reads and writes dataset, metadata, and configuration files.
#
################################################################################


# Import os for creating directories.
import os
# Import glob for getting a list of the datasets.
import glob
# Import time for formatting times.
import time
# Import json for saving the configuration file.
import json
# Import pickle for loading and saving the data.
try:
    import cPickle as pickle
except ImportError:
    import pickle


def write_profile(main_dir = "", name = "", filename = "", data = []):
    """Writes the data to the dataset file."""

    # Get the filename.
    filename = filename if filename != "" else "%s/profiles/%s/weather" % (main_dir, name)

    try:
        data_file = open(filename, "w")
        pickle.dump(data, data_file)
        data_file.close()
        return True

    except IOError as e:
        print("write_profile(): Error saving dataset file (IOError):\n%s" % e)
        return False

    except (TypeError, ValueError) as e:
        print("write_profile(): Error saving dataset file (TypeError or ValueError):\n%s" % e)
        return False


def read_profile(main_dir = "", name = "", filename = ""):
    """Reads the data from the dataset file."""

    # Get the filename.
    filename = filename if filename != "" else "%s/profiles/%s/weather" % (main_dir, name)

    try:
        data_file = open(filename, "r")
        data = pickle.load(data_file)
        data_file.close()

    except IOError as e:
        print("read_profile(): Error importing data (IOError):\n%s" % e)
        data = []

    except (TypeError, ValueError) as e:
        print("read_profile(): Error importing data (TypeError or ValueError):\n%s" % e)
        data = []

    return data


def write_blank_profile(main_dir, name):
    """Writes a blank dataset file."""

    try:
        os.makedirs("%s/profiles/%s" % (main_dir, name))
        new_prof_file = open("%s/profiles/%s/weather" % (main_dir, name), "w")
        pickle.dump([], new_prof_file)
        new_prof_file.close()
    
    except IOError as e:
        print("write_blank_profile(): Error saving dataset file (IOError):\n%s" % e)
        data = []

    except (TypeError, ValueError) as e:
        print("write_blank_profile(): Error saving dataset file (TypeError or ValueError):\n%s" % e)
        data = []


def write_standard_file(filename, data):
    """Writes a basic file."""

    try:
        data_file = open(filename, "w")
        data_file.write(data)
        data_file.close()

    except IOError as e:
        print("write_standard_file(): Error saving data file (IOError):\n%s" % e)


def write_json_file(filename, data, indent = False, indent_amount = 4):
    """Writes a JSON file."""
    
    try:
        data_file = open(filename, "w")
        if indent:
            json.dump(data, data_file, indent = indent_amount)
        else:
            json.dump(data, data_file)
        data_file.close()

    except IOError as e:
        print("write_json_file(): Error saving data file (IOError):\n%s" % e)


def get_profile_list(main_dir, last_profile, exclude_current = True):
    """Gets the list of datasets."""

    # Remember the correct directory and switch to where the datasets are stored.
    current_dir = os.getcwd()
    os.chdir("%s/profiles" % main_dir)

    # Get the list of datasets and sort the list.
    profiles = glob.glob("*")
    if exclude_current:
        profiles = list(set(profiles) - set([last_profile]))
    profiles.sort()

    # Get the creation and last modified dates.
    for i in range(0, len(profiles)):

        # Get the dates.
        creation, modified = get_metadata(main_dir, profiles[i])
        profiles[i] = [profiles[i], creation, modified]

    # Switch back to the previous directory.
    os.chdir(current_dir)

    return profiles


def get_metadata(main_dir, last_profile):
    """Gets the current metadata."""

    try:
        meta_file = open("%s/profiles/%s/metadata.json" % (main_dir, last_profile), "r")
        meta_data = json.load(meta_file)
        meta_file.close()
        creation = meta_data["creation"]
        modified = meta_data["modified"]

    except IOError as e:
        print("get_metadata(): Error reading metadata file (IOError):\n%s" % e)
        creation = "Error"
        modified = "Error"

    return creation, modified


def write_metadata(main_dir, last_profile, creation, modified):
    """Writes the metadata file."""

    try:
        meta_file = open("%s/profiles/%s/metadata.json" % (main_dir, last_profile), "w")
        json.dump({"creation": creation, "modified": modified}, meta_file)
        meta_file.close()

    except IOError as e:
        print("write_metadata(): Error saving metadata file (IOError):\n%s" % e)


def write_config(conf_dir, config):
    """Saves the configuration."""

    try:
        config_file = open("%s/config.json" % conf_dir, "w")
        json.dump(config, config_file)
        config_file.close()

    except IOError as e:
        print("write_config(): Error saving configuration file (IOError):\n%s" % e)

    except (TypeError, ValueError) as e:
        print("write_config(): Error saving configuration file (TypeError or ValueError):\n%s" % e)


def write_restore_data(conf_dir, last_dataset, window_height, window_width):
    """Saves the last dataset and window size."""

    try:
        rest_file = open("%s/application_restore.json" % conf_dir, "w")
        json.dump({"last_dataset": last_dataset, "window_height": window_height, "window_width": window_width}, rest_file)
        rest_file.close()

    except IOError as e:
        print("write_last_profile(): Error saving application restore file (IOError):\n%s" % e)
