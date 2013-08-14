# -*- coding: utf-8 -*-


################################################################################

# WeatherLog
# Version 1.0

# WeatherLog is an application for keeping track of the weather.

# Released under the MIT open source license:
license_text = """
Copyright (c) 2013 Adam Chesak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

################################################################################


# Import any needed modules.
# Import Gtk for the interface.
from gi.repository import Gtk, Gdk, GdkPixbuf
# Import json for loading and saving the data.
import json
# Import collections.Counter for getting how often items appear.
from collections import Counter
# Import webbrowser for opening websites in the user's browser.
import webbrowser
# Import datetime for getting the difference between two dates.
import datetime
# Import re for validating the data.
import re
# Import glob for getting a list of directories.
import glob
# Import shutil for removing a directory.
import shutil
# Import os for creating a directory.
import os
# Import os.path for seeing if a directory exists.
import os.path
# Import sys for sys.exit().
import sys
# Import urlopen and urlencode for opening a file from a URL.
# Try importing Python 3 module, then fall back to Python 2 if needed.
try:
    # Try importing for Python 3.
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2.
    from urllib import urlopen, urlencode

# Tell Python not to create bytecode files.
sys.dont_write_bytecode = True

# Import the application's UI data.
from resources.ui import *
# Import the functions for various tasks.
import resources.utility_functions as utility_functions
# Import the functions for getting the data.
import resources.info_functions as info_functions
# Import the functions for exporting the data.
import resources.export as export
# Import the function for converting the data.
import resources.convert as convert
# Import the dialogs.
from resources.dialogs.new_dialog import *
from resources.dialogs.info_dialog import *
from resources.dialogs.data_dialog import *
from resources.dialogs.add_profile_dialog import *
from resources.dialogs.switch_profile_dialog import *
from resources.dialogs.remove_profile_dialog import *
from resources.dialogs.info_range_dialog import *
from resources.dialogs.options_dialog import *


# Get the main directory.
main_dir = "%s/.weatherornot" % os.path.expanduser("~")

# Check to see if the directory exists, and create it if it doesn't.
dir_exists = True
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
    dir_exists = False

# Get the last profile.
try:
    # Load the last profile file.
    prof_file = open("%s/lastprofile" % main_dir, "r")
    last_profile = prof_file.read().rstrip()
    prof_file.close()

except IOError:
    # Show the error message, and close the application.
    # This one shows if there was a problem reading the file.
    print("Error reading profile file (IOError).")
    sys.exit()

# Get the configuration.
try:
    # Load the configuration file.
    config_file = open("%s/config" % main_dir, "r")
    config = json.load(config_file)
    config_file.close()

except IOError:
    # Continue.
    config = {"pre-fill": False,
              "location": "",
              "units": "metric",
              "pastebin": "d2314ff616133e54f728918b8af1500e"}

# Get the previous window size.
try:
    # Load the window size file.
    wins_file = open("%s/window_size" % main_dir, "r")
    last_width = int(wins_file.readline())
    last_height = int(wins_file.readline())
    wins_file.close()

except IOError:
    # Continue.
    last_width = 900
    last_height = 500

# Load the data.   
try:
    # This should be ~/.weatherornot/[profile name]/weather.json on Linux.
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


# Configure the units.
# Metric:
if config["units"] == "metric":
    
    units = {"temp": "°C",
             "prec": "cm",
             "wind": "kph",
             "airp": "hPa"}

# Imperial:
elif config["units"] == "imperial":
    
    units = {"temp": "°F",
             "prec": "in",
             "wind": "mph",
             "airp": "mbar"}


class Weather(Gtk.Window):
    """Shows the main application."""
    def __init__(self):
        """Create the application."""
        # Create the window.
        Gtk.Window.__init__(self, title = "WeatherLog")
        # Set the window size.
        self.set_default_size(last_width, last_height)
        # Set the icon.
        self.set_icon_from_file("resources/images/icon.png")
        # Use this variable to store the fullscreen state.
        self.fullscreen_state = False
        
        # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str, str, str, str, str, str, str, str)
        # Add the data.
        for i in data:
            self.liststore.append(i)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        # Create the Date column.
        date_text = Gtk.CellRendererText()
        self.date_col = Gtk.TreeViewColumn("Date", date_text, text = 0)
        self.treeview.append_column(self.date_col)
        # Create the Temperature column.
        temp_text = Gtk.CellRendererText()
        self.temp_col = Gtk.TreeViewColumn("Temperature (%s)" % units["temp"], temp_text, text = 1)
        self.treeview.append_column(self.temp_col)
        # Create the Precipation column.
        prec_text = Gtk.CellRendererText()
        self.prec_col = Gtk.TreeViewColumn("Precipitation (%s)" % units["prec"], prec_text, text = 2)
        self.treeview.append_column(self.prec_col)
        # Create the Wind column.
        wind_text = Gtk.CellRendererText()
        self.wind_col = Gtk.TreeViewColumn("Wind (%s)" % units["wind"], wind_text, text = 3)
        self.treeview.append_column(self.wind_col)
        # Create the Humidity column.
        humi_text = Gtk.CellRendererText()
        self.humi_col = Gtk.TreeViewColumn("Humidity (%)", humi_text, text = 4)
        self.treeview.append_column(self.humi_col)
        # Create the Air Pressure column.
        airp_text = Gtk.CellRendererText()
        self.airp_col = Gtk.TreeViewColumn("Air Pressure (%s)" % units["airp"], airp_text, text = 5)
        self.treeview.append_column(self.airp_col)
        # Create the Cloud Cover column.
        clou_text = Gtk.CellRendererText()
        self.clou_col = Gtk.TreeViewColumn("Cloud Cover", clou_text, text = 6)
        self.treeview.append_column(self.clou_col)
        # Create the Notes column.
        note_text = Gtk.CellRendererText()
        self.note_col = Gtk.TreeViewColumn("Notes", note_text, text = 7)
        self.treeview.append_column(self.note_col)
        
        # Create the ScrolledWindow for displaying the list with a scrollbar.
        scrolled_win = Gtk.ScrolledWindow()
        # The container should scroll both horizontally and vertically.
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        # Display the TreeView.
        scrolled_win.add(self.treeview)
        
        # Create the action group for the menus.
        action_group = Gtk.ActionGroup("actions")
        # Create the Weather menu.
        action_group.add_actions([
            ("weather_menu", None, "Weather"),
            ("add_new", Gtk.STOCK_ADD, "Add _New...", "<Control>n", "Add a new day to the list", self.add_new),
            ("remove", Gtk.STOCK_REMOVE, "Remo_ve...", "<Control>r", "Remove a day from the list", self.remove),
            ("import", Gtk.STOCK_OPEN, "_Import...", None, "Import data from a file", self.import_file),
            ("import_profile", None, "Import as New _Profile...", "<Control><Shift>o", None, self.import_new_profile),
            ("import_append", None, "Imp_ort and Merge...", None, None, self.import_append),
            ("export", Gtk.STOCK_SAVE, "_Export...", None, "Export data to a file", self.export_file)
        ])
        
        # Create the Weather -> Export to submenu.
        action_weather_info_group = Gtk.Action("export_menu", "E_xport to", None, None)
        action_group.add_action(action_weather_info_group)
        action_group.add_actions([
            ("export_html", None, "Export to _HTML...", "<Control><Alt>h", None, self.export_file_html),
            ("export_csv", None, "Export to _CSV...", "<Control><Alt>c", None, self.export_file_csv),
            ("export_pastebin", None, "Export to Paste_bin...", None, None, lambda x: self.export_pastebin("raw")),
            ("export_pastebin_html", None, "_Export to Pastebin (HTML)...", None, None, lambda x: self.export_pastebin("html")),
            ("export_pastebin_csv", None, "E_xport to Pastebin (CSV)...", None, None, lambda x: self.export_pastebin("csv")),
            ("info", Gtk.STOCK_INFO, "_Info...", "<Control>i", "Show info about the data", lambda x: self.show_info(event = "ignore", data = data))
        ])
        
        # Create the Weather -> More Info submenu.
        action_weather_info_group = Gtk.Action("info_menu", "_More Info", None, None)
        action_group.add_action(action_weather_info_group)
        action_group.add_actions([
            ("temperature", None, "_Temperature...", "<Control>t", None, lambda x: self.show_info_temp(event = "ignore", data = data)),
            ("precipitation", None, "_Precipitation...", "<Control>p", None, lambda x: self.show_info_prec(event = "ignore", data = data)),
            ("wind", None, "_Wind...", "<Control>w", None, lambda x: self.show_info_wind(event = "ignore", data = data)),
            ("humidity", None, "_Humidity...", "<Control>h", None, lambda x: self.show_info_humi(event = "ignore", data = data)),
            ("air_pressure", None, "_Air Pressure...", "<Control>a", None, lambda x: self.show_info_airp(event = "ignore", data = data)),
            ("cloud_cover", None, "_Cloud Cover...", "<Control>c", None, lambda x: self.show_info_clou(event = "ignore", data = data)),
            ("info_range", None, "Info in _Range...", "<Control><Shift>i", None, lambda x: self.info_range("General"))
        ])
        
        # Create the Weather -> More Info in Range submenu.
        action_weather_info_range_group = Gtk.Action("info_range_menu", "More Info in Ran_ge", None, None)
        action_group.add_action(action_weather_info_range_group)
        action_group.add_actions([
            ("temperature_range", None, "_Temperature in Range...", "<Control><Shift>t", None, lambda x: self.info_range("Temperature")),
            ("precipitation_range", None, "_Precipitation in Range...", "<Control><Shift>p", None, lambda x: self.info_range("Precipitation")),
            ("wind_range", None, "_Wind in Range...", "<Control><Shift>w", None, lambda x: self.info_range("Wind")),
            ("humidity_range", None, "_Humidity in Range...", "<Control><Shift>h", None, lambda x: self.info_range("Humidity")),
            ("air_pressure_range", None, "_Air Pressure in Range...", "<Control><Shift>a", None, lambda x: self.info_range("Air Pressure")),
            ("cloud_cover_range", None, "_Cloud Cover in Range...", "<Control><Shift>c", None, lambda x: self.info_range("Cloud Cover")),
            ("clear_data", Gtk.STOCK_CLEAR, "Clear Current _Data...", "<Control>d", "Clear the data", self.clear),
            ("clear_all", None, "Clear _All Data...", "<Control><Alt>d", None, self.clear_all),
            ("reload_current", None, "Reload Current Data...", "F5", None, None),
            ("reload_all", None, "Reload All Data...", "<Shift>F5", None, None),
            ("manual_save", None, "Manual Save", "<Control>m", None, self.save),
            ("fullscreen", Gtk.STOCK_FULLSCREEN, "Toggle _Fullscreen", "F11", "Toggle fullscreen", self.toggle_fullscreen),
            ("exit", Gtk.STOCK_QUIT, "_Quit...", None, "Close the application", lambda x: self.exit("ignore", "this"))
        ])
        
        # Create the Profiles menu.
        action_group.add_actions([
            ("profiles_menu", None, "Profiles"),
            ("switch_profile", None, "_Switch Profile...", "<Control><Shift>s", None, self.switch_profile),
            ("add_profile", None, "_Add Profile...", "<Control><Shift>n", None, self.add_profile),
            ("remove_profile", None, "_Remove Profile...", "<Control><Shift>d", None, self.remove_profile)
        ])
        
        # Create the Options menu.
        action_group.add_actions([
            ("options_menu", None, "Options"),
            ("options", None, "_Options", "F2", None, self.options)
        ])
        
        # Create the Help menu.
        action_group.add_actions([
            ("help_menu", None, "Help"),
            ("about", Gtk.STOCK_ABOUT, "_About...", "<Shift>F1", None, self.show_about),
            ("help", Gtk.STOCK_HELP, "_Help...", None, None, self.show_help)
        ])
        
        # Create the UI manager.
        ui_manager = Gtk.UIManager()
        ui_manager.add_ui_from_string(MENU_DATA)
        
        # Add the accelerator group to the toplevel window
        accel_group = ui_manager.get_accel_group()
        self.add_accel_group(accel_group)
        ui_manager.insert_action_group(action_group)
        
        # Create the grid for the UI.
        grid = Gtk.Grid()
        
        # Add the menubar.
        menubar = ui_manager.get_widget("/menubar")
        grid.add(menubar)
        
        # Add the toolbar.
        toolbar = ui_manager.get_widget("/toolbar")
        grid.attach_next_to(toolbar, menubar, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Add the ScrolledWindow with the TreeView.
        grid.attach_next_to(scrolled_win, toolbar, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Add the grid to the main window.
        self.add(grid)
        self.show_all()
        
        # Set the new title.
        self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
        
        # Bind the events.
        self.connect("key-press-event", self.keypress)
        self.connect("delete-event", self.delete_event)
    
    
    def keypress(self, widget, event):
        """Handles keypresses."""
        
        # If the Escape key was pressed and the application is in fullscreen,
        # change back to windowed mode.
        if Gdk.keyval_name(event.keyval) == "Escape" and self.fullscreen_state:
            
            # Toggle the fullscreen state.
            self.toggle_fullscreen("ignore")
        
        # If the Escape key was pressed and the application isn't in fullscreen,
        # iconify the window.
        elif Gdk.keyval_name(event.keyval) == "Escape" and not self.fullscreen_state:
            
            # iconify the window.
            self.iconify()
    
    
    def delete_event(self, widget, event):
        """Saves the window size."""
        
        # Get the current window size.
        height, width = self.get_size()
        
        # Save the window size.
        try:
            wins_file = open("%s/window_size" % main_dir, "w")
            wins_file.write("%d\n%d" % (height, width))
            wins_file.close()
        
        except IOError:
            # Show the error message if something happened, but continue.
            # This one is shown if there was an error writing to the file.
            print("Error saving window size file (IOError).")
    
    
    def add_new(self, event):
        """Shows the dialog for input of new data."""
        
        global data
        
        # Show the dialog.
        new_dlg = AddNewDialog(self, last_profile, config["location"], config["pre-fill"], units)
        # Get the response.
        response = new_dlg.run()
        
        # If the user clicked the OK button, add the data.
        if response == Gtk.ResponseType.OK:
            
            # Get the data from the entries and comboboxes.
            year, month, day = new_dlg.date_cal.get_date()
            date = "%d/%d/%d" % (day, month + 1, year)
            temp = new_dlg.temp_sbtn.get_value()
            prec = new_dlg.prec_sbtn.get_value()
            prec_type = new_dlg.prec_com.get_active_text()
            wind = new_dlg.wind_sbtn.get_value()
            wind_dir = new_dlg.wind_com.get_active_text()
            humi = new_dlg.humi_sbtn.get_value()
            airp = new_dlg.airp_sbtn.get_value()
            airp_read = new_dlg.airp_com.get_active_text()
            clou = new_dlg.clou_com.get_active_text()
            note = new_dlg.note_ent.get_text()
            
            # If the precipitation or wind are zero, set the appropriate type/direction to "None".
            if not prec:
                prec_type = "None"
            if not wind:
                wind_dir = "None"
            
            # If the date is already used, show the dialog.
            if date in utility_functions.get_column(data, 0):
                
                # Create the error dialog.
                err_miss_dlg = Gtk.MessageDialog(new_dlg, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Add New")
                err_miss_dlg.format_secondary_text("The date %s has already been entered." % date)
                
                # Show the error dialog.
                err_miss_dlg.run()
                
                # Close the error dialog and the "Add New" dialog. The second one
                # is needed because of a bug where the window will stop responding
                # to events, making it useless. Fix later!
                err_miss_dlg.destroy()
                new_dlg.destroy()
                
            else:
                
                # Add the data to the list.
                new_data = [date, ("%.2f" % temp), "%s%s" % ((("%.2f" % prec) + " " if prec_type != "None" else ""), prec_type), "%s%s" % ((("%.2f" % wind) + " " if wind_dir != "None" else ""), wind_dir), ("%.2f" % humi), ("%.2f %s" % (airp, airp_read)), clou, note]
                data.append(new_data)
                
                # Sort the list.
                data = sorted(data, key = lambda x: datetime.datetime.strptime(x[0], '%d/%m/%Y'))
                
                # Update the ListStore.
                self.liststore.clear()
                for i in data:
                    self.liststore.append(i)
        
        # Update the title.
        self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
        
        # Close the dialog.
        new_dlg.destroy()        
    
    
    def remove(self, event):
        """Removes a row of data from the list."""
        
        # Get the selected date.
        try:
            tree_sel = self.treeview.get_selection()
            tm, ti = tree_sel.get_selected()
            date = tm.get_value(ti, 0)
        
        except:
            # If nothing was selected, show a dialog and don't continue.
            
            # Tell the user there is nothing selected.
            sel_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Remove - %s" % last_profile)
            sel_dlg.format_secondary_text("No list item selected.")
            
            # Run then close the dialog.
            sel_dlg.run()
            sel_dlg.destroy()
            
            return
        
        # Confirm that the user wants to delete the row.
        rem_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "Confirm Remove - %s" % last_profile)
        rem_dlg.format_secondary_text("Are you sure you want to delete the data for %s?\n\nThis action cannot be undone." % date)
        
        # Get the response.
        response = rem_dlg.run()
        rem_dlg.destroy()
        
        # If the user doesn't want to overwrite, cancel the action.
        if response != Gtk.ResponseType.OK:
            return
        
        # Get the index of the date.
        index = utility_functions.get_column(data, 0).index(date)
        
        # Delete the index in the data.
        del data[index]
        
        # Refresh the ListStore.
        self.liststore.clear()
        for i in data:
            self.liststore.append(i)
        
        # Update the title.
        self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
    
    
    def info_range(self, info):
        """Gets the range for the info to display."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "%s Info - %s" % (info, last_profile))
            return
        
        # Get the first entered date.
        days, months, years = data[0][0].split("/")
        days = int(days)
        months = int(months) - 1
        years = int(years)
        
        # Get the last entered date.
        daye, monthe, yeare = data[len(data) - 1][0].split("/")
        daye = int(daye)
        monthe = int(monthe) - 1
        yeare = int(yeare)
        
        # Get the start date.
        start_dlg = InfoRangeDialog(self, last_profile, info, "starting", days, months, years)
        
        # Get the response.
        response1 = start_dlg.run()
        
        # If the user clicked OK:
        if response1 == Gtk.ResponseType.OK:
            
            # Get the date.
            year1, month1, day1 = start_dlg.info_cal.get_date()
            date1 = "%d/%d/%d" % (day1, month1 + 1, year1)
            
            # Check to make sure this date is valid, and cancel the action if not.
            if date1 not in utility_functions.get_column(data, 0):
                
                # Show the dialog.
                info_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "%s Info in Range - %s" % (info, last_profile))
                info_dlg.format_secondary_text("%s is not a valid date." % date1)
                  
                # Run then close the dialog.
                info_dlg.run()
                info_dlg.destroy()
                
                # Close the dialog.
                start_dlg.destroy()
                
                return
        
        # Otherwise, cancel the action.
        else:
            
            # Close the dialog.
            start_dlg.destroy()
            
            return
        
        # Close the dialog.
        start_dlg.destroy()
        
        # Get the end date.
        end_dlg = InfoRangeDialog(self, last_profile, info, "ending", daye, monthe, yeare)
        
        # Get the response.
        response2 = end_dlg.run()
        
        # If the user clicked OK:
        if response2 == Gtk.ResponseType.OK:
            
            # Get the date.
            year2, month2, day2 = end_dlg.info_cal.get_date()
            date2 = "%d/%d/%d" % (day2, month2 + 1, year2)
            
            # Check to make sure this date is valid, and cancel the action if not.
            if date2 not in utility_functions.get_column(data, 0):
                
                # Show the dialog.
                info_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "%s Info in Range - %s" % (info, last_profile))
                info_dlg.format_secondary_text("%s is not a valid date." % date1)
                  
                # Run then close the dialog.
                info_dlg.run()
                info_dlg.destroy()
                
                # Close the dialog.
                end_dlg.destroy()
                
                return
            
            # Check to make sure this date is not the same as or earlier than the starting date,
            # and canel the action if it is.
            elif date2 == date1 or (day1, month1 + 1, year1) > (day2, month2 + 1, year2):
                
                # Show the dialog.
                info_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "%s Info in Range - %s" % (info, last_profile))
                info_dlg.format_secondary_text("The ending date must not be before or the same as the starting date.")
                  
                # Run then close the dialog.
                info_dlg.run()
                info_dlg.destroy()
                
                # Close the dialog.
                end_dlg.destroy()
                
                return
        
        # Otherwise, cancel the action.
        else:
            
            # Close the dialog.
            end_dlg.destroy()
            
            return
        
        # Close the dialog.
        end_dlg.destroy()
        
        # Get the indices.
        date_col = utility_functions.get_column(data, 0)
        index1 = date_col.index(date1)
        index2 = date_col.index(date2)
        
        # Get the new list.
        data2 = data[index1:index2 + 1]
        
        # Pass the data to the appropriate function.
        if info == "General":
            self.show_info(False, data2)
        elif info == "Temperature":
            self.show_info_temp(False, data2)
        elif info == "Precipitation":
            self.show_info_prec(False, data2)
        elif info == "Wind":
            self.show_info_wind(False, data2)
        elif info == "Humidity":
            self.show_info_humi(False, data2)
        elif info == "Air Pressure":
            self.show_info_airp(False, data2)
        elif info == "Cloud Cover":
            self.show_info_clou(False, data2)
    
    
    def show_info(self, event, data = data):
        """Shows info about the data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "General Info - %s" % last_profile)
            return
        
        # Get the date data.
        date_data = utility_functions.get_column(data, 0)
        date_first = date_data[0]
        date_last = date_data[len(date_data) - 1]
        date_first2 = datetime.datetime.strptime(date_first, "%d/%m/%Y")
        date_last2 = datetime.datetime.strptime(date_last, "%d/%m/%Y")
        date_num = (date_last2 - date_first2).days + 1
        
        # Get the temperature data.
        temp_data = utility_functions.convert_float(utility_functions.get_column(data, 1))
        temp_low = min(temp_data)
        temp_high = max(temp_data)
        temp_avg = info_functions.mean(temp_data)
        
        # Get the precipitation data.
        prec_data1, prec_data2 = utility_functions.split_list(utility_functions.get_column(data, 2))
        prec_data1 = utility_functions.convert_float(utility_functions.none_to_zero(prec_data1))
        try:
            prec_low = min(prec_data1)
            prec_high = max(prec_data1)
            prec_avg = info_functions.mean(prec_data1)
        except:
            prec_low = "None"
            prec_high = "None"
            prec_avg = "None"
        
        # Get the wind data.
        wind_data1, wind_data2 = utility_functions.split_list(utility_functions.get_column(data, 3))
        wind_data1 = utility_functions.convert_float(utility_functions.none_to_zero(wind_data1))
        try:
            wind_low = min(wind_data1)
            wind_high = max(wind_data1)
            wind_avg = info_functions.mean(wind_data1)
        except:
            wind_low = "None"
            wind_high = "None"
            wind_avg = "None"
        
        # Get the humidity data.
        humi_data = utility_functions.convert_float(utility_functions.get_column(data, 4))
        humi_low = min(humi_data)
        humi_high = max(humi_data)
        humi_avg = info_functions.mean(humi_data)
        
        # Get the air pressure data.
        airp_data1, airp_data2 = utility_functions.split_list(utility_functions.get_column(data, 5))
        airp_data1 = utility_functions.convert_float(airp_data1)
        airp_low = min(airp_data1)
        airp_high = max(airp_data1)
        airp_avg = info_functions.mean(airp_data1)
        
        # Get the cloud cover data.
        clou_data = Counter(utility_functions.get_column(data, 6))
        clou_mode = clou_data.most_common(1)[0][0]
        
        # Change any values, if needed.
        prec_low = "None" if prec_low == "None" else ("%.2f %s" % (prec_low, units["prec"]))
        prec_high = "None" if prec_high == "None" else ("%.2f %s" % (prec_high, units["prec"]))
        prec_avg = "None" if prec_avg == "None" else ("%.2f %s" % (prec_avg, units["prec"]))
        wind_low = "None" if wind_low == "None" else ("%.2f %s" % (wind_low, units["wind"]))
        wind_high = "None" if wind_high == "None" else ("%.2f %s" % (wind_high, units["wind"]))
        wind_avg = "None" if wind_avg == "None" else ("%.2f %s" % (wind_avg, units["wind"]))
        
        # Create the data list.
        data2 = [
            ["First day", "%s" % date_first],
            ["Last day", "%s" % date_last],
            ["Number of days", "%d" % date_num],
            ["Lowest temperature", "%.2f %s" % (temp_low, units["temp"])], 
            ["Highest temperature", "%.2f %s" % (temp_high, units["temp"])],
            ["Average temperature", "%.2f %s" % (temp_avg, units["temp"])],
            ["Lowest precipitation", prec_low],
            ["Highest precipitation", prec_high],
            ["Average precipitation", prec_avg],
            ["Lowest wind speed", wind_low],
            ["Highest wind speed", wind_high],
            ["Average wind speed", wind_avg],
            ["Lowest humidity", "%.2f%%" % humi_low], 
            ["Highest humidity", "%.2f%%" % humi_high],
            ["Average humidity", "%.2f%%" % humi_avg],
            ["Lowest air pressure", "%.2f %s" % (airp_low, units["airp"])],
            ["Highest air pressure", "%.2f %s" % (airp_high, units["airp"])],
            ["Average air pressure", "%.2f %s" % (airp_avg, units["airp"])],
            ["Most common cloud cover", "%s" % clou_mode]
        ]        
        
        # Show the dialog.
        info_dlg = GenericInfoDialog(self, "General Info - %s" % last_profile, data2)
        info_dlg.run()
        
        # Close the dialog. The response can be ignored.
        info_dlg.destroy()
    
    
    def show_info_temp(self, event, data = data):
        """Shows info about the temperature data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Temperature Info - %s" % last_profile)
            return
        
        # Get the data.
        temp_data = utility_functions.convert_float(utility_functions.get_column(data, 1))
        temp_low = min(temp_data)
        temp_high = max(temp_data)
        temp_avg = info_functions.mean(temp_data)
        temp_median = info_functions.median(temp_data)
        temp_range = info_functions.range(temp_data)
        temp_mode = info_functions.mode(temp_data)
        
        # Create the data list.
        data2 = [
            ["Lowest", "%.2f %s" % (temp_low, units["temp"])],
            ["Highest", "%.2f %s" % (temp_high, units["temp"])],
            ["Average", "%.2f %s" % (temp_avg, units["temp"])],
            ["Median", "%.2f %s" % (temp_median, units["temp"])],
            ["Range", "%.2f %s" % (temp_range, units["temp"])],
            ["Most common", "%.2f %s" % (temp_mode, units["temp"])]
        ]
        
        # Show the dialog.
        temp_dlg = GenericInfoDialog(self, "Temperature Info - %s" % last_profile, data2)
        temp_dlg.run()
        
        # Close the dialog. The response can be ignored.
        temp_dlg.destroy()
    
    
    def show_info_prec(self, event, data = data):
        """Shows info about the precipitation data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Precipitation Info - %s" % last_profile)
            return
        
        # Get the data.
        prec_data1, prec_data2 = utility_functions.split_list(utility_functions.get_column(data, 2))
        prec_split = utility_functions.split_list2(utility_functions.get_column(data, 2))
        prec_data1 = utility_functions.none_to_zero(prec_data1)
        prec_data1 = utility_functions.convert_float(prec_data1)
        try:
            prec_low = min(prec_data1)
            prec_high = max(prec_data1)
            prec_avg = info_functions.mean(prec_data1)
            prec_median = info_functions.median(prec_data1)
            prec_range = info_functions.range(prec_data1)
        except:
            prec_low = "None"
            prec_high = "None"
            prec_avg = "None"
            prec_median = "None"
            prec_range = "None"
        prec_total = 0
        prec_total_rain = 0
        prec_total_snow = 0
        prec_total_hail = 0
        prec_total_sleet = 0
        prec_none = 0
        prec_rain = 0
        prec_snow = 0
        prec_hail = 0
        prec_sleet = 0
        for i in prec_split:
            if i[1] != "None":
                prec_total += float(i[0])
            if i[1] == "None":
                prec_none += 1
            elif i[1] == "Rain":
                prec_total_rain += float(i[0])
                prec_rain += 1
            elif i[1] == "Snow":
                prec_total_snow += float(i[0])
                prec_snow += 1
            elif i[1] == "Hail":
                prec_total_hail += float(i[0])
                prec_hail += 1
            elif i[1] == "Sleet":
                prec_total_sleet += float(i[0])
                prec_hail += 1
        prec_mode = info_functions.mode(prec_data2)
        
        # Change any values, if needed.
        prec_low = "None" if prec_low == "None" else ("%.2f %s" % (prec_low, units["prec"]))
        prec_high = "None" if prec_high == "None" else ("%.2f %s" % (prec_high, units["prec"]))
        prec_avg = "None" if prec_avg == "None" else ("%.2f %s" % (prec_avg, units["prec"]))
        prec_median = "None" if prec_median == "None" else ("%.2f %s" % (prec_median, units["prec"]))
        prec_range = "None" if prec_range == "None" else ("%.2f %s" % (prec_range, units["prec"]))
        
        # Create the data list.
        data2 = [
            ["Lowest", prec_low],
            ["Highest", prec_high],
            ["Average", prec_avg],
            ["Median", prec_median],
            ["Range", prec_range],
            ["Total (all)", "%.2f %s" % (prec_total, units["prec"])],
            ["Total (rain)", "%.2f %s" % (prec_total_rain, units["prec"])],
            ["Total (snow)", "%.2f %s" % (prec_total_snow, units["prec"])],
            ["Total (hail)", "%.2f %s" % (prec_total_hail, units["prec"])],
            ["Total (sleet)", "%.2f %s" % (prec_total_sleet, units["prec"])],
            ["None", "%d day%s" % (prec_none, "" if prec_none == 1 else "s")],
            ["Rain", "%d day%s" % (prec_rain, "" if prec_rain == 1 else "s")],
            ["Snow", "%d day%s" % (prec_snow, "" if prec_snow == 1 else "s")],
            ["Hail", "%d day%s" % (prec_hail, "" if prec_hail == 1 else "s")],
            ["Sleet", "%d day%s" % (prec_sleet, "" if prec_sleet == 1 else "s")],
            ["Most common type", "%s" % (prec_mode if prec_mode != "" else "None")]
        ]
        
        # Show the dialog.
        prec_dlg = GenericInfoDialog(self, "Precipitation Info - %s" % last_profile, data2)
        prec_dlg.run()
        
        # Close the dialog. The response can be ignored.
        prec_dlg.destroy()
    
    
    def show_info_wind(self, event, data = data):
        """Shows info about the wind data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Wind Info - %s" % last_profile)
            return
        
        # Get the data.
        wind_data1, wind_data2 = utility_functions.split_list(utility_functions.get_column(data, 3))
        wind_data1 = utility_functions.none_to_zero(wind_data1)
        wind_data1 = utility_functions.convert_float(wind_data1)
        try:
            wind_low = min(wind_data1)
            wind_high = max(wind_data1)
            wind_avg = info_functions.mean(wind_data1)
            wind_median = info_functions.median(wind_data1)
            wind_range = info_functions.range(wind_data1)
        except:
            wind_low = "None"
            wind_high = "None"
            wind_avg = "None"
            wind_median = "None"
            wind_range = "None"
        wind_mode = info_functions.mode(wind_data2)
        
        # Change any values, if needed.
        wind_low = "None" if wind_low == "None" else ("%.2f %s" % (wind_low, units["wind"]))
        wind_high = "None" if wind_high == "None" else ("%.2f %s" % (wind_high, units["wind"]))
        wind_avg = "None" if wind_avg == "None" else ("%.2f %s" % (wind_avg, units["wind"]))
        wind_median = "None" if wind_median == "None" else ("%.2f %s" % (wind_median, units["wind"]))
        wind_range = "None" if wind_range == "None" else ("%.2f %s" % (wind_range, units["wind"]))
        
        # Create the data list.
        data2 = [
            ["Lowest", wind_low],
            ["Highest", wind_high],
            ["Average", wind_avg],
            ["Median", wind_median],
            ["Range", wind_range],
            ["Most common direction", "%s" % (wind_mode if wind_mode != "" else "None")]
        ]
        
        # Show the dialog.
        wind_dlg = GenericInfoDialog(self, "Wind Info - %s" % last_profile, data2)
        wind_dlg.run()
        
        # Close the dialog. The response can be ignored.
        wind_dlg.destroy()
    
    
    def show_info_humi(self, event, data = data):
        """Shows info about the humidity data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Humidity Info - %s" % last_profile)
            return
        
        # Get the data.
        humi_data = utility_functions.convert_float(utility_functions.get_column(data, 4))
        humi_low = min(humi_data)
        humi_high = max(humi_data)
        humi_avg = info_functions.mean(humi_data)
        humi_median = info_functions.median(humi_data)
        humi_range = info_functions.range(humi_data)
        humi_mode = info_functions.mode(humi_data)
        
        # Create the data list.
        data2 = [
            ["Lowest", "%.2f%%" % humi_low],
            ["Highest", "%.2f%%" % humi_high],
            ["Average", "%.2f%%" % humi_avg],
            ["Median", "%.2f%%" % humi_median],
            ["Range", "%.2f%%" % humi_range],
            ["Most common", "%.2f%%" % humi_mode]
        ]
        
        # Show the dialog.
        humi_dlg = GenericInfoDialog(self, "Humidity Info - %s" % last_profile, data2)
        humi_dlg.run()
        
        # Close the dialog. The response can be ignored.
        humi_dlg.destroy()
    
    
    def show_info_airp(self, event, data = data):
        """Shows info about the air pressure data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Air Pressure Info - %s" % last_profile)
            return
        
        # Get the data.
        airp_data1, airp_data2 = utility_functions.split_list(utility_functions.get_column(data, 5))
        airp_data1 = utility_functions.convert_float(airp_data1)
        airp_low = min(airp_data1)
        airp_high = max(airp_data1)
        airp_avg = info_functions.mean(airp_data1)
        airp_median = info_functions.median(airp_data1)
        airp_range = info_functions.range(airp_data1)
        airp_mode = info_functions.mode(airp_data1)
        airp_steady = 0
        airp_rising = 0
        airp_falling = 0
        for i in airp_data2:
            if i == "Steady":
                airp_steady += 1
            elif i == "Rising":
                airp_rising += 1
            elif i == "Falling":
                airp_falling += 1
        
        # Create the data list.
        data2 = [
            ["Lowest", "%.2f %s" % (airp_low, units["airp"])],
            ["Highest", "%.2f %s" % (airp_high, units["airp"])],
            ["Average", "%.2f %s" % (airp_avg, units["airp"])],
            ["Median", "%.2f %s" % (airp_median, units["airp"])],
            ["Range", "%.2f %s" % (airp_range, units["airp"])],
            ["Most common", "%.2f %s" % (airp_mode, units["airp"])],
            ["Steady", "%d day%s" % (airp_steady, "" if airp_steady == 1 else "s")],
            ["Rising", "%d day%s" % (airp_rising, "" if airp_rising == 1 else "s")],
            ["Falling", "%d day%s" % (airp_falling, "" if airp_falling == 1 else "s")]
        ]
        
        # Show the dialog.
        airp_dlg = GenericInfoDialog(self, "Air Pressure Info - %s" % last_profile, data2)
        airp_dlg.run()
        
        # Close the dialog. The response can be ignored.
        airp_dlg.destroy()
    
    
    def show_info_clou(self, event, data = data):
        """Shows info about the cloud cover data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Cloud Cover Info - %s" % last_profile)
            return
        
        # Get the data.
        # Put the items into a collection.
        clou_data = Counter(utility_functions.get_column(data, 6))
        # Find how many times the items appear.
        m_list = clou_data.most_common()
        # Convert the list to a dictionary.
        m_dict = {}
        for i in m_list:
            m_dict[i[0]] = i[1]
        
        # If any of the items don't appear, add dict items for them, with the values set to 0.
        if not "Sunny" in m_dict:
            m_dict["Sunny"] = 0
        if not "Mostly Sunny" in m_dict:
            m_dict["Mostly Sunny"] = 0
        if not "Partly Cloudy" in m_dict:
            m_dict["Partly Cloudy"] = 0
        if not "Mostly Cloudy" in m_dict:
            m_dict["Mostly Cloudy"] = 0
        if not "Cloudy" in m_dict:
            m_dict["Cloudy"] = 0
        
        # Create the data list.
        data2 = [
            ["Sunny", "%s day%s" % (m_dict["Sunny"], "" if m_dict["Sunny"] == 1 else "s")],
            ["Mostly Sunny", "%s day%s" % (m_dict["Mostly Sunny"], "" if m_dict["Mostly Sunny"] == 1 else "s")],
            ["Partly Cloudy", "%s day%s" % (m_dict["Partly Cloudy"], "" if m_dict["Partly Cloudy"] == 1 else "s")],
            ["Mostly Cloudy", "%s day%s" % (m_dict["Mostly Cloudy"], "" if m_dict["Mostly Cloudy"] == 1 else "s")],
            ["Cloudy", "%s day%s" % (m_dict["Cloudy"], "" if m_dict["Cloudy"] == 1 else "s")]
        ]
        
        # Show the dialog.
        clou_dlg = GenericInfoDialog(self, "Cloud Cover Info - %s" % last_profile, data2)
        clou_dlg.run()
        
        # Close the dialog. The response can be ignored.
        clou_dlg.destroy()
    
    
    def import_file(self, event):
        """Imports data from a file."""
        
        # Create the dialog.
        import_dlg = Gtk.FileChooserDialog("Import - %s" % last_profile, self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        # Set the filters.
        filter_all = Gtk.FileFilter()
        filter_all.set_name("All files")
        filter_all.add_pattern("*")
        filter_json = Gtk.FileFilter()
        filter_json.set_name("WeatherLog data files")
        filter_json.add_pattern("*.json")
        
        # Add the filters.
        import_dlg.add_filter(filter_all)
        import_dlg.add_filter(filter_json)
        
        # Get the response.
        response = import_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Confirm that the user wants to overwrite the data.
            over_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "Confirm Import - %s" % last_profile)
            over_dlg.format_secondary_text("Are you sure you want to import the data?\n\nCurrent data will be overwritten.")
            
            # Get the response.
            response = over_dlg.run()
            over_dlg.destroy()
            
            # If the user doesn't want to overwrite, cancel the action.
            if response != Gtk.ResponseType.OK:
                import_dlg.destroy()
                return
            
            # Get the filename.
            filename = import_dlg.get_filename()
            
            # Clear the data.
            global data
            data[:] = []
            # Clear the ListStore.
            self.liststore.clear()
            
            # Read the data.
            try:
                # Read from the specified file. 
                data_file = open(filename, "r")
                data = json.load(data_file)
                data_file.close()
                
            except IOError:
                # Show the error message, and don't add the data.
                # This one shows if there was a problem reading the file.
                print("Error importing data (IOError).")
            
            except (TypeError, ValueError):
                # Show the error message, and don't add the data.
                # This one shows if there was a problem with the data type.
                print("Error importing data (TypeError or ValueError).")
            
            else:
                # Add the new data.
                for i in data:
                    self.liststore.append(i)
            
        # Close the dialog.
        import_dlg.destroy()
    
    
    def import_append(self, event):
        """Imports data and merges it into the current list."""
        
        global data
        
        # Create the dialog.
        import_dlg = Gtk.FileChooserDialog("Import and Merge - %s" % last_profile, self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        # Set the filters.
        filter_all = Gtk.FileFilter()
        filter_all.set_name("All files")
        filter_all.add_pattern("*")
        filter_json = Gtk.FileFilter()
        filter_json.set_name("WeatherLog data files")
        filter_json.add_pattern("*.json")
        
        # Add the filters.
        import_dlg.add_filter(filter_all)
        import_dlg.add_filter(filter_json)
        
        # Get the response.
        response = import_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Get the filename.
            filename = import_dlg.get_filename()
            
            # Read the data.
            try:
                # Read from the specified file. 
                data_file = open(filename, "r")
                data2 = json.load(data_file)
                data_file.close()
                
            except IOError:
                # Show the error message, and don't add the data.
                # This one shows if there was a problem reading the file.
                print("Error importing data (IOError).")
            
            except (TypeError, ValueError):
                # Show the error message, and don't add the data.
                # This one shows if there was a problem with the data type.
                print("Error importing data (TypeError or ValueError).")
            
            else:
                
                # Filter the new data to make sure there are no duplicates.
                new_data = []
                date_col = utility_functions.get_column(data, 0)
                for i in data2:
                    
                    # If the date already appears, don't include it.
                    if i[0] not in date_col:
                        new_data.append(i)
                
                # Append the data.
                data += new_data
                
                # Sort the data.
                data = sorted(data, key = lambda x: datetime.datetime.strptime(x[0], '%d/%m/%Y'))
                
                # Update the ListStore.
                self.liststore.clear()
                for i in data:
                    self.liststore.append(i)
                
                # Update the title.
                self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
            
        # Close the dialog.
        import_dlg.destroy()        
    
    
    def import_new_profile(self, event):
        """Imports data from a file and inserts it in a new profile."""
        
        global last_profile
        global data
        
        # Show the dialog.
        new_dlg = AddProfileDialog(self)
        # Get the response.
        response = new_dlg.run()
        name = new_dlg.add_ent.get_text()
        
        # If the OK button was pressed:
        if response == Gtk.ResponseType.OK:
            
            # Validate the name. If it contains a non-alphanumeric character or is just space,
            # show a dialog and cancel the action.
            if re.compile("[^a-zA-Z1-90 \.\-\+\(\)\?\!]").match(name) or not name or name.lstrip().rstrip() == "" or name.startswith("."):
                
                # Create the error dialog.
                err_new_dlg = Gtk.MessageDialog(new_dlg, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Add Profile")
                err_new_dlg.format_secondary_text("The profile name \"%s\" is not valid.\n\n1. Profile names may not be blank.\n2. Profile names may not be all spaces.\n3. Profile names may only be letters, numbers, and spaces.\n4. Profile names may not start with a period (\".\")." % name)
                
                # Show then close the error dialog.
                err_new_dlg.run()
                err_new_dlg.destroy()
                
                new_dlg.destroy()
                return
            
            # If the profile name is already in use, show a dialog and cancel the action.
            elif os.path.isdir("%s/profiles/%s" % (main_dir, name)):
                
                # Create the error dialog.
                err_new_dlg = Gtk.MessageDialog(new_dlg, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Add Profile")
                err_new_dlg.format_secondary_text("The profile name \"%s\" is already in use." % name)
                
                # Show then close the error dialog.
                err_new_dlg.run()
                err_new_dlg.destroy()
                
                new_dlg.destroy()
                return
            
            # Otherwise if there are no problems with the name, add the profile.
            else:
                
                # Save the current data.
                try:
                    # This should save to ~/.weatherornot/[profile name]/weather.json on Linux.
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
                
                # Create the directory and file.
                last_profile = name
                os.makedirs("%s/profiles/%s" % (main_dir, name))
                open("%s/profiles/%s/weather.json" % (main_dir, name), "w").close()
                
                # Clear the old data.
                data[:] = []
                self.liststore.clear()
                
                # Set the new title.
                self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
        
            # Close the dialog.
            new_dlg.destroy()
        
        # Otherwise, close the dialog and don't go any further.
        else:
            
            new_dlg.destroy()
            return
        
        # Create the dialog.
        import_dlg = Gtk.FileChooserDialog("Import - %s" % last_profile, self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        # Set the filters.
        filter_all = Gtk.FileFilter()
        filter_all.set_name("All files")
        filter_all.add_pattern("*")
        filter_json = Gtk.FileFilter()
        filter_json.set_name("WeatherLog data files")
        filter_json.add_pattern("*.json")
        
        # Add the filters.
        import_dlg.add_filter(filter_all)
        import_dlg.add_filter(filter_json)
        
        # Get the response.
        response = import_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Get the filename.
            filename = import_dlg.get_filename()
            
            # Clear the data.
            data[:] = []
            # Clear the ListStore.
            self.liststore.clear()
            
            # Read the data.
            try:
                # Read from the specified file. 
                data_file = open(filename, "rb")
                data = json.load(data_file)
                data_file.close()
                
            except IOError:
                # Show the error message, and don't add the data.
                # This one shows if there was a problem reading the file.
                print("Error importing data (IOError).")
            
            except (TypeError, ValueError):
                # Show the error message, and don't add the data.
                # This one shows if there was a problem with the data type.
                print("Error importing data (TypeError or ValueError).")
            
            else:
                # Add the new data.
                for i in data:
                    self.liststore.append(i)
            
        # Close the dialog.
        import_dlg.destroy()
        
    
    def export_file(self, event):
        """Exports the data to a file."""
        
        # If there is no data, tell the user and cancel the action.
        if len(data) == 0:
            
            # Tell the user there is no data to export,
            expo_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Export - %s" % last_profile)
            expo_dlg.format_secondary_text("There is no data to export.")
            
            # Run then close the dialog.
            expo_dlg.run()
            expo_dlg.destroy()
            
            return
        
        # Create the dialog.
        export_dlg = Gtk.FileChooserDialog("Export - %s" % last_profile, self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        export_dlg.set_do_overwrite_confirmation(True)
        
        # Get the response.
        response = export_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Get the filename.
            filename = export_dlg.get_filename()
            
            # Save the data.
            try:
                # Write to the specified file.
                data_file = open(filename, "w")
                json.dump(data, data_file, indent = 4)
                data_file.close()
                
            except IOError:
                # Show the error message.
                # This only shows if the error occurred when writing to the file.
                print("Error exporting data (IOError).")
            
            except (TypeError, ValueError):
                # Show the error message.
                # This one is shown if there was an error with the data type.
                print("Error exporting data (TypeError or ValueError).")
            
        # Close the dialog.
        export_dlg.destroy()
    
    
    def export_file_html(self, event):
        """Formats the data into a HTML table, then exports it to a file."""
        
        # If there is no data, tell the user and cancel the action.
        if len(data) == 0:
            
            # Tell the user there is no data to export,
            expo_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Export to HTML - %s" % last_profile)
            expo_dlg.format_secondary_text("There is no data to export.")
            
            # Run then close the dialog.
            expo_dlg.run()
            expo_dlg.destroy()
            
            return
        
        # Convert to data to HTML.
        html = export.html(data, units)
        
        # Create the dialog.
        export_html_dlg = Gtk.FileChooserDialog("Export to HTML - %s" % last_profile, self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        export_html_dlg.set_do_overwrite_confirmation(True)
        
        # Get the response.
        response = export_html_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Get the filename.
            filename = export_html_dlg.get_filename()
            
            # Save the data.
            try:
                # Write to the specified file.
                data_file = open(filename, "w")
                data_file.write(html)
                data_file.close()
                
            except IOError:
                # Show the error message.
                # This only shows if the error occurred when writing to the file.
                print("Error exporting data to HTML (IOError).")
            
        # Close the dialog.
        export_html_dlg.destroy()
    
    
    def export_file_csv(self, event):
        """Formats the data into CSV, then exports it to a file."""
        
        # If there is no data, tell the user and cancel the action.
        if len(data) == 0:
            
            # Tell the user there is no data to export,
            expo_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Export to CSV - %s" % last_profile)
            expo_dlg.format_secondary_text("There is no data to export.")
            
            # Run then close the dialog.
            expo_dlg.run()
            expo_dlg.destroy()
            
            return
        
        # Convert the data to CSV.
        csv = export.csv(data, units)
        
        # Create the dialog.
        export_csv_dlg = Gtk.FileChooserDialog("Export to CSV - %s" % last_profile, self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        export_csv_dlg.set_do_overwrite_confirmation(True)
        
        # Get the response.
        response = export_csv_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Get the filename.
            filename = export_csv_dlg.get_filename()
            
            # Save the data.
            try:
                # Write to the specified file.
                data_file = open(filename, "w")
                data_file.write(csv)
                data_file.close()
                
            except IOError:
                # Show the error.
                # This only shows if the error occurred when writing to the file.
                print("Error exporting data to CSV (IOError).")
            
        # Close the dialog.
        export_csv_dlg.destroy()
    
    
    def export_pastebin(self, mode):
        """Exports the data to Pastebin."""
        
        # If there is no data, tell the user and cancel the action.
        if len(data) == 0:
            
            # Tell the user there is no data to export.
            expo_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Export to Pastebin - %s" % last_profile)
            expo_dlg.format_secondary_text("There is no data to export.")
            
            # Run then close the dialog.
            expo_dlg.run()
            expo_dlg.destroy()
            
            return
        
        # Convert the data.
        if mode == "html":
            new_data = export.html(data, units)
        elif mode == "csv":
            new_data = export.csv(data, units)
        elif mode == "raw":
            new_data = json.dumps(data)
        
        # Build the api string.
        api = {"api_option": "paste",
               "api_dev_key": config["pastebin"],
               "api_paste_code": new_data}
        
        # Add the data type:
        if mode == "html":
            api["api_paste_format"] = "html5"
        elif mode == "raw":
            api["api_paste_format"] = "javascript"
        
        # Encode the api string.
        api = urlencode(api)
        
        # Upload the text.
        try:
            
            # Send the data.
            pastebin = urlopen("http://pastebin.com/api/api_post.php", api)
            
            # Read the result.
            result = pastebin.read()
            
            # Close the connection.
            pastebin.close()
            
            success = True
            
        except:
            
            success = False
        
        # Show the dialog telling the user either that there was an error or giving the URL.
        if success:
            
            # Tell the user the URL.
            expo_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Export to Pastebin - %s" % last_profile)
            expo_dlg.format_secondary_text("The data has been uploaded to Pastebin, and can be accessed at the following URL:\n\n%s" % result)
            
            # Run then close the dialog.
            expo_dlg.run()
            expo_dlg.destroy()
        
        else:
            
            # Tell the user there was an error
            expo_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Export to Pastebin - %s" % last_profile)
            expo_dlg.format_secondary_text("The data could not be uploaded to Pastebin.")
            
            # Run then close the dialog.
            expo_dlg.run()
            expo_dlg.destroy()
    
    
    def clear(self, event):
        """Clears the data."""
        
        # Confirm that the user wants to clear the data.
        clear_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "Confirm Clear Current Data - %s" % last_profile)
        clear_dlg.format_secondary_text("Are you sure you want to clear the data?\n\nThis action cannot be undone.")
        
        # Get the response.
        response = clear_dlg.run()
        
        # If the user confirms the clear:
        if response == Gtk.ResponseType.OK:
            
            # Clear the data.
            global data
            data[:] = []
            
            # Clear the ListStore.
            self.liststore.clear()
        
        # Close the dialog.
        clear_dlg.destroy()
        
        # Update the title.
        self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
    
    
    def clear_all(self, event):
        """Clears all data."""
        
        # Confirm that the user wants to clear the data.
        clear_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "Confirm Clear All Data - %s" % last_profile)
        clear_dlg.format_secondary_text("Are you sure you want to clear all the data?\n\nThis action cannot be undone, and requires a restart.")
        
        # Get the response.
        response = clear_dlg.run()
        
        # If the user confirms the clear:
        if response == Gtk.ResponseType.OK:
            
            # Clear the data.
            global data
            data[:] = []
            
            # Clear the ListStore.
            self.liststore.clear()
            
            # Delete all the files.
            shutil.rmtree(main_dir)
            
            # Tell the user data has been cleared and that it will now close.
            clear_dlg2 = Gtk.MessageDialog(clear_dlg, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Clear All Data - %s" % last_profile)
            clear_dlg2.format_secondary_text("All data has been cleared.\n\nWeatherLog will now close...")
            
            # Run then close the dialog.
            clear_dlg2.run()
            clear_dlg2.destroy()
            
            # Close the dialog.
            Gtk.main_quit()
        
        # Close the dialog.
        clear_dlg.destroy()
    
    
    def switch_profile(self, event):
        """Switches profiles."""
        
        global last_profile
        global data
        
        # Remember the currect directory and switch to where the profiles are stored.
        current_dir = os.getcwd()
        os.chdir("%s/profiles" % main_dir)
        
        # Get the list of profiles.
        profiles = glob.glob("*")
        
        # Remove the current profile from the list.
        profiles = list(set(profiles) - set([last_profile]))
        
        # Sort the profiles.
        profiles.sort()
        
        # Switch back to the previous directory.
        os.chdir(current_dir)
        
        # If there are no other profiles, tell the user and cancel the action.
        if len(profiles) == 0:
            
            # Tell the user there are no other profiles.
            prof_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Switch Profile")
            prof_dlg.format_secondary_text("There are no other profiles.")
            
            # Run then close the dialog.
            prof_dlg.run()
            prof_dlg.destroy()
            
            return
        
        # Show the dialog.
        swi_dlg = SwitchProfileDialog(self, profiles)
        # Get the response.
        response = swi_dlg.run()
        name = swi_dlg.swi_com.get_active_text()
        
        # If the OK button was pressed:
        if response == Gtk.ResponseType.OK:
            
            # If nothing was selected, show a dialog and cancel the action.
            if not name:
                
                # Create the error dialog.
                err_swi_dlg = Gtk.MessageDialog(swi_dlg, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Switch Profile")
                err_swi_dlg.format_secondary_text("No profile was selected.")
                
                # Show then close the error dialog.
                err_swi_dlg.run()
                err_swi_dlg.destroy()
            
            # Otherwise if there are no problems with the name, switch to the profile.
            else:
                
                # Save the current data.
                try:
                    # This should save to ~/.weatherornot/[profile name]/weather.json on Linux.
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
                
                # Clear the old data.
                data[:] = []
                self.liststore.clear()
                
                # Load the data.   
                try:
                    # This should be ~/.weatherornot/[profile name]/weather.json on Linux.
                    data_file = open("%s/profiles/%s/weather.json" % (main_dir, name), "r")
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
                
                # Switch to the new profile.
                last_profile = name
                for i in data:
                    self.liststore.append(i)
                
                # Set the new title.
                self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
        
        # Close the dialog.
        swi_dlg.destroy()
    
    
    def add_profile(self, event):
        """Adds a new profile."""
        
        global last_profile
        global data
        
        # Show the dialog.
        new_dlg = AddProfileDialog(self)
        # Get the response.
        response = new_dlg.run()
        name = new_dlg.add_ent.get_text()
        
        # If the OK button was pressed:
        if response == Gtk.ResponseType.OK:
            
            # Validate the name. If it contains a non-alphanumeric character or is just space,
            # show a dialog and cancel the action.
            if re.compile("[^a-zA-Z1-90 \.\-\+\(\)\?\!]").match(name) or not name or name.lstrip().rstrip() == "" or name.startswith("."):
                
                # Create the error dialog.
                err_new_dlg = Gtk.MessageDialog(new_dlg, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Add Profile")
                err_new_dlg.format_secondary_text("The profile name \"%s\" is not valid.\n\n1. Profile names may not be blank.\n2. Profile names may not be all spaces.\n3. Profile names may only be letters, numbers, and spaces.\n4. Profile names may not start with a period (\".\")." % name)
                
                # Show then close the error dialog.
                err_new_dlg.run()
                err_new_dlg.destroy()
            
            # If the profile name is already in use, show a dialog and cancel the action.
            elif os.path.isdir("%s/profiles/%s" % (main_dir, name)):
                
                # Create the error dialog.
                err_new_dlg = Gtk.MessageDialog(new_dlg, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Add Profile")
                err_new_dlg.format_secondary_text("The profile name \"%s\" is already in use." % name)
                
                # Show then close the error dialog.
                err_new_dlg.run()
                err_new_dlg.destroy()
            
            # Otherwise if there are no problems with the name, add the profile.
            else:
                
                # Save the current data.
                try:
                    # This should save to ~/.weatherornot/[profile name]/weather.json on Linux.
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
                
                # Create the directory and file.
                last_profile = name
                os.makedirs("%s/profiles/%s" % (main_dir, name))
                open("%s/profiles/%s/weather.json" % (main_dir, name), "w").close()
                
                # Clear the old data.
                data[:] = []
                self.liststore.clear()
                
                # Set the new title.
                self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
        
        # Close the dialog.
        new_dlg.destroy()
    
    
    def remove_profile(self, event):
        """Removes a profile."""
        
        global last_profile
        
        # Remember the currect directory and switch to where the profiles are stored.
        current_dir = os.getcwd()
        os.chdir("%s/profiles" % main_dir)
        
        # Get the list of profiles.
        profiles = glob.glob("*")
        
        # Remove the current profile from the list.
        profiles = list(set(profiles) - set([last_profile]))
        
        # Sort the profiles.
        profiles.sort()
        
        # Switch back to the previous directory.
        os.chdir(current_dir)
        
        # If there are no other profiles, tell the user and cancel the action.
        if len(profiles) == 0:
            
            # Tell the user there are no other profiles.
            prof_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Remove Profile")
            prof_dlg.format_secondary_text("There are no other profiles.")
            
            # Run then close the dialog.
            prof_dlg.run()
            prof_dlg.destroy()
            
            return
        
        # Show the dialog.
        rem_dlg = RemoveProfileDialog(self, profiles)
        # Get the response.
        response = rem_dlg.run()
        name = rem_dlg.rem_com.get_active_text()
        
        # If the OK button was pressed:
        if response == Gtk.ResponseType.OK:
            
            # If nothing was selected, show a dialog and cancel the action.
            if not name:
                
                # Create the error dialog.
                err_rem_dlg = Gtk.MessageDialog(rem_dlg, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Remove Profile")
                err_rem_dlg.format_secondary_text("No profile was selected.")
                
                # Show then close the error dialog.
                err_rem_dlg.run()
                err_rem_dlg.destroy()
            
            # If the selected profile is the current one, show a 
            # dialog and cancel the action.
            elif name == last_profile:
                
                # Create the error dialog.
                err_rem_dlg = Gtk.MessageDialog(rem_dlg, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Remove Profile")
                err_rem_dlg.format_secondary_text("The current profile cannot be deleted.")
                
                # Show then close the error dialog.
                err_rem_dlg.run()
                err_rem_dlg.destroy()
            
            # Otherwise remove the profile.
            else:
                
                # Confirm that the user wants to delete the profile.
                del_dlg = Gtk.MessageDialog(rem_dlg, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "Confirm Delete")
                del_dlg.format_secondary_text("Are you sure you want to delete the profile?\n\nThis action cannot be undone.")
                
                # Get the response.
                response = del_dlg.run()
                del_dlg.destroy()
                
                # If the user wants to continue:
                if response == Gtk.ResponseType.OK:
                    
                    # Delete the directory.
                    shutil.rmtree("%s/profiles/%s" % (main_dir, name))
        
        # Close the dialog.
        rem_dlg.destroy()
    
    
    def toggle_fullscreen(self, event):
        """Toggles fullscreen window."""
        
        # Turn fullscreen off:
        if self.fullscreen_state:
            self.unfullscreen()
            self.fullscreen_state = False
        
        # Turn fullscreen on:
        else:
            self.fullscreen()
            self.fullscreen_state = True
    
    
    def options(self, event):
        """Shows the Options dialog."""
        
        global units
        current_units = config["units"]
        
        # Create the dialog.
        opt_dlg = OptionsDialog(self, config)
        
        # Get the response.
        response = opt_dlg.run()
        
        # If the user pressed OK:
        if response == Gtk.ResponseType.OK:
            
            # Get the values.
            prefill = opt_dlg.pre_chk.get_active()
            location = opt_dlg.loc_ent.get_text()
            units_ = opt_dlg.unit_com.get_active_text().lower()
            
            # Set the configuration.
            config["pre-fill"] = prefill
            config["location"] = location
            config["units"] = units_
            
            # Configure the units.
            # Metric:
            if config["units"] == "metric":
                
                units = {"temp": "°C",
                         "prec": "cm",
                         "wind": "kph",
                         "airp": "hPa"}
            
            # Imperial:
            elif config["units"] == "imperial":
                
                units = {"temp": "°F",
                         "prec": "in",
                         "wind": "mph",
                         "airp": "mbar"}
            
            # Update the main window.
            self.temp_col.set_title("Temperature (%s)" % units["temp"])
            self.prec_col.set_title("Precipitation (%s)" % units["prec"])
            self.wind_col.set_title("Wind (%s)" % units["wind"])
            self.airp_col.set_title("Air Pressure (%s)" % units["airp"])
            
            # If the units changed, ask the user if they want to convert the data.
            if current_units != units_:
                
                # Ask the user if they want to convert the data.
                con_dlg = Gtk.MessageDialog(opt_dlg, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "Options")
                con_dlg.format_secondary_text("The units have changed from %s to %s.\n\nWould you like to convert the data to the new units?" % (current_units, units_))
                
                # Get the response.
                response = con_dlg.run()
                con_dlg.destroy()
                
                # If the user wants to continue:
                if response == Gtk.ResponseType.OK:
                    
                    # Convert the data.
                    new_data = convert.convert(data, units_)
                    
                    # Update the list.
                    data[:] = []
                    data[:] = new_data[:]
                    
                    # Update the ListStore.
                    self.liststore.clear()
                    for i in data:
                        self.liststore.append(i)
        
        # Close the dialog.
        opt_dlg.destroy()
    
    
    def save(self, show_dialog = True):
        """Saves the data."""
        
        # Save to the file.
        try:
            # This should save to ~/.weatherornot/[profile name]/weather.json on Linux.
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
        
        # Save the configuration.
        try:
            # Save the configuration file.
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
        
        # Save the last profile.
        try:
            # This should save to ~/.weatherornot/lastprofile on Linux.
            prof_file = open("%s/lastprofile" % main_dir, "w")
            prof_file.write(last_profile)
            prof_file.close()
            
        except IOError:
            # Show the error message if something happened, but continue.
            # This one is shown if there was an error writing to the file.
            print("Error saving profile file (IOError).")
        
        # Show the dialog, if specified.
        if show_dialog:
            
            # Show the dialog.
            sav_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Manual Save - %s" % last_profile)
            sav_dlg.format_secondary_text("Data has been saved.")
            
            # Run then close the dialog.
            sav_dlg.run()
            sav_dlg.destroy()
    
    
    def show_about(self, event):
        """Shows the About dialog."""
        
        # Load the icon.
        img_file = open("resources/images/icon.png", "rb")
        img_bin = img_file.read()
        img_file.close()
        
        # Get the PixBuf.
        loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        loader.write(img_bin)
        loader.close()
        pixbuf = loader.get_pixbuf()
        
        # Create the dialog.
        about_dlg = Gtk.AboutDialog()
        
        # Set the title.
        about_dlg.set_title("About WeatherLog")
        # Set the program name.
        about_dlg.set_program_name(TITLE)
        # Set the program icon.
        about_dlg.set_logo(pixbuf)
        # Set the program version.
        about_dlg.set_version(VERSION)
        # Set the comments.
        about_dlg.set_comments("WeatherLog is an application for keeping track of the weather\nand getting information about past trends.")
        # Set the copyright notice. Legal stuff, bleh.
        about_dlg.set_copyright("Copyright (c) 2013 Adam Chesak")
        # Set the authors. This is, of course, only me. I feel special.
        about_dlg.set_authors(["Adam Chesak <achesak@yahoo.com>"])
        # Set the license.
        about_dlg.set_license(license_text)
        # Set the website.
        about_dlg.set_website("http://poultryandprogramming.wordpress.com/")
        about_dlg.set_website_label("http://poultryandprogramming.wordpress.com/")
        
        # Show the dialog.
        about_dlg.show_all()
        
        # Run then close the dialog.
        about_dlg.run()
        about_dlg.destroy()

    
    def show_help(self, event):
        """Shows the help in a web browser."""
        
        # Open the help file.
        webbrowser.open_new("resources/help/help.html")    
    

    def exit(self, x, y):
        """Saves data and closes the application."""
        
        # Save the application.
        self.save(show_dialog = False)
        
        # Close the  application.
        Gtk.main_quit()


# Show the window and start the application.
if __name__ == "__main__":
    win = Weather()
    win.connect("delete-event", win.exit)
    win.show_all()
    Gtk.main()
