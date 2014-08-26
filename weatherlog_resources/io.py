# -*- coding: utf-8 -*-


# This file defines the functions for reading and writing profiles.


# Import os for creating directories.
import os
# Import glob for getting a list of the profiles.
import glob
# Import time for formatting times.
import time
# Import json for saving the configuration file.
import json
# Import pickle for loading and saving the data.
# Try importing cPickle (for most Python 2 implementations), then
# fall back to pickle (for Python 2 implementations lacking this module
# and Python 3) if needed.
try:
    import cPickle as pickle
except ImportError:
    import pickle


def write_profile(main_dir = "", name = "", filename = "", data = []):
    """Writes the data to the profile file."""
    
    # Get the filename.
    filename = filename if filename != "" else "%s/profiles/%s/weather" % (main_dir, name)
    
    # Write the data.
    try:
        # This should save to ~/.local/share/weatherlog/[profile name]/weather on Linux.
        data_file = open(filename, "w")
        pickle.dump(data, data_file)
        data_file.close()
        return True
    
    except IOError:
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error writing to the file.
        print("Error saving data file (IOError).")
        return False
    
    except (TypeError, ValueError):
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error with the data type.
        print("Error saving data file (TypeError or ValueError).")
        return False


def read_profile(main_dir = "", name = "", filename = ""):
    """Reads the data from the profile file."""
    
    # Get the filename.
    filename = filename if filename != "" else "%s/profiles/%s/weather" % (main_dir, name)
    
    # Load the data.   
    try:
        # This should be ~/.local/share/weatherlog/[profile name]/weather on Linux.
        data_file = open(filename, "r")
        data = pickle.load(data_file)
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
    new_prof_file = open("%s/profiles/%s/weather" % (main_dir, name), "w")
    pickle.dump([], new_prof_file)
    new_prof_file.close()


def write_standard_file(filename, data):
    """Writes a file without formatting it as JSON."""
    
    # Save the data.
    try:
        data_file = open(filename, "w")
        data_file.write(data)
        data_file.close()
        
    except IOError:
        # Show the error message.
        # This only shows if the error occurred when writing to the file.
        print("Error saving data file (IOError).")


def get_profile_list(main_dir, last_profile):
    """Gets the list of profiles."""
    
    # Remember the currect directory and switch to where the profiles are stored.
    current_dir = os.getcwd()
    os.chdir("%s/profiles" % main_dir)
    
    # Get the list of profiles, remove the current profile, and sort the list.
    profiles = glob.glob("*")
    profiles = list(set(profiles) - set([last_profile]))
    profiles.sort()
    
    # Get the creation and last modified dates.
    for i in range(0, len(profiles)):
        
        # Get the dates.
        creation, modified = get_metadata(main_dir, profiles[i])
        
        # Change the values in the list.
        profiles[i] = [profiles[i], creation, modified]
    
    # Switch back to the previous directory.
    os.chdir(current_dir)
    
    return profiles


def get_metadata(main_dir, last_profile):
    """Gets the current metadata."""
    
    # Read the creation date and last modified date.
    try:
        meta_file = open("%s/profiles/%s/metadata" % (main_dir, last_profile), "r")
        creation = meta_file.readline().strip()
        modified = meta_file.readline().strip()
        meta_file.close()
    
    except IOError:
        # Show the error message.
        # This only shows if the error occurred when reading from the file.
        print("Error reading metadata file (IOError).")
    
    return creation, modified


def write_metadata(main_dir, last_profile, creation, modified):
    """Writes the metadata file."""
    
    # Writes the metadata to the file.
    try:
        meta_file = open("%s/profiles/%s/metadata" % (main_dir, last_profile), "w")
        meta_file.write("%s\n%s" % (creation, modified))
        meta_file.close()
    
    except IOError:
        # Show the error message.
        # This only shows if the error occurred when writing to the file.
        print("Error saving metadata file (IOError).")


def write_config(conf_dir, config):
    """Saves the configuration."""
    
    try:
        # This should save to ~/.config/weatherlog/config on Linux.
        config_file = open("%s/config" % conf_dir, "w")
        json.dump(config, config_file)
        config_file.close()
        
    except IOError:
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error writing to the file.
        print("Error saving configuration file (IOError).")
    
    except (TypeError, ValueError):
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error with the data type.
        print("Error saving configuration file (TypeError or ValueError).")


def write_last_profile(conf_dir, last_profile):
    """Saves the last profile."""
    
    try:
        # This should save to ~/.config/weatherlog/lastprofile on Linux.
        prof_file = open("%s/lastprofile" % conf_dir, "w")
        prof_file.write(last_profile)
        prof_file.close()
        
    except IOError:
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error writing to the file.
        print("Error saving profile file (IOError).")
