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
# Import json for saving the configuration file.
import json
# Import datetime for getting the current time.
import datetime
# Import pickle for loading and saving the data.
import pickle


def write_dataset(main_dir="", name="", filename="", data=""):
    """Writes the data to the dataset file."""

    # Get the filename.
    filename = filename if filename != "" else "%s/datasets/%s/weather" % (main_dir, name)

    if data == "":
        data = []

    try:
        data_file = open(filename, "wb")
        pickle.dump(data, data_file)
        data_file.close()
        return True

    except IOError as e:
        print("write_dataset(): Error saving dataset file (IOError):\n%s" % e)
        return False

    except (TypeError, ValueError) as e:
        print("write_dataset(): Error saving dataset file (TypeError or ValueError):\n%s" % e)
        return False


def read_dataset(main_dir="", name="", filename=""):
    """Reads the data from the dataset file."""

    # Get the filename.
    filename = filename if filename != "" else "%s/datasets/%s/weather" % (main_dir, name)

    try:
        data_file = open(filename, "rb")
        data = pickle.load(data_file)
        data_file.close()

    except IOError as e:
        print("read_dataset(): Error importing data (IOError):\n%s" % e)
        data = []

    except (TypeError, ValueError) as e:
        print("read_dataset(): Error importing data (TypeError or ValueError):\n%s" % e)
        data = []

    return data


def write_blank_dataset(main_dir, name):
    """Writes a blank dataset file."""

    try:
        os.makedirs("%s/datasets/%s" % (main_dir, name))
        new_prof_file = open("%s/datasets/%s/weather" % (main_dir, name), "wb")
        pickle.dump([], new_prof_file)
        new_prof_file.close()
    
    except IOError as e:
        print("write_blank_dataset(): Error saving dataset file (IOError):\n%s" % e)

    except (TypeError, ValueError) as e:
        print("write_blank_dataset(): Error saving dataset file (TypeError or ValueError):\n%s" % e)


def write_standard_file(filename, data):
    """Writes a basic file."""

    try:
        data_file = open(filename, "w")
        data_file.write(data)
        data_file.close()

    except IOError as e:
        print("write_standard_file(): Error saving data file (IOError):\n%s" % e)


def write_json_file(filename, data, indent=False, indent_amount=4):
    """Writes a JSON file."""
    
    try:
        data_file = open(filename, "w")
        if indent:
            json.dump(data, data_file, indent=indent_amount)
        else:
            json.dump(data, data_file)
        data_file.close()

    except IOError as e:
        print("write_json_file(): Error saving data file (IOError):\n%s" % e)
    
    except (TypeError, ValueError) as e:
        print("write_json_file(): Error saving data file (TypeError or ValueError):\n%s" % e)


def get_dataset_list(main_dir, last_dataset, exclude_current=True):
    """Gets the list of datasets."""

    # Remember the correct directory and switch to where the datasets are stored.
    current_dir = os.getcwd()
    os.chdir("%s/datasets" % main_dir)

    # Get the list of datasets and sort the list.
    datasets = glob.glob("*")
    if exclude_current:
        datasets = list(set(datasets) - {last_dataset})
    datasets.sort()

    # Get the creation and last modified dates.
    for i in range(0, len(datasets)):

        # Get the dates.
        creation, modified = get_metadata(main_dir, datasets[i])
        datasets[i] = [datasets[i], creation, modified]

    # Switch back to the previous directory.
    os.chdir(current_dir)

    return datasets


def get_metadata(main_dir, last_dataset):
    """Gets the current metadata."""

    try:
        meta_file = open("%s/datasets/%s/metadata.json" % (main_dir, last_dataset), "r")
        meta_data = json.load(meta_file)
        meta_file.close()
        creation = meta_data["creation"]
        modified = meta_data["modified"]

    except IOError as e:
        print("get_metadata(): Error reading metadata file (IOError):\n%s" % e)
        creation = "Error"
        modified = "Error"
    
    except (TypeError, ValueError) as e:
        print("get_metadata(): Error reading metadata file (TypeError or ValueError):\n%s" % e)
        creation = "Error"
        modified = "Error"

    return creation, modified


def write_metadata(main_dir, last_dataset, creation="", modified="", now=False):
    """Writes the metadata file."""
    
    if now:
        now = datetime.datetime.now()
        creation = "%d/%d/%d" % (now.day, now.month, now.year)
        modified = creation

    try:
        meta_file = open("%s/datasets/%s/metadata.json" % (main_dir, last_dataset), "w")
        json.dump({"creation": creation, "modified": modified}, meta_file)
        meta_file.close()

    except IOError as e:
        print("write_metadata(): Error saving metadata file (IOError):\n%s" % e)
    
    except (TypeError, ValueError) as e:
        print("write_metadata(): Error saving metadata file (TypeError or ValueError):\n%s" % e)


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
        json.dump({
            "last_dataset": last_dataset,
            "window_height": window_height,
            "window_width": window_width
        }, rest_file)
        rest_file.close()

    except IOError as e:
        print("write_restore_data(): Error saving application restore file (IOError):\n%s" % e)
    
    except (TypeError, ValueError) as e:
        print("write_restore_data(): Error saving application restore file (TypeError or ValueError):\n%s" % e)
