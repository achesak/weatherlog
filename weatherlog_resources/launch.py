# -*- coding: utf-8 -*-


# This file defines the functions for launching and setting up the application.


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
            
            # Set the profile name.
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

