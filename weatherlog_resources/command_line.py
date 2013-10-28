# -*- coding: utf-8 -*-


# This file defines the functions for the command line arguments.


# Import datetime for sorting based on dates.
import datetime
# Import json for loading and saving the data.
import json


def add(data, main_dir, last_profile, args):
    """Adds a row of data."""
    
    # Add a row of data:
    if args[1] == "add":
        
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
        
        # Save to the file.
        try:
            
            # Append the data.
            data.append([date, temp, prec, wind, humi, airp, clou, note])
            
            # Sort the list.
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
    
    # Save to the file.
    try:
        
        # Remove the row.
        del data[index]
        
        # Sort the list.
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
