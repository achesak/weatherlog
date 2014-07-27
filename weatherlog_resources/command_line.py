# -*- coding: utf-8 -*-


# This file defines the functions for the command line arguments.


# Import datetime for sorting based on dates.
import datetime
# Import json for loading and saving the data.
import json
# Import os for checking if files exist.
import os
# Import shutil for deleting files.
import shutil
# Import sys for printing output.
import sys


def add(data, main_dir, last_profile, args):
    """Adds a row of data."""
    
    # Get the arguments.
    date = args[2]
    temp = args[3]
    prec = args[4]
    wind = args[5]
    humi = args[6]
    airp = args[7]
    clou = args[8]
    if len(args) >= 10:
        note = args[9]
    else:
        note = ""
    
    try:
        
        # Append the data and sort the list.
        data.append([date, temp, prec, wind, humi, airp, clou, note])
        data = sorted(data, key = lambda x: datetime.datetime.strptime(x[0], '%d/%m/%Y'))
        
        # Save the data.
        data_file = open("%s/profiles/%s/weather.json" % (main_dir, last_profile), "w")
        json.dump(data, data_file)
        data_file.close()
        
    except IOError:
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error writing to the file.
        print("Error saving data file (IOError).")
    
    except TypeError:
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error with the data type.
        print("Error saving data file (TypeError).")
    
    except ValueError:
        # Show the error message if something happened, but continue.
        # This one is shown if the date is of the wrong format.
        print("Error saving data file (ValueError) - date format is likely invalid (needs to be %d/%m/%Y).")


def remove(data, main_dir, last_profile, args):
    """Removes a row of data."""
    
    # Get the index.
    index = int(args[2])
    
    try:
        
        # Remove the row and sort the list.
        del data[index]
        data = sorted(data, key = lambda x: datetime.datetime.strptime(x[0], '%d/%m/%Y'))
        
        # Save the data.
        data_file = open("%s/profiles/%s/weather.json" % (main_dir, last_profile), "w")
        json.dump(data, data_file)
        data_file.close()
        
    except IOError:
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error writing to the file.
        print("Error saving data file (IOError).")
    
    except (TypeError, ValueError):
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error with the data type.
        print("Error saving data file (TypeError or ValueError).")
    
    except IndexError:
        # Show the error message if something happened, but continue.
        # This one is shown if the index is invalid.
        print("Error saving data file (IndexError).")


def clear(main_dir, last_profile):
    """Clears the current profile."""
    
    # Clear the file.
    try:
        data_file = open("%s/profiles/%s/weather.json" % (main_dir, last_profile), "w")
        data_file.write("[]")
        data_file.close()
        
    except IOError:
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error writing to the file.
        print("Error saving data file (IOError).")
    
    except (TypeError, ValueError):
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error with the data type.
        print("Error saving data file (TypeError or ValueError).")


def switch_profile(main_dir, profile):
    """Switches profiles."""
    
    # Save the new profile name.
    try:
        # This should save to ~/.weatherlog/lastprofile on Linux.
        prof_file = open("%s/lastprofile" % main_dir, "w")
        prof_file.write(profile)
        prof_file.close()
        
    except IOError:
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error writing to the file.
        print("Error saving profile file (IOError).")


def add_profile(main_dir, profile):
    """Adds a new profile."""
    
    # If the profile name is already in use, cancel the action.
    if os.path.isdir("%s/profiles/%s" % (main_dir, profile)):
        print("Profile name is already is use.")
        
    # Otherwise if there are no problems with the name, add the profile.
    else:
        # Create the directory and file.
        os.makedirs("%s/profiles/%s" % (main_dir, profile))
        new_prof_file = open("%s/profiles/%s/weather.json" % (main_dir, profile), "w")
        new_prof_file.write("[]")
        new_prof_file.close()
    
    # Save the new profile name.
    try:
        # This should save to ~/.weatherlog/lastprofile on Linux.
        prof_file = open("%s/lastprofile" % main_dir, "w")
        prof_file.write(profile)
        prof_file.close()
        
    except IOError:
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error writing to the file.
        print("Error saving profile file (IOError).")


def remove_profile(main_dir, last_profile, profile):
    """Removes a profile."""
    
    # If this profile is the current one, cancel the action.
    if profile == last_profile:
        print("Profile is currently in use.")
    
    # Otherwise, remove the profile.
    else:
        
        try:
            # Delete the directory.
            shutil.rmtree("%s/profiles/%s" % (main_dir, profile))
        
        except:
            # Show the error message if something happened, but continue.
            # This one is shown if there was an error deleting the files.
            print("Error deleting profile. (Does the profile exist?)")


def options(py_version, config, main_dir):
    """Sets the options."""
    
    def get_input():
        """Gets input from the user."""
        
        # If this is running under python 2:
        if py_version == 2:
            user_input = raw_input()
        
        # If this is running under python 3:
        elif py_version == 3:
            user_input = input()
        
        # Return the user's input.
        return user_input
    
    # Ask the user for the options.
    print("----If nothing is entered the current value will be kept----")
    sys.stdout.write("Pre-fill data (current: %s) (True|False): " % config["pre-fill"])
    opt_prefill = get_input()
    sys.stdout.write("Save automatically (current: %s) (True|False): " % config["auto_save"])
    opt_autosave = get_input()
    sys.stdout.write("Confirm deletions (current: %s) (True|False): " % config["confirm_del"])
    opt_confirmdel = get_input()
    sys.stdout.write("Location (current: %s) (five ints): " % config["location"])
    opt_location = get_input()
    sys.stdout.write("Units (current: %s) (metric|imperial): " % config["units"])
    opt_units = get_input()
    sys.stdout.write("Escape windowed (current: %s) (ignore|minimize|close): " % config["escape_windowed"])
    opt_escwin = get_input()
    sys.stdout.write("Escape fullscreen (current: %s) (ignore|exit fullscreen|close): " % config["escape_fullscreen"])
    opt_escfull = get_input()
    sys.stdout.write("Restore window size (current: %s) (True|False): " % config["restore"])
    opt_restore = get_input()
    sys.stdout.write("Show dates in title (current: %s) (True|False): " % config["show_dates"])
    opt_showdates = get_input()
    sys.stdout.write("Show unit in list (current: %s) (True|False): " % config["show_units"])
    opt_showunits = get_input()
    sys.stdout.write("Show prefill dialog (current: %s) (True|False): " % config["show_pre-fill"])
    opt_showprefill = get_input()
    sys.stdout.write("Confirm exit (current: %s) (True|False): " % config["confirm_exit"])
    opt_confirmexit = get_input()
    
    # Set the options.
    if opt_prefill == "True":
        config["pre-fill"] = True
    elif opt_prefill == "False":
        config["pre-fill"] = False
    
    if opt_autosave == "True":
        config["auto_save"] = True
    elif opt_autosave == "False":
        config["auto_save"] = False
    
    if opt_confirmdel == "True":
        config["confirm_del"] = True
    elif opt_confirmdel == "False":
        config["confirm_del"] = False
    
    if opt_location:
        config["location"] = opt_location
    
    if opt_units:
        config["units"] = opt_units
    
    if opt_escwin:
        config["escape_windowed"] = opt_escwin
    
    if opt_escfull:
        config["escape_fullscreen"] = opt_escfull
    
    if opt_restore == "True":
        config["restore"] = True
    elif opt_restore == "False":
        config["restore"] = False
    
    if opt_showdates == "True":
        config["show_dates"] = True
    elif opt_showdates == "False":
        config["show_dates"] = False
    
    if opt_showunits == "True":
        config["show_units"] = True
    elif opt_showunits == "False":
        config["show_units"] = False
    
    if opt_showprefill == "True":
        config["show_pre-fill"] = True
    elif opt_showprefill == "False":
        config["show_pre-fill"] = False
    
    if opt_confirmexit == "True":
        config["confirm_exit"] = True
    elif opt_confirmexit == "False":
        config["confirm_exit"] = False
    
    # Save the configuration.
    try:
        config_file = open("%s/config" % main_dir, "w")
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


def reset_options(config, main_dir):
    """Resets the options."""
    
    # Set the config variables.
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
    
    # Save the configuration.
    try:
        config_file = open("%s/config" % main_dir, "w")
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


def window_size(main_dir, args):
    """Sets the window size."""
    
    # Get the window size.
    width = int(args[2])
    height = int(args[3])
    
    # Save the window size.
    try:
        wins_file = open("%s/window_size" % main_dir, "w")
        wins_file.write("%d\n%d" % (width, height))
        wins_file.close()
    
    except IOError:
        # Show the error message if something happened, but continue.
        # This one is shown if there was an error writing to the file.
        print("Error saving window size file (IOError).")
