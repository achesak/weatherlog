# -*- coding: utf-8 -*-


################################################################################

# Weather Or Not
# Version 0.1

# Weather Or Not is an application for keeping track of the weather.

# Released under the MIT open source license:
"""
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
from gi.repository import Gtk
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
# Import the function for validating the data.
import resources.validate as validate
# Import the dialogs.
from resources.dialogs.new_dialog import *
from resources.dialogs.info_dialog import *
from resources.dialogs.data_dialog import *
from resources.dialogs.add_profile_dialog import *
from resources.dialogs.switch_profile_dialog import *
from resources.dialogs.remove_profile_dialog import *


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

# Get the last profile
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


class Weather(Gtk.Window):
    """Shows the main application."""
    def __init__(self):
        """Create the application."""
        # Create the window.
        Gtk.Window.__init__(self, title = "Weather Or Not")
        # Set the default size. This should be a good value on all except very tiny screens.
        self.set_default_size(900, 500)
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
        date_col = Gtk.TreeViewColumn("Date", date_text, text = 0)
        self.treeview.append_column(date_col)
        # Create the Temperature column.
        temp_text = Gtk.CellRendererText()
        temp_col = Gtk.TreeViewColumn("Temperature (°C)", temp_text, text = 1)
        self.treeview.append_column(temp_col)
        # Create the Precipation column.
        prec_text = Gtk.CellRendererText()
        prec_col = Gtk.TreeViewColumn("Precipation (cm)", prec_text, text = 2)
        self.treeview.append_column(prec_col)
        # Create the Wind column.
        wind_text = Gtk.CellRendererText()
        wind_col = Gtk.TreeViewColumn("Wind (kph)", wind_text, text = 3)
        self.treeview.append_column(wind_col)
        # Create the Humidity column.
        humi_text = Gtk.CellRendererText()
        humi_col = Gtk.TreeViewColumn("Humidity (%)", humi_text, text = 4)
        self.treeview.append_column(humi_col)
        # Create the Air Pressure column.
        airp_text = Gtk.CellRendererText()
        airp_col = Gtk.TreeViewColumn("Air Pressure (hPa)", airp_text, text = 5)
        self.treeview.append_column(airp_col)
        # Create the Cloud Cover column.
        clou_text = Gtk.CellRendererText()
        clou_col = Gtk.TreeViewColumn("Cloud Cover", clou_text, text = 6)
        self.treeview.append_column(clou_col)
        # Create the Notes column.
        note_text = Gtk.CellRendererText()
        note_col = Gtk.TreeViewColumn("Notes", note_text, text = 7)
        self.treeview.append_column(note_col)
        
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
            ("remove", Gtk.STOCK_REMOVE, "_Remove...", "<Control>r", "Remove a day from the list", self.remove),
            ("import", Gtk.STOCK_OPEN, "_Import...", None, "Import data from a file", self.import_file),
            ("import_profile", None, "Import as New _Profile...", "<Control><Shift>o", None, self.import_new_profile),
            ("export", Gtk.STOCK_SAVE, "_Export...", None, "Export data to a file", self.export_file),
            ("export_html", None, "Export to _HTML...", "<Control><Shift>h", None, self.export_file_html),
            ("export_csv", None, "Export to _CSV...", "<Control><Shift>c", None, self.export_file_csv),
            ("info", Gtk.STOCK_INFO, "_Info...", "<Control>i", "Show info about the data", self.show_info)
        ])
        
        # Create the Weather -> More Info submenu.
        action_weather_info_group = Gtk.Action("info_menu", "_More Info...", None, None)
        action_group.add_action(action_weather_info_group)
        action_group.add_actions([
            ("temperature", None, "_Temperature...", "<Control>t", None, self.show_info_temp),
            ("precipitation", None, "_Precipitation...", "<Control>p", None, self.show_info_prec),
            ("wind", None, "_Wind...", "<Control>w", None, self.show_info_wind),
            ("humidity", None, "_Humidity...", "<Control>h", None, self.show_info_humi),
            ("air_pressure", None, "_Air Pressure...", "<Control>a", None, self.show_info_airp),
            ("cloud_cover", None, "_Cloud Cover...", "<Control>c", None, self.show_info_clou),
            ("clear_data", Gtk.STOCK_CLEAR, "Clear _Data...", "<Control>d", "Clear the data", self.clear),
            ("fullscreen", Gtk.STOCK_FULLSCREEN, "Toggle _Fullscreen", "F11", "Toggle fullscreen", self.toggle_fullscreen),
            ("exit", Gtk.STOCK_QUIT, "E_xit...", None, "Close the application", lambda x: self.exit("ignore", "this"))
        ])
        
        # Create the Profiles menu.
        action_group.add_actions([
            ("profiles_menu", None, "Profiles"),
            ("switch_profile", None, "_Switch Profile...", "<Control><Shift>s", None, self.switch_profile),
            ("add_profile", None, "_Add Profile...", "<Control><Shift>n", None, self.add_profile),
            ("remove_profile", None, "_Remove Profile...", "<Control><Shift>d", None, self.remove_profile)
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
        
        # Add the menubar
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
        self.set_title("Weather Or Not - %s" % last_profile)
    
    
    def add_new(self, event):
        """Shows the dialog for input of new data."""
        
        global data
        
        # Show the dialog.
        new_dlg = AddNewDialog(self)
        # Get the response.
        response = new_dlg.run()
        
        # If the user clicked the OK button, add the data.
        if response == Gtk.ResponseType.OK:
            
            # Get the data from the entries and comboboxes.
            date = new_dlg.date_ent.get_text()
            temp = new_dlg.temp_ent.get_text()
            prec = new_dlg.prec_ent.get_text()
            prec_type = new_dlg.prec_com.get_active_text()
            wind = new_dlg.wind_ent.get_text()
            wind_dir = new_dlg.wind_com.get_active_text()
            humi = new_dlg.humi_ent.get_text()
            airp = new_dlg.airp_ent.get_text()
            clou = new_dlg.clou_com.get_active_text()
            note = new_dlg.note_ent.get_text()                
            
            # If anything required was missing, cancel this action. Everything is required except for the notes.
            # Also check to make sure everything is of the correct type.
            missing_msg = validate.validate(date, temp, prec, prec_type, wind, wind_dir, humi, airp, clou)
            
            # If the error message isn't blank, show the dialog.
            if missing_msg:
                
                # Create the error dialog.
                err_miss_dlg = Gtk.MessageDialog(new_dlg, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Add New")
                err_miss_dlg.format_secondary_text("There were one or more problems with the data entered.\n\n%s" % missing_msg.rstrip())
                
                # Show the error dialog.
                err_miss_dlg.run()
                
                # Close the error dialog and the "Add New" dialog. The second one
                # is needed because of a bug where the window will stop responding
                # to events, making it useless. Fix later!
                err_miss_dlg.destroy()
                new_dlg.destroy()
            
            # If the date is already used, show the dialog.
            elif date in utility_functions.get_column(data, 0):
                
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
                new_data = [date, temp, "%s%s" % ((prec + " " if prec_type != "None" else ""), prec_type), "%s%s" % ((wind + " " if wind_dir != "None" else ""), wind_dir), humi, airp, clou, note]
                data.append(new_data)
                
                # Sort the list.
                data = sorted(data, key = lambda x: datetime.datetime.strptime(x[0], '%d/%m/%y'))
                
                # Update the ListStore.
                self.liststore.clear()
                for i in data:
                    self.liststore.append(i)
        
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
            # If nothing was selected, don't continue.
            return
        
        # Confirm that the user wants to delete the row.
        rem_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "Confirm Remove")
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
    
    
    def show_info(self, event):
        """Shows info about the data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "General Info")
            return
        
        # Get the date data.
        date_data = utility_functions.get_column(data, 0)
        date_first = date_data[0]
        date_last = date_data[len(date_data) - 1]
        date_first2 = datetime.datetime.strptime(date_first, "%d/%m/%y")
        date_last2 = datetime.datetime.strptime(date_last, "%d/%m/%y")
        date_num = (date_last2 - date_first2).days + 1
        
        # Get the temperature data.
        temp_data = utility_functions.convert_float(utility_functions.get_column(data, 1))
        temp_low = min(temp_data)
        temp_high = max(temp_data)
        temp_avg = info_functions.mean(temp_data)
        
        # Get the precipitation data.
        prec_data1, prec_data2 = utility_functions.split_list(utility_functions.get_column(data, 2))
        prec_data1 = utility_functions.convert_float(prec_data1)
        prec_low = min(prec_data1)
        prec_high = max(prec_data1)
        prec_avg = info_functions.mean(prec_data1)
        
        # Get the wind data.
        wind_data1, wind_data2 = utility_functions.split_list(utility_functions.get_column(data, 3))
        wind_data1 = utility_functions.convert_float(wind_data1)
        wind_low = min(wind_data1)
        wind_high = max(wind_data1)
        wind_avg = info_functions.mean(wind_data1)
        
        # Get the humidity data.
        humi_data = utility_functions.convert_float(utility_functions.get_column(data, 4))
        humi_low = min(humi_data)
        humi_high = max(humi_data)
        humi_avg = info_functions.mean(humi_data)
        
        # Get the air pressure data.
        airp_data = utility_functions.convert_float(utility_functions.get_column(data, 5))
        airp_low = min(airp_data)
        airp_high = max(airp_data)
        airp_avg = info_functions.mean(airp_data)
        
        # Get the cloud cover data.
        clou_data = Counter(utility_functions.get_column(data, 6))
        clou_mode = clou_data.most_common(1)[0][0]
        
        # Create the data list.
        data2 = [
            ["First day", "%s" % date_first],
            ["Last day", "%s" % date_last],
            ["Number of days", "%d" % date_num],
            ["Lowest temperature", "%.2f °C" % temp_low], 
            ["Highest temperature", "%.2f °C" % temp_high],
            ["Average temperature", "%.2f °C" % temp_avg],
            ["Lowest precipitation", "%.2f cm" % prec_low],
            ["Highest precipitation", "%.2f cm" % prec_high],
            ["Average precipitation", "%.2f cm" % prec_avg],
            ["Lowest wind speed", "%.2f kph" % wind_low],
            ["Highest wind speed", "%.2f kph" % wind_high],
            ["Average wind speed", "%.2f kph" % wind_avg],
            ["Lowest humidity", "%.2f%%" % humi_low], 
            ["Highest humidity", "%.2f%%" % humi_high],
            ["Average humidity", "%.2f%%" % humi_avg],
            ["Lowest air pressure", "%.2f hPa" % airp_low],
            ["Highest air pressure", "%.2f hPa" % airp_high],
            ["Average air pressure", "%.2f hPa" % airp_avg],
            ["Most common cloud cover", "%s" % clou_mode]
        ]        
        
        # Show the dialog.
        info_dlg = GenericInfoDialog(self, "General Info", data2)
        info_dlg.run()
        
        # Close the dialog. The response can be ignored.
        info_dlg.destroy()
    
    
    def show_info_temp(self, event):
        """Shows info about the temperature data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Temperature Info")
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
            ["Lowest", "%.2f °C" % temp_low],
            ["Highest", "%.2f °C" % temp_high],
            ["Average", "%.2f °C" % temp_avg],
            ["Median", "%.2f °C" % temp_median],
            ["Range", "%.2f °C" % temp_range],
            ["Most common", "%.2f °C" % temp_mode]
        ]
        
        # Show the dialog.
        temp_dlg = GenericInfoDialog(self, "Temperature Info", data2)
        temp_dlg.run()
        
        # Close the dialog. The response can be ignored.
        temp_dlg.destroy()
    
    
    def show_info_prec(self, event):
        """Shows info about the precipitation data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Precipitation Info")
            return
        
        # Get the data.
        prec_data1, prec_data2 = utility_functions.split_list(utility_functions.get_column(data, 2))
        prec_split = utility_functions.split_list2(utility_functions.get_column(data, 2))
        prec_data1 = utility_functions.filter_none(prec_data1, prec_data2)
        prec_data1 = utility_functions.convert_float(prec_data1)
        prec_low = min(prec_data1)
        prec_high = max(prec_data1)
        prec_avg = info_functions.mean(prec_data1)
        prec_median = info_functions.median(prec_data1)
        prec_range = info_functions.range(prec_data1)
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
        
        # Create the data list.
        data2 = [
            ["Lowest", "%.2f cm" % prec_low],
            ["Highest", "%.2f cm" % prec_high],
            ["Average", "%.2f cm" % prec_avg],
            ["Median", "%.2f cm" % prec_median],
            ["Range", "%.2f cm" % prec_range],
            ["Total (all)", "%.2f cm" % prec_total],
            ["Total (rain)", "%.2f cm" % prec_total_rain],
            ["Total (snow)", "%.2f cm" % prec_total_snow],
            ["Total (hail)", "%.2f cm" % prec_total_hail],
            ["Total (sleet)", "%.2f cm" % prec_total_sleet],
            ["None", "%d day%s" % (prec_none, "" if prec_none == 1 else "s")],
            ["Rain", "%d day%s" % (prec_rain, "" if prec_rain == 1 else "s")],
            ["Snow", "%d day%s" % (prec_snow, "" if prec_snow == 1 else "s")],
            ["Hail", "%d day%s" % (prec_hail, "" if prec_hail == 1 else "s")],
            ["Sleet", "%d day%s" % (prec_sleet, "" if prec_sleet == 1 else "s")],
            ["Most common type", "%s" % (prec_mode if prec_mode != "" else "None")]
        ]
        
        # Show the dialog.
        prec_dlg = GenericInfoDialog(self, "Precipitation Info", data2)
        prec_dlg.run()
        
        # Close the dialog. The response can be ignored.
        prec_dlg.destroy()
    
    
    def show_info_wind(self, event):
        """Shows info about the wind data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Wind Info")
            return
        
        # Get the data.
        wind_data1, wind_data2 = utility_functions.split_list(utility_functions.get_column(data, 3))
        wind_data1 = utility_functions.filter_none(wind_data1, wind_data2)
        wind_data1 = utility_functions.convert_float(wind_data1)
        wind_low = min(wind_data1)
        wind_high = max(wind_data1)
        wind_avg = info_functions.mean(wind_data1)
        wind_median = info_functions.median(wind_data1)
        wind_range = info_functions.range(wind_data1)
        wind_mode = info_functions.mode(wind_data2)
        
        # Create the data list.
        data2 = [
            ["Lowest", "%.2f kph" % wind_low],
            ["Highest", "%.2f kph" % wind_high],
            ["Average", "%.2f kph" % wind_avg],
            ["Median", "%.2f kph" % wind_median],
            ["Range", "%.2f kph" % wind_range],
            ["Most common direction", "%s" % (wind_mode if wind_mode != "" else "None")]
        ]
        
        # Show the dialog.
        wind_dlg = GenericInfoDialog(self, "Wind Info", data2)
        wind_dlg.run()
        
        # Close the dialog. The response can be ignored.
        wind_dlg.destroy()
    
    
    def show_info_humi(self, event):
        """Shows info about the humidity data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Humidity Info")
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
        humi_dlg = GenericInfoDialog(self, "Humidity Info", data2)
        humi_dlg.run()
        
        # Close the dialog. The response can be ignored.
        humi_dlg.destroy()
    
    
    def show_info_airp(self, event):
        """Shows info about the air pressure data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Air Pressure Info")
            return
        
        # Get the data.
        airp_data = utility_functions.convert_float(utility_functions.get_column(data, 5))
        airp_low = min(airp_data)
        airp_high = max(airp_data)
        airp_avg = info_functions.mean(airp_data)
        airp_median = info_functions.median(airp_data)
        airp_range = info_functions.range(airp_data)
        airp_mode = info_functions.mode(airp_data)
        
        # Create the data list.
        data2 = [
            ["Lowest", "%.2f hPa" % airp_low],
            ["Highest", "%.2f hPa" % airp_high],
            ["Average", "%.2f hPa" % airp_avg],
            ["Median", "%.2f hPa" % airp_median],
            ["Range", "%.2f hPa" % airp_range],
            ["Most common", "%.2f hPa" % airp_mode]
        ]
        
        # Show the dialog.
        airp_dlg = GenericInfoDialog(self, "Air Pressure Info", data2)
        airp_dlg.run()
        
        # Close the dialog. The response can be ignored.
        airp_dlg.destroy()
    
    
    def show_info_clou(self, event):
        """Shows info about the cloud cover data."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Cloud Cover Info")
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
        clou_dlg = GenericInfoDialog(self, "Cloud Cover Info", data2)
        clou_dlg.run()
        
        # Close the dialog. The response can be ignored.
        clou_dlg.destroy()
    
    
    def import_file(self, event):
        """Imports data from a file."""
        
        # Confirm that the user wants to overwrite the data.
        over_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "Confirm Import")
        over_dlg.format_secondary_text("Are you sure you want to import the data?\n\nCurrent data will be overwritten.")
        
        # Get the response.
        response = over_dlg.run()
        over_dlg.destroy()
        
        # If the user doesn't want to overwrite, cancel the action.
        if response != Gtk.ResponseType.OK:
            return
        
        # Create the dialog.
        import_dlg = Gtk.FileChooserDialog("Import", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        # Set the filters.
        filter_all = Gtk.FileFilter()
        filter_all.set_name("All files")
        filter_all.add_pattern("*")
        filter_json = Gtk.FileFilter()
        filter_json.set_name("Weather Or Not data files")
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
    
    
    def import_new_profile(self, event):
        """Imports data from a file in a new profile."""
        
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
                    json.dump(data, data_file, indent = 4)
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
                self.set_title("Weather Or Not - %s" % last_profile)
        
            # Close the dialog.
            new_dlg.destroy()
        
        # Otherwise, close the dialog and don't go any further.
        else:
            
            new_dlg.destroy()
            return
        
        # Create the dialog.
        import_dlg = Gtk.FileChooserDialog("Import", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        # Set the filters.
        filter_all = Gtk.FileFilter()
        filter_all.set_name("All files")
        filter_all.add_pattern("*")
        filter_json = Gtk.FileFilter()
        filter_json.set_name("Weather Or Not data files")
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
        
        # Create the dialog.
        export_dlg = Gtk.FileChooserDialog("Export", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
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
        
        # Convert to data to HTML.
        html = export.html(data)
        
        # Create the dialog.
        export_html_dlg = Gtk.FileChooserDialog("Export to HTML", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
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
        
        # Convert the data to CSV.
        csv = export.csv(data)
        
        # Create the dialog.
        export_csv_dlg = Gtk.FileChooserDialog("Export to CSV", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
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
    
    
    def clear(self, event):
        """Clears the data."""
        
        # Confirm that the user wants to clear the data.
        clear_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "Confirm Clear")
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
                    json.dump(data, data_file, indent = 4)
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
                self.set_title("Weather Or Not - %s" % last_profile)
        
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
                    json.dump(data, data_file, indent = 4)
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
                self.set_title("Weather Or Not - %s" % last_profile)
        
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
    
    
    def show_about(self, event):
        """Shows the About dialog."""
        
        # Create the dialog.
        about_dlg = Gtk.AboutDialog()
        
        # Set the title.
        about_dlg.set_title("About Weather Or Not")
        # Set the program name.
        about_dlg.set_program_name(TITLE)
        # Set the program version.
        about_dlg.set_version(VERSION)
        # Set the comments. Maybe come up with something better later?
        about_dlg.set_comments("Weather Or Not is an application for keeping track of the weather.")
        # Set the copyright notice. Legal stuff, bleh.
        about_dlg.set_copyright("Copyright (c) 2013 Adam Chesak")
        # Set the authors. This is, of course, only me. I feel special.
        about_dlg.set_authors(["Adam Chesak <achesak@yahoo.com>"])
        # Set the license. I think this can be used with GTK3? (It's LGPL.)
        about_dlg.set_license_type(Gtk.License.MIT_X11)
        # Set the website. Change this to the site on github, when I get that up.
        about_dlg.set_website("http://poultryandprogramming.wordpress.com/")
        about_dlg.set_website_label("http://poultryandprogramming.wordpress.com/")
        
        # Show the dialog.
        about_dlg.show_all()
        
        # Have the dialog close when the user presses the Close button.
        # There is only one button, so it's not necessary to check for 
        # Gtk.ResponseType.CLOSE here.
        about_dlg.run()
        about_dlg.destroy()

    
    def show_help(self, event):
        """Shows the help in a web browser."""
        
        # Open the website.
        webbrowser.open("http://poultryandprogramming.wordpress.com/programming/weather-or-not-help/")    
    

    def exit(self, x, y):
        """Saves data and closes the application."""
        
        # Save to the file.
        try:
            # This should save to ~/.weatherornot/[profile name]/weather.json on Linux.
            data_file = open("%s/profiles/%s/weather.json" % (main_dir, last_profile), "w")
            json.dump(data, data_file, indent = 4)
            data_file.close()
            
        except IOError:
            # Show the error message if something happened, but continue.
            # This one is shown if there was an error writing to the file.
            print("Error saving data file (IOError).")
        
        except (TypeError, ValueError):
            # Show the error message if something happened, but continue.
            # This one is shown if there was an error with the data type.
            print("Error saving data file (TypeError or ValueError).")
            
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
        
        # Close the  application.
        Gtk.main_quit()


# Show the window and start the application.
if __name__ == "__main__":
    win = Weather()
    win.connect("delete-event", win.exit)
    win.show_all()
    Gtk.main()