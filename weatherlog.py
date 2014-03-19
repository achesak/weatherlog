#!/usr/bin/env python
# -*- coding: utf-8 -*-


################################################################################

# WeatherLog
# Version 1.7.1

# WeatherLog is an application for keeping track of the weather and
# getting information about past trends.

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
# Import Gtk and Gdk for the interface.
from gi.repository import Gtk, Gdk, GdkPixbuf
# Import json for loading and saving the data.
import json
# Import collections.Counter for getting the mode of the data.
from collections import Counter
# Import webbrowser for opening the help in the user's browser.
import webbrowser
# Import datetime for getting the difference between two dates, and 
# for sorting based on dates.
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
# Import sys for closing the application.
import sys
# Import platform for getting the user's operating system.
import platform
# Import time for working with dates and times.
import time
# Import urlopen and urlencode for opening a file from a URL.
# Try importing Python 3 module, then fall back to Python 2 if needed.
try:
    # Try importing for Python 3.
    from urllib.request import urlopen
    from urllib.parse import urlencode
    py_version = 3
except ImportError:
    # Fall back to Python 2.
    from urllib import urlopen, urlencode
    py_version = 2

# Tell Python not to create bytecode files, as they mess with the git repo.
# This line can be removed be the user, if desired.
sys.dont_write_bytecode = True

# Import the application's UI data.
from weatherlog_resources.ui import VERSION, TITLE, MENU_DATA
# Import the functions for various tasks.
import weatherlog_resources.utility_functions as utility_functions
# Import the functions for getting and calculating the data.
import weatherlog_resources.info_functions as info_functions
# Import the functions for exporting the data.
import weatherlog_resources.export as export
# Import the function for exporting the info.
import weatherlog_resources.export_info as export_info
# Import the function for converting the data.
import weatherlog_resources.convert as convert
# Import the functions for getting the info.
import weatherlog_resources.info as info
# Import the functions for getting the chart data.
import weatherlog_resources.charts as charts
# Import the functions for handling command line arguments.
import weatherlog_resources.command_line as command_line
# Import the dialog for getting new data.
from weatherlog_resources.dialogs.new_dialog import AddNewDialog
# Import the dialog for editing a row of data.
from weatherlog_resources.dialogs.edit_dialog import EditDialog
# Import the dialog for displaying information.
from weatherlog_resources.dialogs.info_dialog import GenericInfoDialog
# Import the dialog for telling the user there is no data.
from weatherlog_resources.dialogs.data_dialog import show_no_data_dialog
# Import the dialog for adding a profile.
from weatherlog_resources.dialogs.add_profile_dialog import AddProfileDialog
# Import the dialog for switching profiles.
from weatherlog_resources.dialogs.switch_profile_dialog import SwitchProfileDialog
# Import the dialog for removing profiles.
from weatherlog_resources.dialogs.remove_profile_dialog import RemoveProfileDialog
# Import the dialog for renaming profiles.
from weatherlog_resources.dialogs.rename_profile_dialog import RenameProfileDialog
# Import the dialog for merging profiles.
from weatherlog_resources.dialogs.merge_profiles_dialog import MergeProfilesDialog
# Import the dialog for selecting dates to copy or move.
from weatherlog_resources.dialogs.profile_date_dialog import ProfileDateSelectionDialog
# Import the dialog for adding a new profile when moving/copying data.
from weatherlog_resources.dialogs.data_profile_new_dialog import ProfileDataNewDialog
# Import the dialog for choosing a profile when moving/copying data.
from weatherlog_resources.dialogs.data_profile_existing_dialog import ProfileDataExistingDialog
# Import the dialog for selecting a range of dates to show information about.
from weatherlog_resources.dialogs.info_range_dialog import InfoRangeDialog
# Import the dialog for selecting a range of dates to show a chart about.
from weatherlog_resources.dialogs.chart_range_dialog import ChartRangeDialog
# Import the dialog for changing the options.
from weatherlog_resources.dialogs.options_dialog import OptionsDialog
# Import the dialog for displaying the charts.
from weatherlog_resources.dialogs.chart_dialog import GenericChartDialog
# Import the dialog for selecting dates to show information about.
from weatherlog_resources.dialogs.info_selected_dialog import InfoSelectedDialog
# Import the dialog for selecting dates to show a chart about.
from weatherlog_resources.dialogs.chart_selected_dialog import ChartSelectedDialog
# Import the miscellaneous dialogs.
from weatherlog_resources.dialogs.misc_dialogs import show_alert_dialog, show_error_dialog, show_question_dialog


# Get the main directory.
if platform.system().lower() == "windows":
    main_dir = "C:\\.weatherlog"
else:
    main_dir = "%s/.weatherlog" % os.path.expanduser("~")

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

# Get the configuration.
try:
    # Load the configuration file.
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

# If there is missing configuration options, then add them.
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

# If the user doesn't want to restore the window size, set the size to the defaults.
if not config["restore"]:
    last_width = 900
    last_height = 500

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


class Weather(Gtk.Window):
    """Shows the main application."""
    def __init__(self):
        """Create the application."""
        
        # Create the window.
        Gtk.Window.__init__(self, title = "WeatherLog")
        # Set the window size.
        self.set_default_size(last_width, last_height)
        # Set the icon.
        self.set_icon_from_file("weatherlog_resources/images/icon.png")
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
            ("weather_menu", None, "_Weather"),
            ("add_new", Gtk.STOCK_ADD, "Add _New...", "<Control>n", "Add a new day to the list", self.add_new),
            ("edit", None, "_Edit...", "<Control>e", None, self.edit),
            ("remove", Gtk.STOCK_REMOVE, "Remo_ve...", "<Control>r", "Remove a day from the list", self.remove),
            ("import", Gtk.STOCK_OPEN, "_Import...", None, "Import data from a file", self.import_file),
            ("import_profile", None, "Import as New _Profile...", "<Control><Shift>o", None, self.import_new_profile),
            ("import_append", None, "Imp_ort and Merge...", "<Alt><Shift>o", None, self.import_append),
            ("export", Gtk.STOCK_SAVE, "_Export...", None, "Export data to a file", self.export_file)
        ])
        
        # Create the Weather -> Export to submenu.
        action_weather_export_group = Gtk.Action("export_menu", "E_xport to", None, None)
        action_group.add_action(action_weather_export_group)
        action_group.add_actions([
            ("export_html", None, "Export to _HTML...", "<Control><Alt>h", None, self.export_file_html),
            ("export_csv", None, "Export to _CSV...", "<Control><Alt>c", None, self.export_file_csv),
            ("export_pastebin", None, "Export to Paste_bin...", None, None, lambda x: self.export_pastebin("raw")),
            ("export_pastebin_html", None, "_Export to Pastebin (HTML)...", None, None, lambda x: self.export_pastebin("html")),
            ("export_pastebin_csv", None, "E_xport to Pastebin (CSV)...", None, None, lambda x: self.export_pastebin("csv")),
            ("clear_data", Gtk.STOCK_CLEAR, "Clear Current _Data...", "<Control>d", "Clear the data", self.clear),
            ("clear_all", None, "Clear _All Data...", "<Control><Alt>d", None, self.clear_all),
            ("reload_current", None, "Reload _Current Data...", "F5", None, self.reload_current),
            ("manual_save", None, "Man_ual Save...", "<Control>m", None, lambda x: self.save(show_dialog = True, automatic = False)),
            ("fullscreen", Gtk.STOCK_FULLSCREEN, "Toggle _Fullscreen", "F11", "Toggle fullscreen", self.toggle_fullscreen),
            ("exit", Gtk.STOCK_QUIT, "_Quit...", None, "Close the application", lambda x: self.exit("ignore", "this"))
        ])
        
        # Create the Info menu.
        action_group.add_actions([
            ("info_global_menu", None, "_Info"),
            ("info", Gtk.STOCK_INFO, "_Info...", "<Control>i", "Show info about the data", lambda x: self.show_info_generic(event = "ignore", info_type = "General", data = data))
        ])
        
        # Create the Info -> More Info submenu.
        action_weather_info_group = Gtk.Action("info_menu", "_More Info", None, None)
        action_group.add_action(action_weather_info_group)
        action_group.add_actions([
            ("temperature", None, "_Temperature...", "<Control>t", None, lambda x: self.show_info_generic(event = "ignore", info_type = "Temperature", data = data)),
            ("precipitation", None, "_Precipitation...", "<Control>p", None, lambda x: self.show_info_generic(event = "ignore", info_type = "Precipitation", data = data)),
            ("wind", None, "_Wind...", "<Control>w", None, lambda x: self.show_info_generic(event = "ignore", info_type = "Wind", data = data)),
            ("humidity", None, "_Humidity...", "<Control>h", None, lambda x: self.show_info_generic(event = "ignore", info_type = "Humidity", data = data)),
            ("air_pressure", None, "_Air Pressure...", "<Control>a", None, lambda x: self.show_info_generic(event = "ignore", info_type = "Air Pressure", data = data)),
            ("cloud_cover", None, "_Cloud Cover...", "<Control>c", None, lambda x: self.show_info_generic(event = "ignore", info_type = "Cloud Cover", data = data)),
            ("notes", None, "_Notes...", "<Control>e", None, lambda x: self.show_info_generic(event = "ignore", info_type = "Notes", data = data)),
            ("info_range", None, "Info in _Range...", "<Control><Shift>i", None, lambda x: self.info_range("General"))
        ])
        
        # Create the Info -> More Info in Range submenu.
        action_weather_info_range_group = Gtk.Action("info_range_menu", "More In_fo in Range", None, None)
        action_group.add_action(action_weather_info_range_group)
        action_group.add_actions([
            ("temperature_range", None, "_Temperature in Range...", "<Control><Shift>t", None, lambda x: self.info_range("Temperature")),
            ("precipitation_range", None, "_Precipitation in Range...", "<Control><Shift>p", None, lambda x: self.info_range("Precipitation")),
            ("wind_range", None, "_Wind in Range...", "<Control><Shift>w", None, lambda x: self.info_range("Wind")),
            ("humidity_range", None, "_Humidity in Range...", "<Control><Shift>h", None, lambda x: self.info_range("Humidity")),
            ("air_pressure_range", None, "_Air Pressure in Range...", "<Control><Shift>a", None, lambda x: self.info_range("Air Pressure")),
            ("cloud_cover_range", None, "_Cloud Cover in Range...", "<Control><Shift>c", None, lambda x: self.info_range("Cloud Cover")),
            ("notes_range", None, "_Notes in Range...", "<Control><Shift>e", None, lambda x: self.info_range("Notes")),
            ("info_selected", None, "Info for Se_lected Dates...", None, None, lambda x: self.info_selected("General"))
        ])
        
        # Create the Info -> More Info for Selected Dates submenu.
        action_weather_info_selected_group = Gtk.Action("info_selected_menu", "More Info for Selected _Dates", None, None)
        action_group.add_action(action_weather_info_selected_group)
        action_group.add_actions([
            ("temperature_selected", None, "_Temperature for Selected Dates...", None, None, lambda x: self.info_selected("Temperature")),
            ("precipitation_selected", None, "_Precipitation for Selected Dates...", None, None, lambda x: self.info_selected("Precipitation")),
            ("wind_selected", None, "_Wind for Selected Dates...", None, None, lambda x: self.info_selected("Wind")),
            ("humidity_selected", None, "_Humidity for Selected Dates...", None, None, lambda x: self.info_selected("Humidity")),
            ("air_pressure_selected", None, "_Air Pressure for Selected Dates...", None, None, lambda x: self.info_selected("Air Pressure")),
            ("cloud_cover_selected", None, "_Cloud Cover for Selected Dates...", None, None, lambda x: self.info_selected("Cloud Cover")),
            ("notes_selected", None, "_Notes for Selected Dates...", None, None, lambda x: self.info_selected("Notes"))
        ])
        
        # Create the Info -> Charts submenu.
        action_weather_charts_group = Gtk.Action("info_charts_menu", "Chart_s", None, None)
        action_group.add_action(action_weather_charts_group)
        action_group.add_actions([
            ("temperature_chart", None, "_Temperature Chart...", "<Alt><Shift>t", None, lambda x: self.show_chart_generic(event = "ignore", info_type = "Temperature", data = data)),
            ("precipitation_chart", None, "_Precipitation Chart...", "<Alt><Shift>p", None, lambda x: self.show_chart_generic(event = "ignore", info_type = "Precipitation", data = data)),
            ("wind_chart", None, "_Wind Chart...", "<Alt><Shift>w", None, lambda x: self.show_chart_generic(event = "ignore", info_type = "Wind", data = data)),
            ("humidity_chart", None, "_Humidity Chart...", "<Alt><Shift>h", None, lambda x: self.show_chart_generic(event = "ignore", info_type = "Humidity", data = data)),
            ("air_pressure_chart", None, "_Air Pressure Chart...", "<Alt><Shift>a", None, lambda x: self.show_chart_generic(event = "ignore", info_type = "Air Pressure", data = data)),
        ])
        
        # Create the Info -> Charts in Range submenu.
        action_weather_charts_range_group = Gtk.Action("info_charts_range_menu", "C_harts in Range", None, None)
        action_group.add_action(action_weather_charts_range_group)
        action_group.add_actions([
            ("temperature_range_chart", None, "_Temperature Chart in Range...", None, None, lambda x: self.chart_range("Temperature")),
            ("precipitation_range_chart", None, "_Precipitation Chart in Range...", None, None, lambda x: self.chart_range("Precipitation")),
            ("wind_range_chart", None, "_Wind Chart in Range...", None, None, lambda x: self.chart_range("Wind")),
            ("humidity_range_chart", None, "_Humidity Chart in Range...", None, None, lambda x: self.chart_range("Humidity")),
            ("air_pressure_range_chart", None, "_Air Pressure Chart in Range...", None, None, lambda x: self.chart_range("Air Pressure")),
        ])
        
        # Create the Info -> Charts for Selected Dates submenu.
        action_weather_charts_selected_group = Gtk.Action("info_charts_selected_menu", "Charts for Selec_ted Dates", None, None)
        action_group.add_action(action_weather_charts_selected_group)
        action_group.add_actions([
            ("temperature_selected_chart", None, "_Temperature for Selected Dates...", None, None, lambda x: self.chart_selected("Temperature")),
            ("precipitation_selected_chart", None, "_Precipitation for Selected Dates...", None, None, lambda x: self.chart_selected("Precipitation")),
            ("wind_selected_chart", None, "_Wind for Selected Dates...", None, None, lambda x: self.chart_selected("Wind")),
            ("humidity_selected_chart", None, "_Humidity for Selected Dates...", None, None, lambda x: self.chart_selected("Humidity")),
            ("air_pressure_selected_chart", None, "_Air Pressure for Selected Dates...", None, None, lambda x: self.chart_selected("Air Pressure"))
        ])
        
        # Create the Profiles menu.
        action_group.add_actions([
            ("profiles_menu", None, "_Profiles"),
            ("switch_profile", None, "_Switch Profile...", "<Control><Shift>s", None, self.switch_profile),
            ("add_profile", None, "_Add Profile...", "<Control><Shift>n", None, self.add_profile),
            ("remove_profile", None, "_Remove Profile...", "<Control><Shift>d", None, self.remove_profile),
            ("rename_profile", None, "Re_name Profile...", None, None, self.rename_profile),
            ("merge_profiles", None, "_Merge Profiles...", None, None, self.merge_profiles)
        ])
        
        # Create the Profiles -> Copy Data submenu.
        action_copy_group = Gtk.Action("copy_menu", "_Copy Data", None, None)
        action_group.add_action(action_copy_group)
        action_group.add_actions([
            ("copy_new", None, "To _New Profile...", None, None, lambda x: self.data_profile(mode = "Copy", method = "New")),
            ("copy_existing", None, "To _Existing Profile...", None, None, None)
        ])
        
        # Create the Profiles -> Move Data submenu.
        action_move_group = Gtk.Action("move_menu", "Mo_ve Data", None, None)
        action_group.add_action(action_move_group)
        action_group.add_actions([
            ("move_new", None, "To _New Profile...", None, None, lambda x: self.data_profile(mode = "Move", method = "New")),
            ("move_existing", None, "To _Existing Profile...", None, None, None)
        ])
        
        # Create the Options menu.
        action_group.add_actions([
            ("options_menu", None, "_Options"),
            ("options", None, "_Options...", "F2", None, self.options)
        ])
        
        # Create the Help menu.
        action_group.add_actions([
            ("help_menu", None, "_Help"),
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
        if config["show_dates"]:
            self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
        else:
            self.set_title("WeatherLog - %s" % last_profile)
        
        # Bind the events.
        self.connect("key-press-event", self.keypress)
        self.connect("delete-event", self.delete_event)
        
        # Change the titles, if needed.
        if not config["show_units"]:
            self.temp_col.set_title("Temperature")
            self.prec_col.set_title("Precipitation")
            self.wind_col.set_title("Wind")
            self.humi_col.set_title("Humidity")
            self.airp_col.set_title("Air Pressure")
        
        # Show the dialog telling the user the profile couldn't be found, if neccessary:
        if not profile_exists:
            
            # Show the dialog.
            show_alert_dialog(self, "WeatherLog", "The profile \"%s\" could not be found." % original_profile)
            
            # Save the profile name.
            self.save(show_dialog = False)
    
    
    def keypress(self, widget, event):
        """Handles keypresses."""
        
        # If the Escape key was pressed and the application is in fullscreen:
        if Gdk.keyval_name(event.keyval) == "Escape" and self.fullscreen_state:
            
            # Do whatever the user wants:
            # Ignore:
            if config["escape_fullscreen"].lower() == "ignore":
                return
            
            # Exit fullscreen:
            elif config["escape_fullscreen"].lower() == "exit fullscreen":
                self.toggle_fullscreen("ignore")
            
            # Close:
            elif config["escape_fullscreen"].lower() == "close":
                self.exit("ignore", "this")
        
        # If the Escape key was pressed and the application isn't in fullscreen:
        elif Gdk.keyval_name(event.keyval) == "Escape" and not self.fullscreen_state:
            
            # Do whatever the user wants:
            # Ignore:
            if config["escape_windowed"].lower() == "ignore":
                return
            
            # Minimize:
            elif config["escape_windowed"].lower() == "minimize":
                self.iconify()
            
            # Close:
            elif config["escape_windowed"].lower() == "close":
                self.exit("ignore", "this")
    
    
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
        new_dlg = AddNewDialog(self, last_profile, config["location"], config["pre-fill"], config["show_pre-fill"], units)
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
            note = new_dlg.note_ent.get_text().strip()
            
            # If the precipitation or wind are zero, set the appropriate type/direction to "None".
            if not prec:
                prec_type = "None"
            if not wind:
                wind_dir = "None"
            
            # If the date is already used, show the dialog.
            if date in utility_functions.get_column(data, 0):
                
                # Show the error dialog.
                show_error_dialog(new_dlg, "Add New", "The date %s has already been entered." % date)
                
                # Close the error dialog and the "Add New" dialog. The second one
                # is needed because of a bug where the window will stop responding
                # to events, making it useless. Fix later!
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
        if config["show_dates"]:
            self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
        else:
            self.set_title("WeatherLog - %s" % last_profile)
        
        # Close the dialog.
        new_dlg.destroy() 
        
        # Save the data.
        self.save(show_dialog = False)
    
    
    def edit(self, event):
        """Edits a row of data."""
        
        # Get the selected date.
        try:
            tree_sel = self.treeview.get_selection()
            tm, ti = tree_sel.get_selected()
            date = tm.get_value(ti, 0)
        
        except:
            # If nothing was selected, show a dialog and don't continue.
            
            # Tell the user there is nothing selected.
            show_error_dialog(self, "Edit - %s" % last_profile, "No date selected.")
            
            return
        
        # Get the index of the date.
        index = utility_functions.get_column(data, 0).index(date)
        
        # Show the dialog.
        edit_dlg = EditDialog(self, last_profile, data[index], date, units)
        # Get the response.
        response = edit_dlg.run()
        
        
        # If the user clicked the OK button, add the data.
        if response == Gtk.ResponseType.OK:
            
            # Get the data from the entries and comboboxes.
            temp = edit_dlg.temp_sbtn.get_value()
            prec = edit_dlg.prec_sbtn.get_value()
            prec_type = edit_dlg.prec_com.get_active_text()
            wind = edit_dlg.wind_sbtn.get_value()
            wind_dir = edit_dlg.wind_com.get_active_text()
            humi = edit_dlg.humi_sbtn.get_value()
            airp = edit_dlg.airp_sbtn.get_value()
            airp_read = edit_dlg.airp_com.get_active_text()
            clou = edit_dlg.clou_com.get_active_text()
            note = edit_dlg.note_ent.get_text().strip()
            
            # If the precipitation or wind are zero, set the appropriate type/direction to "None".
            if not prec:
                prec_type = "None"
            if not wind:
                wind_dir = "None"
            
            # Create the edited list of data.
            new_data = [date, ("%.2f" % temp), "%s%s" % ((("%.2f" % prec) + " " if prec_type != "None" else ""), prec_type), "%s%s" % ((("%.2f" % wind) + " " if wind_dir != "None" else ""), wind_dir), ("%.2f" % humi), ("%.2f %s" % (airp, airp_read)), clou, note]
            
            # Store the edited data.
            data[index] = new_data
            
            # Update the ListStore.
            self.liststore.clear()
            for i in data:
                self.liststore.append(i)
        
        # Close the dialog.
        edit_dlg.destroy()
    
    
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
            show_error_dialog(self, "Remove - %s" % last_profile, "No date selected.")
            
            return
        
        # Only show the dialog if the user wants that.
        if config["confirm_del"]:
            
            # Confirm that the user wants to delete the row.
            response = show_question_dialog(self, "Confirm Remove - %s" % last_profile, "Are you sure you want to delete the data for %s?\n\nThis action cannot be undone." % date)
            
            # If the user doesn't want to overwrite, cancel the action.
            if response != Gtk.ResponseType.OK:
                return
        
        # Get the index of the date.
        index = utility_functions.get_column(data, 0).index(date)
        
        # Delete the index in the list.
        del data[index]
        
        # Refresh the ListStore.
        self.liststore.clear()
        for i in data:
            self.liststore.append(i)
        
        # Update the title.
        if config["show_dates"]:
            self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
        else:
            self.set_title("WeatherLog - %s" % last_profile)
            
        # Save the data.
        self.save(show_dialog = False)
        
    
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
                show_error_dialog(self, "%s Info in Range - %s" % (info, last_profile), "%s is not a valid date." % date1)
                
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
            
            # Convert the dates to ISO notation for comparison.
            nDate1 = str(year1) + "-" + (str(month1) if month1 > 9 else "0" + str(month1)) + "-" + (str(day1) if day1 > 9 else "0" + str(day1))
            nDate2 = str(year2) + "-" + (str(month2) if month2 > 9 else "0" + str(month2)) + "-" + (str(day2) if day2 > 9 else "0" + str(day2))
            
            # Check to make sure this date is valid, and cancel the action if not.
            if date2 not in utility_functions.get_column(data, 0):
                
                # Show the dialog.
                show_error_dialog(self, "%s Info in Range - %s" % (info, last_profile), "%s is not a valid date." % date2)
                
                # Close the dialog.
                end_dlg.destroy()
                
                return
            
            # Check to make sure this date is not the same as or earlier than the starting date,
            # and canel the action if it is.
            elif date1 == date2 or nDate1 > nDate2:
                
                # Show the dialog.
                show_error_dialog(self, "%s Info in Range - %s" % (info, last_profile), "The ending date must not be before or the same as the starting date.")
                
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
        self.show_info_generic(event = "ignore", info_type = info, data = data2)
    
    
    def info_selected(self, info = "General"):
        """Gets the selected dates to for the info to display."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "%s Info - %s" % (info, last_profile))
            return
        
        # Get the dates.
        dates = []
        for i in data:
            dates.append([i[0]])
        
        # Show the dialog and get the response.
        info_dlg = InfoSelectedDialog(self, info, last_profile, dates)
        response = info_dlg.run()
        
        # If the user clicked OK:
        if response == Gtk.ResponseType.OK:
            
            # Get the selected items.
            model, treeiter = info_dlg.treeview.get_selection().get_selected_rows()
            
            # If nothing was selected, don't continue.
            if treeiter == None:
                
                # Close the dialog.
                info_dlg.destroy()
                
                return
            
            # Get the dates.
            ndates = []
            for i in treeiter:
                ndates.append(model[i][0])
            
            # Get the data.
            ndata = []
            for i in range(0, len(data)):
                if data[i][0] in ndates:
                    ndata.append(data[i])
            
            # If there is no data, don't continue.
            if len(ndata) == 0:
                
                # Close the dialog.
                info_dlg.destroy()
                
                return
        
        # Otherwise, cancel the action.
        else:
            
            # Close the dialog.
            info_dlg.destroy()
            
            return
        
        # Close the dialog.
        info_dlg.destroy()
        
        # Pass the data to the appropriate function.
        self.show_info_generic(event = "ignore", info_type = info, data = ndata)
    
    
    def show_info_generic(self, event, info_type = "General", data = data):
        """Shows info about the data."""
        
        # If there is no data, tell the user and don't show the dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "%s Info - %s" % (info_type, last_profile))
            return
        
        # Get the info.
        if info_type == "General":
            data2 = info.general_info(data, units)
        elif info_type == "Temperature":
            data2 = info.temp_info(data, units)
        elif info_type == "Precipitation":
            data2 = info.prec_info(data, units)
        elif info_type == "Wind":
            data2 = info.wind_info(data, units)
        elif info_type == "Humidity":
            data2 = info.humi_info(data, units)
        elif info_type == "Air Pressure":
            data2 = info.airp_info(data, units)
        elif info_type == "Cloud Cover":
            data2 = info.clou_info(data, units)
        elif info_type == "Notes":
            data2 = info.note_info(data, units)
        
        # Show the dialog and get the response.
        info_dlg = GenericInfoDialog(self, "%s Info - %s" % (info_type, last_profile), data2)
        response = info_dlg.run()
        
        # If the user clicked Export:
        if response == 9:
            
            # Create the dialog.
            export_dlg = Gtk.FileChooserDialog("Export %s Info - %s" % (info_type, last_profile), self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
            export_dlg.set_do_overwrite_confirmation(True)
            
            # Get the response.
            response2 = export_dlg.run()
            if response2 == Gtk.ResponseType.OK:
                
                # Get the filename.
                filename = export_dlg.get_filename()
                
                # Export the info.
                export_info.export_info(data2, filename)
                
            # Close the dialog.
            export_dlg.destroy()
        
        # Close the dialog. The response can be ignored.
        info_dlg.destroy()
        
    
    def chart_range(self, info):
        """Gets the range for the chart to display."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "%s Chart - %s" % (info, last_profile))
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
        start_dlg = ChartRangeDialog(self, last_profile, info, "starting", days, months, years)
        
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
                show_error_dialog(self, "%s Chart in Range - %s" % (info, last_profile), "%s is not a valid date." % date1)
                
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
        end_dlg = ChartRangeDialog(self, last_profile, info, "ending", daye, monthe, yeare)
        
        # Get the response.
        response2 = end_dlg.run()
        
        # If the user clicked OK:
        if response2 == Gtk.ResponseType.OK:
            
            # Get the date.
            year2, month2, day2 = end_dlg.info_cal.get_date()
            date2 = "%d/%d/%d" % (day2, month2 + 1, year2)
            
            # Convert the dates to ISO notation for comparison.
            nDate1 = str(year1) + "-" + (str(month1) if month1 > 9 else "0" + str(month1)) + "-" + (str(day1) if day1 > 9 else "0" + str(day1))
            nDate2 = str(year2) + "-" + (str(month2) if month2 > 9 else "0" + str(month2)) + "-" + (str(day2) if day2 > 9 else "0" + str(day2))
            
            # Check to make sure this date is valid, and cancel the action if not.
            if date2 not in utility_functions.get_column(data, 0):
                
                # Show the dialog.
                show_error_dialog(self, "%s Chart in Range - %s" % (info, last_profile), "%s is not a valid date." % date2)
                
                # Close the dialog.
                end_dlg.destroy()
                
                return
            
            # Check to make sure this date is not the same as or earlier than the starting date,
            # and canel the action if it is.
            elif date1 == date2 or nDate1 > nDate2:
                
                # Show the dialog.
                show_error_dialog(self, "%s Chart in Range - %s" % (info, last_profile), "The ending date must not be before or the same as the starting date.")
                
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
        self.show_chart_generic(event = "ignore", info_type = info, data = data2)
    
    
    def chart_selected(self, info = "General"):
        """Gets the selected dates to for the charts to display."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "%s Chart - %s" % (info, last_profile))
            return
        
        # Get the dates.
        dates = []
        for i in data:
            dates.append([i[0]])
        
        # Show the dialog and get the response.
        info_dlg = ChartSelectedDialog(self, info, last_profile, dates)
        response = info_dlg.run()
        
        # If the user clicked OK:
        if response == Gtk.ResponseType.OK:
            
            # Get the selected items.
            model, treeiter = info_dlg.treeview.get_selection().get_selected_rows()
            
            # If nothing was selected, don't continue.
            if treeiter == None:
                
                # Close the dialog.
                info_dlg.destroy()
                
                return
            
            # Get the dates.
            ndates = []
            for i in treeiter:
                ndates.append(model[i][0])
            
            # Get the data.
            ndata = []
            for i in range(0, len(data)):
                if data[i][0] in ndates:
                    ndata.append(data[i])
            
            # If there is no data, don't continue.
            if len(ndata) == 0:
                
                # Close the dialog.
                info_dlg.destroy()
                
                return
        
        # Otherwise, cancel the action.
        else:
            
            # Close the dialog.
            info_dlg.destroy()
            
            return
        
        # Close the dialog.
        info_dlg.destroy()
        
        # Pass the data to the appropriate function.
        self.show_chart_generic(event = "ignore", info_type = info, data = ndata)
    
    
    def show_chart_generic(self, event, info_type, data = data):
        """Shows a chart about the data."""
        
        # If there is no data, tell the user and don't show the chart dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "%s Chart - %s" % (info_type, last_profile))
            return
        
        # Get the chart data
        if info_type == "Temperature":
            data2 = charts.temp_chart(data, units)
        elif info_type == "Precipitation":
            data2 = charts.prec_chart(data, units)
        elif info_type == "Wind":
            data2 = charts.wind_chart(data, units)
        elif info_type == "Humidity":
            data2 = charts.humi_chart(data, units)
        elif info_type == "Air Pressure":
            data2 = charts.airp_chart(data, units)
        
        # Show the dialog and get the response.
        chart_dlg = GenericChartDialog(self, "%s Chart - %s" % (info_type, last_profile), data2)
        response = chart_dlg.run()
        
        # If the user clicked Export:
        if response == 9:
            
            # Create the dialog.
            export_dlg = Gtk.FileChooserDialog("Export %s Chart - %s" % (info_type, last_profile), self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
            export_dlg.set_do_overwrite_confirmation(True)
            
            # Get the response.
            response2 = export_dlg.run()
            if response2 == Gtk.ResponseType.OK:
                
                # Get the filename.
                filename = export_dlg.get_filename()
                
                # Export the info.
                export_info.export_chart(data2, filename)
                
            # Close the dialog.
            export_dlg.destroy()
        
        # Close the dialog. The response can be ignored.
        chart_dlg.destroy()
    
    
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
            response = show_question_dialog(self, "Confirm Import - %s" % last_profile, "Are you sure you want to import the data?\n\nCurrent data will be overwritten.")
            
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
                if config["show_dates"]:
                    self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
                else:
                    self.set_title("WeatherLog - %s" % last_profile)
                    
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
                show_error_dialog(new_dlg, "Add Profile", "The profile name \"%s\" is not valid.\n\n1. Profile names may not be blank.\n2. Profile names may not be all spaces.\n3. Profile names may only be letters, numbers, and spaces.\n4. Profile names may not start with a period (\".\")." % name)
                
                # Close the dialog.
                new_dlg.destroy()
                
                return
            
            # If the profile name is already in use, show a dialog and cancel the action.
            elif os.path.isdir("%s/profiles/%s" % (main_dir, name)):
                
                # Create the error dialog.
                show_error_dialog(new_dlg, "Add Profile", "The profile name \"%s\" is already in use." % name)
                
                # Close the dialog.
                new_dlg.destroy()
                
                return
            
            # Otherwise if there are no problems with the name, add the profile.
            else:
                
                # Create the directory and file.
                last_profile = name
                os.makedirs("%s/profiles/%s" % (main_dir, name))
                open("%s/profiles/%s/weather.json" % (main_dir, name), "w").close()
                
                # Clear the old data.
                data[:] = []
                self.liststore.clear()
                
                # Set the new title.
                if config["show_dates"]:
                    self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
                else:
                    self.set_title("WeatherLog - %s" % last_profile)
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
            
            # Tell the user there is no data to export.
            show_alert_dialog(self, "Export - %s" % last_profile, "There is no data to export.")
            
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
            
            # Tell the user there is no data to export.
            show_alert_dialog(self, "Export to HTML - %s" % last_profile, "There is no data to export.")
            
            return
        
        # Create the dialog.
        export_html_dlg = Gtk.FileChooserDialog("Export to HTML - %s" % last_profile, self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        export_html_dlg.set_do_overwrite_confirmation(True)
        
        # Get the response.
        response = export_html_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Convert to data to HTML.
            html = export.html(data, units)
            
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
            
            # Tell the user there is no data to export.
            show_alert_dialog(self, "Export to CSV - %s" % last_profile, "There is no data to export.")
            
            return
        
        # Create the dialog.
        export_csv_dlg = Gtk.FileChooserDialog("Export to CSV - %s" % last_profile, self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        export_csv_dlg.set_do_overwrite_confirmation(True)
        
        # Get the response.
        response = export_csv_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Convert the data to CSV.
            csv = export.csv(data, units)
            
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
            show_alert_dialog(self, "Export to Pastebin - %s" % last_profile, "There is no data to export.")
            
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
            show_alert_dialog(self, "Export to Pastebin - %s" % last_profile, "The data has been uploaded to Pastebin, and can be accessed at the following URL:\n\n%s" % result)
        
        else:
            
            # Tell the user there was an error
            show_error_dialog(self, "Export to Pastebin - %s" % last_profile, "The data could not be uploaded to Pastebin.")
    
    
    def clear(self, event):
        """Clears the data."""
        
        global data
        
        # Only show the dialog if the user wants that.
        if config["confirm_del"]:
            
            # Confirm that the user wants to clear the data.
            response = show_question_dialog(self, "Confirm Clear Current Data - %s" % last_profile, "Are you sure you want to clear the data?\n\nThis action cannot be undone.")
            
            # If the user confirms the clear:
            if response == Gtk.ResponseType.OK:
                
                # Clear the data.
                data[:] = []
                
                # Clear the ListStore.
                self.liststore.clear()
        
        else:
            
            # Clear the data.
            data[:] = []
            
            # Clear the ListStore.
            self.liststore.clear()
        
        # Update the title.
        if config["show_dates"]:
            self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
        else:
            self.set_title("WeatherLog - %s" % last_profile)
        
        # Save the data.
        self.save(show_dialog = False)
        
    
    def clear_all(self, event):
        """Clears all data."""
        
        global last_profile
        global config
        global units
        
        # Only show the dialog if the user wants that.
        clear = True
        if config["confirm_del"]:
            
            # Confirm that the user wants to clear the data.
            response = show_question_dialog(self, "Confirm Clear All Data", "Are you sure you want to clear all the data?\n\nThis action cannot be undone.")
            
            # If the user cancels the clear:
            if response != Gtk.ResponseType.OK:
                clear = False
        
        # If the user wants to continue:
        if clear:
            
            # Clear the old data.
            data[:] = []
            self.liststore.clear()
            
            # Delete all the files.
            shutil.rmtree(main_dir)
            
            # Create the directory.
            os.makedirs(main_dir)
            
            # Set the profile name.
            last_profile = "Main Profile"
            
            # Create the last profile file.
            last_prof = open("%s/lastprofile" % main_dir, "w")
            last_prof.write("Main Profile")
            last_prof.close()
            
            # Create the Main Profile directory and data file.
            os.makedirs("%s/profiles/Main Profile" % main_dir)
            last_prof_data = open("%s/profiles/Main Profile/weather.json" % main_dir, "w")
            last_prof_data.write("[]")
            last_prof_data.close()
            
            # Set the default config.
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
            
            # Add/remove the units, if desired:
            if not config["show_units"]:
                self.temp_col.set_title("Temperature")
                self.prec_col.set_title("Precipitation")
                self.wind_col.set_title("Wind")
                self.humi_col.set_title("Humidity")
                self.airp_col.set_title("Air Pressure")
            else:
                self.temp_col.set_title("Temperature (%s)" % units["temp"])
                self.prec_col.set_title("Precipitation (%s)" % units["prec"])
                self.wind_col.set_title("Wind (%s)" % units["wind"])
                self.humi_col.set_title("Humidity (%)")
                self.airp_col.set_title("Air Pressure (%s)" % units["airp"])
            
            # Set the new title.
            if config["show_dates"]:
                self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
            else:
                self.set_title("WeatherLog - %s" % last_profile)
            
            # Save the data.
            self.save(show_dialog = False, from_options = True)
    
    
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
        
        # Get the last modified dates.
        for i in range(0, len(profiles)):
            
            # Get the date and format it properly.
            last_modified = os.path.getmtime("%s/profiles/%s/weather.json" % (main_dir, last_profile))
            last_modified = time.strftime("%d/%m/%Y", time.localtime(last_modified))
            
            # Change the value in the list.
            profiles[i] = [profiles[i], last_modified]
        
        # Switch back to the previous directory.
        os.chdir(current_dir)
        
        # If there are no other profiles, tell the user and cancel the action.
        if len(profiles) == 0:
            
            # Tell the user there are no other profiles.
            show_alert_dialog(self, "Switch Profile", "There are no other profiles.")
            
            return
        
        # Show the dialog.
        swi_dlg = SwitchProfileDialog(self, profiles)
        # Get the response.
        response = swi_dlg.run()
        
        # If the OK button was pressed:
        if response == Gtk.ResponseType.OK:
            
            # Get the selected item.
            model, treeiter = swi_dlg.treeview.get_selection().get_selected()
            
            # If nothing was selected, don't continue.
            if treeiter == None:
                
                # Close the dialog.
                swi_dlg.destroy()
                
                return
            
            # Get the profile name.
            name = model[treeiter][0]
            
            # Clear the old data.
            data[:] = []
            self.liststore.clear()
            
            # Load the data.   
            try:
                
                # This should be ~/.weatherlog/[profile name]/weather.json on Linux.
                data_file = open("%s/profiles/%s/weather.json" % (main_dir, name), "r")
                data = json.load(data_file)
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
            
            # Switch to the new profile.
            last_profile = name
            for i in data:
                self.liststore.append(i)
            
            # Set the new title.
            if config["show_dates"]:
                self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
            else:
                self.set_title("WeatherLog - %s" % last_profile)
            
            # Save the data.
            self.save(show_dialog = False)
            
                
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
            
            # Validate the name. If it contains a non-alphanumeric character, starts with a period, or is just space,
            # show a dialog and cancel the action.
            if re.compile("[^a-zA-Z1-90 \.\-\+\(\)\?\!]").match(name) or not name or name.lstrip().rstrip() == "" or name.startswith("."):
                
                # Create the error dialog.
                show_error_dialog(new_dlg, "Add Profile", "The profile name \"%s\" is not valid.\n\n1. Profile names may not be blank.\n2. Profile names may not be all spaces.\n3. Profile names may only be letters, numbers, and spaces.\n4. Profile names may not start with a period (\".\")." % name)
            
            # If the profile name is already in use, show a dialog and cancel the action.
            elif os.path.isdir("%s/profiles/%s" % (main_dir, name)):
                
                # Create the error dialog.
                show_error_dialog(new_dlg, "Add Profile", "The profile name \"%s\" is already in use." % name)
            
            # Otherwise if there are no problems with the name, add the profile.
            else:
                
                # Strip leading and trailing whitespace.
                name = name.lstrip().rstrip()
                
                # Create the directory and file.
                last_profile = name
                os.makedirs("%s/profiles/%s" % (main_dir, name))
                new_prof_file = open("%s/profiles/%s/weather.json" % (main_dir, name), "w")
                new_prof_file.write("[]")
                new_prof_file.close()
                
                # Clear the old data.
                data[:] = []
                self.liststore.clear()
                
                # Set the new title.
                if config["show_dates"]:
                    self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
                else:
                    self.set_title("WeatherLog - %s" % last_profile)
                    
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
        
        # Get the last modified dates.
        for i in range(0, len(profiles)):
            
            # Get the date and format it properly.
            last_modified = os.path.getmtime("%s/profiles/%s/weather.json" % (main_dir, last_profile))
            last_modified = time.strftime("%d/%m/%Y", time.localtime(last_modified))
            
            # Change the value in the list.
            profiles[i] = [profiles[i], last_modified]
        
        # Switch back to the previous directory.
        os.chdir(current_dir)
        
        # If there are no other profiles, tell the user and cancel the action.
        if len(profiles) == 0:
            
            # Tell the user there are no other profiles.
            show_alert_dialog(self, "Remove Profile", "There are no other profiles.")
            
            return
        
        # Show the dialog.
        rem_dlg = RemoveProfileDialog(self, profiles)
        # Get the response.
        response = rem_dlg.run()
        
        # If the OK button was pressed:
        if response == Gtk.ResponseType.OK:
            
            # Get the selected items.
            model, treeiter = rem_dlg.treeview.get_selection().get_selected_rows()
            
            # If nothing was selected, don't continue.
            if treeiter == None:
                
                # Close the dialog.
                rem_dlg.destroy()
                
                return
            
            # Get the profiles.
            profiles = []
            for i in treeiter:
                profiles.append(model[i][0])
            
            # If nothing was selected, don't continue.
            # TODO: check if this block is really necessary.
            if len(profiles) == 0:
                
                # Close the dialog.
                rem_dlg.destroy()
                
                return
            
            # Only show the dialog if the user wants that.
            if config["confirm_del"]:
                
                # Confirm that the user wants to delete the profile.
                response = show_question_dialog(rem_dlg, "Confirm Remove Profile", "Are you sure you want to remove the profile%s?\n\nThis action cannot be undone." % ("" if len(profiles) == 1 else "s"))
                
                # If the user wants to continue:
                if response == Gtk.ResponseType.OK:
                    
                    # Loop through the profiles and delete them all:
                    for name in profiles:
                        
                        # Delete the directory.
                        shutil.rmtree("%s/profiles/%s" % (main_dir, name))
            
            else:
                
                # Loop through the profiles and delete them all:
                for name in profiles:
                    
                    # Delete the directory.
                    shutil.rmtree("%s/profiles/%s" % (main_dir, name))
        
        
        # Close the dialog.
        rem_dlg.destroy()
    
    
    def rename_profile(self, event):
        """Renames the current profile."""
        
        global last_profile
        global data
        
        # Show the dialog.
        ren_dlg = RenameProfileDialog(self)
        
        # Get the response.
        response = ren_dlg.run()
        name = ren_dlg.ren_ent.get_text()
        
        # If the OK button was pressed:
        if response == Gtk.ResponseType.OK:
            
            # Validate the name. If it contains a non-alphanumeric character, starts with a period, or is just space,
            # show a dialog and cancel the action.
            if re.compile("[^a-zA-Z1-90 \.\-\+\(\)\?\!]").match(name) or not name or name.lstrip().rstrip() == "" or name.startswith("."):
                
                # Create the error dialog.
                show_error_dialog(ren_dlg, "Rename Profile", "The profile name \"%s\" is not valid.\n\n1. Profile names may not be blank.\n2. Profile names may not be all spaces.\n3. Profile names may only be letters, numbers, and spaces.\n4. Profile names may not start with a period (\".\")." % name)
            
            # If the profile name is already in use, show a dialog and cancel the action.
            elif os.path.isdir("%s/profiles/%s" % (main_dir, name)):
                
                # Create the error dialog.
                show_error_dialog(ren_dlg, "Rename Profile", "The profile name \"%s\" is already in use." % name)
            
            # Otherwise if there are no problems with the name, add the profile.
            else:
                
                # Strip leading and trailing whitespace.
                name = name.lstrip().rstrip()
            
                # Rename the directory.
                os.rename("%s/profiles/%s" % (main_dir, last_profile), "%s/profiles/%s" % (main_dir, name))
                
                # Clear the old data.
                data[:] = []
                self.liststore.clear()
                
                # Load the data.   
                try:
                    
                    # This should be ~/.weatherlog/[profile name]/weather.json on Linux.
                    data_file = open("%s/profiles/%s/weather.json" % (main_dir, name), "r")
                    data = json.load(data_file)
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
                
                # Switch to the new profile.
                last_profile = name
                for i in data:
                    self.liststore.append(i)
                
                # Set the new title.
                if config["show_dates"]:
                    self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
                else:
                    self.set_title("WeatherLog - %s" % last_profile)
    
        # Close the dialog.
        ren_dlg.destroy()
    
    
    def merge_profiles(self, event):
        """Merges two profiles."""
        
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
        
        # Get the last modified dates.
        for i in range(0, len(profiles)):
            
            # Get the date and format it properly.
            last_modified = os.path.getmtime("%s/profiles/%s/weather.json" % (main_dir, last_profile))
            last_modified = time.strftime("%d/%m/%Y", time.localtime(last_modified))
            
            # Change the value in the list.
            profiles[i] = [profiles[i], last_modified]
        
        # Switch back to the previous directory.
        os.chdir(current_dir)
        
        # If there are no other profiles, tell the user and cancel the action.
        if len(profiles) == 0:
            
            # Tell the user there are no other profiles.
            show_alert_dialog(self, "Merge Profiles", "There are no other profiles.")
            
            return
        
        # Show the dialog.
        mer_dlg = MergeProfilesDialog(self, profiles)
        # Get the response.
        response = mer_dlg.run()
        
        # If the OK button was pressed:
        if response == Gtk.ResponseType.OK:
            
            # Get the selected item.
            model, treeiter = mer_dlg.treeview.get_selection().get_selected()
            
            # If nothing was selected, don't continue.
            if treeiter == None:
                
                # Close the dialog.
                mer_dlg.destroy()
                
                return
            
            # Get the profile name.
            name = model[treeiter][0]
            
            # Read the data.   
            try:
                
                # This should be ~/.weatherlog/[profile name]/weather.json on Linux.
                data_file = open("%s/profiles/%s/weather.json" % (main_dir, name), "r")
                data2 = json.load(data_file)
                data_file.close()
                
            except IOError:
                # Show the error message, and close the application.
                # This one shows if there was a problem reading the file.
                print("Error importing data (IOError).")
                data2 = []
            
            except (TypeError, ValueError):
                # Show the error message, and close the application.
                # This one shows if there was a problem with the data type.
                print("Error importing data (TypeError or ValueError).")
                data2 = []
            
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
                if config["show_dates"]:
                    self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
                else:
                    self.set_title("WeatherLog - %s" % last_profile)
                
                # Delete the directory.
                shutil.rmtree("%s/profiles/%s" % (main_dir, name))
        
        # Close the dialog.
        mer_dlg.destroy()
    
    
    def data_profile(self, mode = "Copy", method = "New"):
        """Copies or moves data to a new or an existing profile."""
        
        global data
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "%s Data to %s Profile" % (mode, method))
            return
        
        # Get the dates.
        dates = []
        dates2 = []
        for i in data:
            dates.append([i[0]])
            dates2.append(i[0])
        
        # If the user wants to copy/move the data to a new profile:
        if method == "New":
            
            # Show the dialog.
            new_dlg = ProfileDataNewDialog(self, mode)
            
            # Get the response.
            response = new_dlg.run()
            name = new_dlg.pro_ent.get_text()
            
            # If the user pressed OK:
            if response == Gtk.ResponseType.OK:
                
                # Validate the name. If it contains a non-alphanumeric character, starts with a period, or is just space,
                # show a dialog and cancel the action.
                if re.compile("[^a-zA-Z1-90 \.\-\+\(\)\?\!]").match(name) or not name or name.lstrip().rstrip() == "" or name.startswith("."):
                    
                    # Create the error dialog.
                    show_error_dialog(new_dlg, "%s Data to %s Profile" % (mode, method), "The profile name \"%s\" is not valid.\n\n1. Profile names may not be blank.\n2. Profile names may not be all spaces.\n3. Profile names may only be letters, numbers, and spaces.\n4. Profile names may not start with a period (\".\")." % name)
                    
                    # Close the dialog.
                    new_dlg.destroy()
                    
                # If the profile name is already in use, show a dialog and cancel the action.
                elif os.path.isdir("%s/profiles/%s" % (main_dir, name)):
                    
                    # Create the error dialog.
                    show_error_dialog(new_dlg, "%s Data to %s Profile" % (mode, method), "The profile name \"%s\" is already in use." % name)
                    
                    # Close the dialog.
                    new_dlg.destroy()
                    
                # Strip leading and trailing whitespace.
                name = name.lstrip().rstrip()
                
                # Create the directory and file.
                os.makedirs("%s/profiles/%s" % (main_dir, name))
                new_prof_file = open("%s/profiles/%s/weather.json" % (main_dir, name), "w")
                new_prof_file.write("[]")
                new_prof_file.close()
                
                # Close the dialog.
                new_dlg.destroy()
                
            else:
                
                # Otherwise, don't continue.
                new_dlg.destroy()
                return
            
            # Show the dialog to get the dates.
            date_dlg = ProfileDateSelectionDialog(self, mode, method, dates)
            
            # Get the response.
            response = date_dlg.run()
            
            # If the user clicked OK:
            if response == Gtk.ResponseType.OK:
                
                # Get the selected items.
                model, treeiter = date_dlg.treeview.get_selection().get_selected_rows()
                
                # If nothing was selected, don't continue.
                if treeiter == None:
                    
                    # Close the dialog.
                    date_dlg.destroy()
                    
                    return
                
                # Get the dates.
                ndates = []
                for i in treeiter:
                    ndates.append(model[i][0])
                
                # Get the data.
                ndata = []
                for i in range(0, len(data)):
                    if data[i][0] in ndates:
                        ndata.append(data[i])
                
                # If there is no data, don't continue.
                if len(ndata) == 0:
                    
                    # Close the dialog.
                    date_dlg.destroy()
                
                    return
                
            else:
                
                # Otherwise, don't continue.
                date_dlg.destroy()
                return
            
            # If the user wants to move the data, delete the items in the current profile.
            if mode == "Move":
                
                data = [x for x in data if x[0] not in ndates]
            
            # Reset the list.
            self.liststore.clear()
            for i in data:
                self.liststore.append(i)
            
            # Set the new title.
            if config["show_dates"]:
                self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
            else:
                self.set_title("WeatherLog - %s" % last_profile)
            
            # Put the data in the new profile.
            try:
                # This should save to ~/.weatherlog/[profile name]/weather.json on Linux.
                data_file = open("%s/profiles/%s/weather.json" % (main_dir, name), "w")
                json.dump(ndata, data_file)
                data_file.close()
                
            except IOError:
                # Show the error message if something happened, but continue.
                # This one is shown if there was an error writing to the file.
                print("Error saving data file (IOError).")
            
            except (TypeError, ValueError):
                # Show the error message if something happened, but continue.
                # This one is shown if there was an error with the data type.
                print("Error saving data file (TypeError or ValueError).")
            
            # Close the dialog.
            date_dlg.destroy()
                
        else:
            pass
            ## TODO: The entire thing with copying/moving to an existing profile.
    
    
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
        global config
        current_units = config["units"]
        
        # Create the dialog.
        opt_dlg = OptionsDialog(self, config)
        
        # Get the response.
        response = opt_dlg.run()
        
        # If the user pressed OK:
        if response == Gtk.ResponseType.OK:
            
            # Get the values.
            prefill = opt_dlg.pre_chk.get_active()
            restore = opt_dlg.win_chk.get_active()
            location = opt_dlg.loc_ent.get_text()
            units_ = opt_dlg.unit_com.get_active_text().lower()
            esc_win = opt_dlg.escw_com.get_active_text().lower()
            esc_ful = opt_dlg.escf_com.get_active_text().lower()
            show_dates = opt_dlg.date_chk.get_active()
            show_units = opt_dlg.unit_chk.get_active()
            auto_save = opt_dlg.sav_chk.get_active()
            confirm_del = opt_dlg.del_chk.get_active()
            show_prefill = opt_dlg.pdl_chk.get_active()
            confirm_exit = opt_dlg.cex_chk.get_active()
            
            # Set the configuration.
            config["pre-fill"] = prefill
            config["restore" ] = restore
            config["location"] = location
            config["units"] = units_
            config["escape_windowed"] = esc_win
            config["escape_fullscreen"] = esc_ful
            config["show_dates"] = show_dates
            config["show_units"] = show_units
            config["auto_save"] = auto_save
            config["confirm_del"] = confirm_del
            config["show_pre-fill"] = show_prefill
            config["confirm_exit"] = confirm_exit
            
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
                response = show_question_dialog(opt_dlg, "Options", "The units have changed from %s to %s.\n\nWould you like to convert the data to the new units?" % (current_units, config["units"]))
                
                # If the user wants to convert the data:
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
            
            # Add/remove the units, if desired:
            if not config["show_units"]:
                self.temp_col.set_title("Temperature")
                self.prec_col.set_title("Precipitation")
                self.wind_col.set_title("Wind")
                self.humi_col.set_title("Humidity")
                self.airp_col.set_title("Air Pressure")
            else:
                self.temp_col.set_title("Temperature (%s)" % units["temp"])
                self.prec_col.set_title("Precipitation (%s)" % units["prec"])
                self.wind_col.set_title("Wind (%s)" % units["wind"])
                self.humi_col.set_title("Humidity (%)")
                self.airp_col.set_title("Air Pressure (%s)" % units["airp"])
            
            # Set the title, if desired:
            if config["show_dates"]:
                self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
            else:
                self.set_title("WeatherLog - %s" % last_profile)
            
            # Save the data.
            self.save(show_dialog = False, from_options = True)
        
        # If the user pressed Reset:
        elif response == 3:
            
            # Confirm that the user wants to reset the options.
            reset = show_question_dialog(opt_dlg, "Options", "Are you sure you want to reset the options to the default values?")
                
            # If the user doesn't want to, don't continue.
            if response == Gtk.ResponseType.CANCEL:
                
                # Close the dialog.
                opt_dlg.destroy()
                
                return
            
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
            if current_units != config["units"]:
                
                # Ask the user if they want to convert the data.
                response = show_question_dialog(opt_dlg, "Options", "The units have changed from %s to %s.\n\nWould you like to convert the data to the new units?" % (current_units, config["units"]))
                
                # If the user wants to convert the data:
                if response == Gtk.ResponseType.OK:
                    
                    # Convert the data.
                    new_data = convert.convert(data, config["units"])
                    
                    # Update the list.
                    data[:] = []
                    data[:] = new_data[:]
                    
                    # Update the ListStore.
                    self.liststore.clear()
                    for i in data:
                        self.liststore.append(i)
            
            # Add/remove the units, if desired:
            if not config["show_units"]:
                self.temp_col.set_title("Temperature")
                self.prec_col.set_title("Precipitation")
                self.wind_col.set_title("Wind")
                self.humi_col.set_title("Humidity")
                self.airp_col.set_title("Air Pressure")
            else:
                self.temp_col.set_title("Temperature (%s)" % units["temp"])
                self.prec_col.set_title("Precipitation (%s)" % units["prec"])
                self.wind_col.set_title("Wind (%s)" % units["wind"])
                self.humi_col.set_title("Humidity (%)")
                self.airp_col.set_title("Air Pressure (%s)" % units["airp"])
            
            # Set the title, if desired:
            if config["show_dates"]:
                self.set_title("WeatherLog - %s - %s to %s" % (last_profile, (data[0][0] if len(data) != 0 else "None"), (data[len(data)-1][0] if len(data) != 0 else "None")))
            else:
                self.set_title("WeatherLog - %s" % last_profile)
            
            # Save the data.
            self.save(show_dialog = False, from_options = True)
        
        # Close the dialog.
        opt_dlg.destroy()
    
    
    def save(self, show_dialog = True, automatic = True, from_options = False):
        """Saves the data."""
        
        # If the user doesn't want automatic saves, don't continue.
        if automatic and not config["auto_save"] and not from_options:
            return
        
        # Save to the file.
        try:
            # This should save to ~/.weatherlog/[profile name]/weather.json on Linux.
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
            # This should save to ~/.weatherlog/lastprofile on Linux.
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
            show_alert_dialog(self, "Manual Save - %s" % last_profile, "Data has been saved.")
    
    
    def reload_current(self, event):
        """Reloads the current data."""
        
        global data
        
        # Show the confirmation dialog, but only if auto-saving isn't turned on.
        if config["auto_save"] == False:
            response = show_question_dialog(self, "Reload Current Data - %s" % last_profile, "Are you sure you want to reload the current data?\n\nUnsaved changes will be lost.")
        else:
            response = Gtk.ResponseType.OK
        
        # If the user wants to continue:
        if response == Gtk.ResponseType.OK:
            
            # Clear the list.
            data[:] = []
            
            # Clear the ListStore.
            self.liststore.clear()
            
            # Load the data.   
            try:
                # This should be ~/.weatherlog/[profile name]/weather.json on Linux.
                data_file = open("%s/profiles/%s/weather.json" % (main_dir, last_profile), "r")
                data = json.load(data_file)
                data_file.close()
                
            except IOError:
                # Show the error message, and close the application.
                # This one shows if there was a problem reading the file.
                print("Error reloading data (IOError).")
                data = []
                
            except (TypeError, ValueError):
                # Show the error message, and close the application.
                # This one shows if there was a problem with the data type.
                print("Error reloading data (TypeError or ValueError).")
                data = []
            
            # Update the ListStore.
            for i in data:
                self.liststore.append(i)
        
        # Tell the user the data has been reloaded.
        show_alert_dialog(self, "Reload Current Data - %s" % last_profile, "Data has been reloaded.")
    
    
    def show_about(self, event):
        """Shows the About dialog."""
        
        # Load the icon.
        img_file = open("weatherlog_resources/images/icon.png", "rb")
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
        webbrowser.open_new("weatherlog_resources/help/help.html")    
    

    def exit(self, x, y):
        """Closes the application."""
        
        # Save the data.
        self.save(show_dialog = False)
        
        # Show the confirmation dialog, if the user wants that.
        if config["confirm_exit"]:
            response = show_question_dialog(self, "Quit", "Are you sure you want to close the application?")
        
        # If the user wants to continue:
        if config["confirm_exit"] and response == Gtk.ResponseType.OK:
        
            # Save the data.
            self.save(show_dialog = False, from_options = True)
            
            # Close the application.
            Gtk.main_quit()
            
            return False
        
        # If the user pressed cancel:
        elif config["confirm_exit"] and response == Gtk.ResponseType.CANCEL:
            
            return True
        
        # If the user doesn't want a confirmation dialog, quit immediately.
        if not config["confirm_exit"]:
            
            # Save the data.
            self.save(show_dialog = False, from_options = True)
            
            # Close the  application.
            Gtk.main_quit()


# Show the window and start the application, but only if there are no exta arguments.
if __name__ == "__main__" and len(sys.argv) == 1:
    
    # Show the window and start the application.
    win = Weather()
    win.connect("delete-event", win.exit)
    win.show_all()
    Gtk.main()

# If there are arguments, add them to the data list and don't show the interface
elif __name__ == "__main__" and len(sys.argv) > 1:
    
    # Add a row of data:
    if sys.argv[1] == "add":
        
        command_line.add(data, main_dir, last_profile, sys.argv)
        
    
    # Remove a row of data:
    elif sys.argv[1] == "remove":
        
        command_line.remove(data, main_dir, last_profile, sys.argv)
    
    
    # Clear the current profile:
    elif sys.argv[1] == "clear":
        
        command_line.clear(main_dir, last_profile)
    
    
    # Clear all the data:
    elif sys.argv[1] == "clear_all":
        
        # Delete all the files.
        shutil.rmtree(main_dir)
    
    
    # Switch profiles:
    elif sys.argv[1] == "switch_profile":
        
        command_line.switch_profile(main_dir, sys.argv[2])
    
    
    # Add a new profile:
    elif sys.argv[1] == "add_profile":
        
        command_line.add_profile(main_dir, sys.argv[2])
    
    
    # Remove an existing profile:
    elif sys.argv[1] == "remove_profile":
        
        command_line.remove_profile(main_dir, last_profile, sys.argv[2])
    
    # Show the help:
    elif sys.argv[1] == "help":
        
        # Open the help file.
        webbrowser.open_new("weatherlog_resources/help/help.html")
    
    # Set the options:
    elif sys.argv[1] == "options":
        
        command_line.options(py_version, config, main_dir)
    
    # Reset the options:
    elif sys.argv[1] == "reset_options":
        
        command_line.reset_options(config, main_dir)
    
    # Set the window size:
    elif sys.argv[1] == "window_size":
        
        command_line.window_size(main_dir, sys.argv)
