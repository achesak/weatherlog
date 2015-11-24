#!/usr/bin/env python
# -*- coding: utf-8 -*-


################################################################################

# WeatherLog
# Version 3.4

# WeatherLog is an application for keeping track of the weather and
# getting information about past trends.

# Released under the MIT open source license:
license_text = """
Copyright (c) 2013-2015 Adam Chesak

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


# Import Gtk and Gdk for the interface.
from gi.repository import Gtk, Gdk, GdkPixbuf
# Import json for saving export data.
import json
# Import webbrowser for opening the help in the user's browser.
import webbrowser
# Import datetime for date operations.
import datetime
# Import modules for working with directories.
import shutil, os, os.path
# Import sys for closing the application.
import sys
# Import copy for deep copying lists.
import copy
# Import pickle for loading and saving the data.
try:
    import cPickle as pickle
except ImportError:
    import pickle
# Import urlopen and urlencode for opening a file from a URL.
try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen, urlencode

# Tell Python not to create bytecode files, as they mess with the git repo.
# This line can be removed be the user, if desired.
sys.dont_write_bytecode = True

# Import constants.
from weatherlog_resources.constants import *
# Import the functions for setting up the application.
import weatherlog_resources.launch as launch
# Import the functions for working with datasets.
import weatherlog_resources.datasets as datasets
# Import the functions for working with dates.
import weatherlog_resources.dates as dates
# Import the functions for validating user-entered data.
import weatherlog_resources.validate as validate
# Import the functions for converting between units.
import weatherlog_resources.convert as convert
# Import the functions for reading and writing datasets.
import weatherlog_resources.io as io
# Import the functions for exporting the data.
import weatherlog_resources.export as export
# Import the functions for getting the info.
import weatherlog_resources.info as info
# Import the functions for getting the chart data.
import weatherlog_resources.charts as charts
# Import the functions for getting the graph data.
import weatherlog_resources.graphs as graphs
# Import the functions for filtering the data.
import weatherlog_resources.filter_data as filter_data
# Import the functions for getting the current weather.
import weatherlog_resources.get_weather as get_weather

# Import dialogs.
from weatherlog_resources.dialogs.new_dialog import AddNewDialog
from weatherlog_resources.dialogs.edit_dialog import EditDialog
from weatherlog_resources.dialogs.info_dialog import GenericInfoDialog
from weatherlog_resources.dialogs.dataset_name_dialog import DatasetNameDialog
from weatherlog_resources.dialogs.dataset_selection_dialog import DatasetSelectionDialog
from weatherlog_resources.dialogs.calendar_dialog import CalendarRangeDialog
from weatherlog_resources.dialogs.date_selection_dialog import DateSelectionDialog
from weatherlog_resources.dialogs.options_dialog import OptionsDialog
from weatherlog_resources.dialogs.chart_dialog import GenericChartDialog
from weatherlog_resources.dialogs.graph_dialog import GenericGraphDialog
from weatherlog_resources.dialogs.data_subset_selection_dialog import DataSubsetSelectionDialog
from weatherlog_resources.dialogs.import_selection_dialog import ImportSelectionDialog
from weatherlog_resources.dialogs.location_dialog import LocationDialog
from weatherlog_resources.dialogs.weather_dialog import CurrentWeatherDialog
from weatherlog_resources.dialogs.export_pastebin_dialog import ExportPastebinDialog
from weatherlog_resources.dialogs.misc_dialogs import *


class WeatherLog(Gtk.Window):
    """Creates the WeatherLog application."""
    
    def __init__(self):
        """Initializes the application."""
        
        # Get the application's UI data.
        self.VERSION, self.TITLE, self.MENU_DATA, self.ICON_SMALL, self.ICON_MEDIUM = launch.get_ui_info()
        # Get the data and configuration directories.
        self.main_dir, self.conf_dir = launch.get_main_dir()
        # Check if the directory and base files exist, and create them if they don't.
        launch.check_files_exist(self.main_dir, self.conf_dir)
        # Get the last dataset.
        self.last_profile, self.original_profile, self.profile_exists = launch.get_last_profile(self.main_dir, self.conf_dir)
        # Get the configuration.
        self.config = launch.get_config(self.conf_dir)
        # Get the previous window size.
        self.last_width, self.last_height = launch.get_window_size(self.conf_dir, self.config)
        # Get the units.
        self.units = launch.get_units(self.config)
        # Get the dataset data.
        self.data = launch.get_data(self.main_dir, self.last_profile)
        # Get the weather codes.
        self.weather_codes = launch.codes
        # Try importing matplotlib, just so we know if it's installed.
        try:
            from matplotlib.figure import Figure
            self.matplotlib_installed = True
        except ImportError:
            self.matplotlib_installed = False
        
        # Create the user interface.
        self.create_interface()
        
        # If the dataset could not be found, tell the user and save as the default dataset.
        if not self.profile_exists:
            show_alert_dialog(self, "WeatherLog", "The dataset \"%s\" could not be found and was not loaded." % self.original_profile)
            self.save()
        
        # Add the data.
        self.update_list()
        
        # Set the new title.
        self.update_title()
    
    
    def create_interface(self):
        """Creates the user interface."""
        
        # Create the window.
        Gtk.Window.__init__(self, title = self.TITLE)
        self.set_default_size(self.last_width, self.last_height)
        self.set_icon_from_file(self.ICON_SMALL)
        
        # Create the main UI.
        self.liststore = Gtk.ListStore(str, str, str, str, str, str, str, str, str, str)
        self.treeview = Gtk.TreeView(model = self.liststore)
        date_text = Gtk.CellRendererText()
        self.date_col = Gtk.TreeViewColumn("Date", date_text, text = 0)
        self.treeview.append_column(self.date_col)
        temp_text = Gtk.CellRendererText()
        self.temp_col = Gtk.TreeViewColumn("Temperature (%s)" % self.units["temp"], temp_text, text = 1)
        self.treeview.append_column(self.temp_col)
        chil_text = Gtk.CellRendererText()
        self.chil_col = Gtk.TreeViewColumn("Wind Chill (%s)" % self.units["temp"], chil_text, text = 2)
        self.treeview.append_column(self.chil_col)
        prec_text = Gtk.CellRendererText()
        self.prec_col = Gtk.TreeViewColumn("Precipitation (%s)" % self.units["prec"], prec_text, text = 3)
        self.treeview.append_column(self.prec_col)
        wind_text = Gtk.CellRendererText()
        self.wind_col = Gtk.TreeViewColumn("Wind (%s)" % self.units["wind"], wind_text, text = 4)
        self.treeview.append_column(self.wind_col)
        humi_text = Gtk.CellRendererText()
        self.humi_col = Gtk.TreeViewColumn("Humidity (%)", humi_text, text = 5)
        self.treeview.append_column(self.humi_col)
        airp_text = Gtk.CellRendererText()
        self.airp_col = Gtk.TreeViewColumn("Air Pressure (%s)" % self.units["airp"], airp_text, text = 6)
        self.treeview.append_column(self.airp_col)
        visi_text = Gtk.CellRendererText()
        self.visi_col = Gtk.TreeViewColumn("Visibility (%s)" % self.units["visi"], visi_text, text = 7)
        self.treeview.append_column(self.visi_col)
        clou_text = Gtk.CellRendererText()
        self.clou_col = Gtk.TreeViewColumn("Cloud Cover", clou_text, text = 8)
        self.treeview.append_column(self.clou_col)
        note_text = Gtk.CellRendererText()
        self.note_col = Gtk.TreeViewColumn("Notes", note_text, text = 9)
        self.treeview.append_column(self.note_col)
        
        # Create the menus.
        action_group = Gtk.ActionGroup("actions")
        action_group.add_actions([
            ("weather_menu", None, "_Weather"),
            ("add_new", Gtk.STOCK_ADD, "Add _New Data...", "<Control>n", "Add a new day to the list", self.add_new),
            ("edit", None, "_Edit Data...", "<Control>e", None, self.edit),
            ("remove", Gtk.STOCK_REMOVE, "Remo_ve Data...", "<Control>r", "Remove a day from the list", self.remove),
            ("clear_data", Gtk.STOCK_CLEAR, "Clear Current _Data...", None, "Clear the data", self.clear),
            ("clear_all", None, "Clear _All Data...", None, None, self.clear_all),
            ("get_current_here", None, "Get Current _Weather...", "<Control>w", None, lambda x: self.get_weather(True)),
            ("get_current_there", None, "Get Current Weather _For...", None, None, lambda x: self.get_weather(False)),
            ("exit", Gtk.STOCK_QUIT, "_Quit", None, "Close the application", lambda x: self.exit())
        ])
        action_group.add_actions([
            ("file_menu", None, "_File"),
            ("import", Gtk.STOCK_OPEN, "_Import...", None, "Import data from a file", self.import_file),
            ("import_merge", None, "Imp_ort and Merge...", "<Control><Shift>o", None, self.import_merge),
            ("import_dataset", None, "Import as New _Dataset...", None, None, self.import_new_dataset),
            ("export", Gtk.STOCK_SAVE, "_Export...", None, "Export data to a file", self.export_file),
            ("export_pastebin", None, "Export to _Pastebin...", None, None, self.export_pastebin)
        ])
        action_group.add_actions([
            ("info_global_menu", None, "_Info"),
            ("info", Gtk.STOCK_INFO, "_Info...", "<Control>i", "Show info about the data", lambda x: self.show_info_generic()),
            ("info_range", None, "Info in _Range...", "<Control><Shift>i", None, lambda x: self.info_range()),
            ("info_selected", None, "Info for _Selected Dates...", None, None, lambda x: self.info_selected()),
            ("charts", None, "_Charts...", "<Control>c", None, lambda x: self.show_chart_generic()),
            ("charts_range", None, "Charts i_n Range...", "<Control><Shift>c", None, lambda x: self.chart_range()),
            ("charts_selected", None, "Charts _for Selected Dates...", None, None, lambda x: self.chart_selected()),
            ("graphs", None, "_Graphs...", "<Control>g", None, lambda x: self.show_graph_generic()),
            ("graphs_range", None, "Gra_phs in Range...", "<Control><Shift>g", None, lambda x: self.graph_range()),
            ("graphs_selected", None, "Grap_hs for Selected Dates...", None, None, lambda x: self.graph_selected()),
            ("view_subset", None, "View _Data Subset...", "<Control>d", None, self.select_data_subset),
        ])
        action_group.add_actions([
            ("datasets_menu", None, "_Datasets"),
            ("switch_dataset", None, "_Switch Dataset...", "<Control><Shift>s", None, self.switch_dataset),
            ("add_dataset", None, "_Add Dataset...", "<Control><Shift>n", None, self.add_dataset),
            ("remove_dataset", None, "_Remove Datasets...", None, None, self.remove_dataset),
            ("rename_dataset", None, "Re_name Current Dataset...", None, None, self.rename_dataset),
            ("merge_datasets", None, "_Merge Datasets...", None, None, self.merge_datasets),
            ("copy_new", None, "Copy _Data to New Dataset...", None, None, self.data_dataset_new),
            ("copy_existing", None, "Copy Data to _Existing Dataset...", None, None, self.data_dataset_existing)
        ])
        action_group.add_actions([
            ("options_menu", None, "_Options"),
            ("options", None, "_Options...", "F2", None, self.options)
        ])
        action_group.add_actions([
            ("help_menu", None, "_Help"),
            ("about", Gtk.STOCK_ABOUT, "_About...", "<Shift>F1", None, self.show_about),
            ("help", Gtk.STOCK_HELP, "_Help...", None, None, self.show_help)
        ])
        
        # Set up the menus.
        ui_manager = Gtk.UIManager()
        ui_manager.add_ui_from_string(self.MENU_DATA)
        accel_group = ui_manager.get_accel_group()
        self.add_accel_group(accel_group)
        ui_manager.insert_action_group(action_group)
        
        # Create the grid for the UI and add the UI items.
        grid = Gtk.Grid()
        menubar = ui_manager.get_widget("/menubar")
        toolbar = ui_manager.get_widget("/toolbar")
        self.context_menu = ui_manager.get_widget("/context_menu")
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        scrolled_win.add(self.treeview)
        grid.add(menubar)
        grid.attach_next_to(toolbar, menubar, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(scrolled_win, toolbar, Gtk.PositionType.BOTTOM, 1, 1)
        self.add(grid)
        self.show_all()
        
        # Bind the events.
        self.connect("delete-event", self.delete_event)
        self.treeview.connect("button-press-event", self.context_event)
        self.treeview.connect("row-activated", self.activated_event)
        
        # Change the titles, if the user doesn't want units to be displayed.
        if not self.config["show_units"]:
            self.temp_col.set_title("Temperature")
            self.chil_col.set_title("Wind Chill")
            self.prec_col.set_title("Precipitation")
            self.wind_col.set_title("Wind")
            self.humi_col.set_title("Humidity")
            self.visi_col.set_title("Visibility")
            self.airp_col.set_title("Air Pressure")
    
    
    def delete_event(self, widget, event):
        """Saves the window size."""
        
        # Get the current window size.
        height, width = self.get_size()
        size = "%d\n%d" % (height, width)
        
        # Save the window size.
        io.write_standard_file("%s/window_size" % self.conf_dir, size)
    
    
    def context_event(self, widget, event):
        """Opens the context menu."""
        
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            self.context_menu.popup(None, None, None, None, event.button, event.time)
            return True
    
    
    def activated_event(self, widget, treepath, column):
		"""Opens the edit dialog on double click."""
		
		# Get the selected date and pass it to the edit function.
		tree_sel = self.treeview.get_selection()
		tm, ti = tree_sel.get_selected()
		date = tm.get_value(ti, 0)
		self.edit(None, date)
    
    
    def add_new(self, event, prefill_data = []):
        """Shows the dialog for input of new data."""
        
        # Get the data to add.
        new_dlg = AddNewDialog(self, self.last_profile, self.config["location"], self.config["pre-fill"], self.config["show_pre-fill"], self.units, prefill_data)
        response = new_dlg.run()
        date = new_dlg.date_ent.get_text()
        temp = new_dlg.temp_sbtn.get_value()
        chil = new_dlg.chil_sbtn.get_value()
        prec = new_dlg.prec_sbtn.get_value()
        prec_type = new_dlg.prec_com.get_active_text()
        wind = new_dlg.wind_sbtn.get_value()
        wind_dir = new_dlg.wind_com.get_active_text()
        humi = new_dlg.humi_sbtn.get_value()
        airp = new_dlg.airp_sbtn.get_value()
        airp_read = new_dlg.airp_com.get_active_text()
        clou = new_dlg.clou_com.get_active_text()
        ctyp = new_dlg.clou_com2.get_active_text()
        visi = new_dlg.visi_sbtn.get_value()
        note = new_dlg.note_buffer.get_text(new_dlg.note_buffer.get_start_iter(), new_dlg.note_buffer.get_end_iter(), True).strip()
        
        temp_unit = new_dlg.temp_unit.get_active_text()
        chil_unit = new_dlg.chil_unit.get_active_text()
        prec_unit = new_dlg.prec_unit.get_active_text()
        wind_unit = new_dlg.wind_unit.get_active_text()
        visi_unit = new_dlg.visi_unit.get_active_text()
        
        new_dlg.destroy()
        
        # If the user did not click OK, don't continue:
        if response != Gtk.ResponseType.OK:
            return
            
        # If the precipitation or wind are zero, set the appropriate type/direction to "None".
        if not prec:
            prec_type = "None"
        if not wind:
            wind_dir = "None"
        
        # If the date has already been entered, tell the user and prompt to continue.
        if date in datasets.get_column(self.data, 0):
            overwrite = show_question_dialog(self, "Add New Data", "The date %s has already been entered.\n\nOverwrite with new data?" % date)
            
            if overwrite == Gtk.ResponseType.OK:
                # Delete the existing data.
                index = datasets.get_column(self.data, 0).index(date)
                del self.data[index]
            else:
                return
            

        # Check that all fields are in the correct units, and convert if necessary.
        convert_check = [temp, chil, prec, wind, visi]
        convert_units = [temp_unit, chil_unit, prec_unit, wind_unit, visi_unit]
        (temp, chil, prec, wind, visi) = convert.new_convert(self.units, convert_check, convert_units)
        
        # Format the data and add it to the list.
        new_data = [date,
                    ("%.2f" % temp),
                    ("%.2f" % chil),
                    "%s%s" % ((("%.2f" % prec) + " " if prec_type != "None" else ""), prec_type),
                    "%s%s" % ((("%.2f" % wind) + " " if wind_dir != "None" else ""), wind_dir),
                    ("%.2f" % humi),
                    ("%.2f %s" % (airp, airp_read)),
                    ("%.2f" % visi),
                    "%s (%s)" % (clou, ctyp),
                    note]
        self.data.append(new_data)
        
        # Sort the list by date.
        self.data = sorted(self.data, key = lambda x: datetime.datetime.strptime(x[0], "%d/%m/%Y"))
        
        # Update the UI.
        self.update_list()
        
        # Update the title and save the data.
        self.update_title()
        self.save()
    
    
    def edit(self, event, edit_date = None):
        """Edits a row of data."""
        
        # Get the selected date.
        if edit_date != None:
            date = edit_date
        
        else:
	        try:
	            tree_sel = self.treeview.get_selection()
	            tm, ti = tree_sel.get_selected()
	            date = tm.get_value(ti, 0)
	        
	        except:
	            show_error_dialog(self, "Edit Data - %s" % last_profile, "No date selected.")
	            return
        
        # Get the index of the date.
        index = datasets.get_column(self.data, 0).index(date)
        
        # Get the new data.
        edit_dlg = EditDialog(self, self.last_profile, self.data[index], date, self.units)
        response = edit_dlg.run()
        temp = edit_dlg.temp_sbtn.get_value()
        chil = edit_dlg.chil_sbtn.get_value()
        prec = edit_dlg.prec_sbtn.get_value()
        prec_type = edit_dlg.prec_com.get_active_text()
        wind = edit_dlg.wind_sbtn.get_value()
        wind_dir = edit_dlg.wind_com.get_active_text()
        humi = edit_dlg.humi_sbtn.get_value()
        airp = edit_dlg.airp_sbtn.get_value()
        airp_read = edit_dlg.airp_com.get_active_text()
        clou = edit_dlg.clou_com.get_active_text()
        ctyp = edit_dlg.clou_com2.get_active_text()
        visi = edit_dlg.visi_sbtn.get_value()
        note = edit_dlg.note_buffer.get_text(edit_dlg.note_buffer.get_start_iter(), edit_dlg.note_buffer.get_end_iter(), True).strip()
        
        temp_unit = edit_dlg.temp_unit.get_active_text()
        chil_unit = edit_dlg.chil_unit.get_active_text()
        prec_unit = edit_dlg.prec_unit.get_active_text()
        wind_unit = edit_dlg.wind_unit.get_active_text()
        visi_unit = edit_dlg.visi_unit.get_active_text()
        
        edit_dlg.destroy()
        
        # If the user did not click OK, don't continue.
        if response != Gtk.ResponseType.OK:
            return
        
        # If the precipitation or wind are zero, set the appropriate type/direction to "None".
        if not prec:
            prec_type = "None"
        if not wind:
            wind_dir = "None"
        
        # Check that all fields are in the correct units, and convert if necessary.
        convert_check = [temp, chil, prec, wind, visi]
        convert_units = [temp_unit, chil_unit, prec_unit, wind_unit, visi_unit]
        (temp, chil, prec, wind, visi) = convert.new_convert(self.units, convert_check, convert_units)
        
        # Create and store the edited list of data.
        new_data = [date,
                    ("%.2f" % temp),
                    ("%.2f" % chil),
                    "%s%s" % ((("%.2f" % prec) + " " if prec_type != "None" else ""), prec_type),
                    "%s%s" % ((("%.2f" % wind) + " " if wind_dir != "None" else ""), wind_dir),
                    ("%.2f" % humi),
                    ("%.2f %s" % (airp, airp_read)),
                    ("%.2f" % visi),
                    "%s (%s)" % (clou, ctyp),
                    note]
        self.data[index] = new_data
        
        # Update the UI.
        self.update_list()
        
        # Save the data.
        self.save()
    
    
    def remove(self, event):
        """Removes a row of data from the list."""
        
        # Get the dates.
        dates = []
        for i in self.data:
            dates.append([i[0]])
        
        # Get the dates to remove.
        rem_dlg = DateSelectionDialog(self, "Remove Data - %s" % self.last_profile, dates)
        response = rem_dlg.run()
        model, treeiter = rem_dlg.treeview.get_selection().get_selected_rows()
        rem_dlg.destroy()
        
        # If the user did not click OK or nothing was selected, don't continue.
        if response != Gtk.ResponseType.OK or treeiter == None:
            return
        
        # Get the dates.
        ndates = []
        for i in treeiter:
            ndates.append(model[i][0])
        
        # If there is no data, don't continue.
        if len(ndates) == 0:
            return
        
        # Only show the confirmation dialog if the user wants that.
        if self.config["confirm_del"]:
            
            # Confirm that the user wants to delete the row.
            response = show_question_dialog(self, "Remove Data - %s" % self.last_profile, "Are you sure you want to delete the selected date%s?\n\nThis action cannot be undone." % ("s" if len(ndates) > 1 else ""))
            if response != Gtk.ResponseType.OK:
                return
        
        # Loop through the list of dates and delete them.
        for i in ndates:
            index = datasets.get_column(self.data, 0).index(i)
            del self.data[index]
        
        # Update the UI.
        self.update_list()
        
        # Update the title and save the data.
        self.update_title()
        self.save()
    
    
    def get_weather(self, here):
        """Gets the current weather."""
        
        location = ""
        
        # If getting the weather for the current location, make sure this
        # location has been specified.
        if here and len(self.config["location"]) == 5:
            location = self.config["location"]
        
        if not here or not location:
            
            # Get the location.
            loc_dlg = LocationDialog(self, "Enter location: ")
            response = loc_dlg.run()
            location = loc_dlg.loc_ent.get_text().lstrip().rstrip()
            loc_dlg.destroy()
            
            if response != Gtk.ResponseType.OK:
                return
        
        # Make sure the location is valid.
        if not location or len(location) != 5 or not location.isdigit():
            show_error_dialog(self, "Get Current Weather", "The specified location is not valid. Only 5-digit US zipcodes are currently supported.")
            return
        
        # Get the weather data.
        city, data, prefill_data = get_weather.get_weather(location, self.config, self.units, self.weather_codes)
        
        # Show the current weather.
        info_dlg = CurrentWeatherDialog(self, "Current Weather For %s" % city, data)
        response = info_dlg.run()
        
        # Close the dialog.
        info_dlg.destroy()
        
        # If the user clicked Export:
        if response == DialogResponse.EXPORT:
            
            # Get the filename.
            response2, filename = show_export_dialog(self, "Export Weather For %s" % city)
            
            # Export the info.
            if response2 == Gtk.ResponseType.OK:
                export.html_generic([["Weather", ["Field", "Value"], data[0]],
                                     ["Location", ["Field", "Value"], data[1]],
                                     ["Forecast", ["Field", "Value"], data[2]]], filename)
        
        # If the user clicked Add:
        elif response == DialogResponse.ADD_DATA:
            
            self.add_new(False, prefill_data)
            
    
    def info_range(self):
        """Gets the range for the info to display."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(self.data) == 0:
            show_no_data_dialog(self, "Info - %s" % self.last_profile)
            return
        
        # Get the first and last entered dates.
        day_start = dates.split_date(self.data[0][0])
        day_end = dates.split_date(self.data[len(self.data) - 1][0])
        
        # Get a list of datetimes from the dates.
        datelist = dates.date_list_datetime(datasets.get_column(self.data, 0))
        
        # Get the starting and ending dates.
        cal_dlg = CalendarRangeDialog(self, "Info in Range - %s" % self.last_profile, day_start, day_end)
        response = cal_dlg.run()
        year1, month1, day1 = cal_dlg.start_cal.get_date()
        year2, month2, day2 = cal_dlg.end_cal.get_date()
        date1 = "%d/%d/%d" % (day1, month1 + 1, year1)
        date2 = "%d/%d/%d" % (day2, month2 + 1, year2)
        cal_dlg.destroy()
        
        # If the user did not click OK, don't continue.
        if response != Gtk.ResponseType.OK:
            return
        
        # Get the indices.
        dt_start = datetime.datetime(year1, month1 + 1, day1)
        start_index = dates.date_above(dt_start, datelist)
        dt_end = datetime.datetime(year2, month2 + 1, day2)
        end_index = dates.date_below(dt_end, datelist)
        
        # Check to make sure these dates are valid, and cancel the action if not.
        if start_index == -1:
            show_error_dialog(self, "Info in Range - %s" % self.last_profile, "%s is not a valid date.\n\nThis date is not present and is not before any other dates." % date1)
            return
        if end_index == -1:
            show_error_dialog(self, "Info in Range - %s" % self.last_profile, "%s is not a valid date.\n\nThis date is not present and is not after any other dates." % date2)
            return
        if end_index < start_index:
            show_error_dialog(self, "Info in Range - %s" % self.last_profile, "The ending date must be after the starting date.")
            return
        
        # Get the new list.
        data2 = self.data[start_index:end_index + 1]
        
        # Pass the data to the info dialog.
        self.show_info_generic(data = data2)
    
    
    def info_selected(self):
        """Gets the selected dates to for the info to display."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(self.data) == 0:
            show_no_data_dialog(self, "Info - %s" % self.last_profile)
            return
        
        # Get the dates.
        dates = []
        for i in self.data:
            dates.append([i[0]])
        
        # Get the selected dates.
        info_dlg = DateSelectionDialog(self, "Info for Selected Dates - %s" % self.last_profile, dates)
        response = info_dlg.run()
        model, treeiter = info_dlg.treeview.get_selection().get_selected_rows()
        info_dlg.destroy()
        
        # If the user did not click OK or nothing was selected, don't continue.
        if response != Gtk.ResponseType.OK or treeiter == None:
            return
        
        # Get the dates.
        ndates = []
        for i in treeiter:
            ndates.append(model[i][0])
        
        # Get the data.
        ndata = []
        for i in range(0, len(self.data)):
            if self.data[i][0] in ndates:
                ndata.append(self.data[i])
        
        # If there is no data, don't continue.
        if len(ndata) == 0:
            return
        
        # Pass the data to the info dialog.
        self.show_info_generic(data = ndata)
    
    
    def show_info_generic(self, data = False):
        """Shows info about the data."""
        
        if data == False:
            data = self.data
        
        # If there is no data, tell the user and don't show the dialog.
        if len(data) == 0:
            show_no_data_dialog(self, "Info - %s" % self.last_profile)
            return
        
        # Get the info.
        data2 = [
            info.general_info(data, self.units),
            info.temp_info(data, self.units),
            info.chil_info(data, self.units),
            info.prec_info(data, self.units),
            info.wind_info(data, self.units),
            info.humi_info(data, self.units),
            info.airp_info(data, self.units),
            info.visi_info(data, self.units),
            info.clou_info(data, self.units),
            info.note_info(data, self.units)
        ]
        
        # Show the info.
        info_dlg = GenericInfoDialog(self, "Info - %s" % self.last_profile, data2)
        response = info_dlg.run()
        
        # If the user clicked Export:
        if response == DialogResponse.EXPORT:
            
            # Get the filename.
            response2, filename = show_export_dialog(self, "Export Info - %s" % self.last_profile)
            
            # Export the info.
            if response2 == Gtk.ResponseType.OK:
                export.html_generic([["General Info", ["Field", "Value"], data2[0]],
                                     ["Temperature Info", ["Field", "Value"], data2[1]],
                                     ["Wind Chill Info", ["Field", "Value"], data2[2]],
                                     ["Precipitation Info", ["Field", "Value"], data2[3]],
                                     ["Wind Info", ["Field", "Value"], data2[4]],
                                     ["Humidity Info", ["Field", "Value"], data2[5]],
                                     ["Air Pressure Info", ["Field", "Value"], data2[6]],
                                     ["Visibility Info", ["Field", "Value"], data2[7]],
                                     ["Cloud Cover Info", ["Field", "Value"], data2[8]],
                                     ["Notes Info", ["Field", "Value"], data2[9]]], filename)
        
        # Close the dialog.
        info_dlg.destroy()
        
    
    def chart_range(self):
        """Gets the range for the chart to display."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(self.data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Charts - %s" % self.last_profile)
            return
        
        # Get the first and last entered dates.
        day_start = dates.split_date(self.data[0][0])
        day_end = dates.split_date(self.data[len(self.data) - 1][0])
        
        # Get a list of datetimes from the dates.
        datelist = dates.date_list_datetime(datasets.get_column(self.data, 0))
        
        # Get the starting and ending dates.
        cal_dlg = CalendarRangeDialog(self, "Charts in Range - %s" % self.last_profile, day_start, day_end)
        response = cal_dlg.run()
        year1, month1, day1 = cal_dlg.start_cal.get_date()
        year2, month2, day2 = cal_dlg.end_cal.get_date()
        date1 = "%d/%d/%d" % (day1, month1 + 1, year1)
        date2 = "%d/%d/%d" % (day2, month2 + 1, year2)
        cal_dlg.destroy()
        
        # If the user did not click OK, don't continue.
        if response != Gtk.ResponseType.OK:
            return
        
        # Get the indices.
        dt_start = datetime.datetime(year1, month1 + 1, day1)
        start_index = dates.date_above(dt_start, datelist)
        dt_end = datetime.datetime(year2, month2 + 1, day2)
        end_index = dates.date_below(dt_end, datelist)
        
        # Check to make sure these dates are valid, and cancel the action if not.
        if start_index == -1:
            show_error_dialog(self, "Charts in Range - %s" % self.last_profile, "%s is not a valid date.\n\nThis date is not present and is not before any other dates." % date1)
            return
        if end_index == -1:
            show_error_dialog(self, "Charts in Range - %s" % self.last_profile, "%s is not a valid date.\n\nThis date is not present and is not after any other dates." % date2)
            return
        if end_index < start_index:
            show_error_dialog(self, "Charts in Range - %s" % self.last_profile, "The ending date must be after the starting date.")
            return
        
        # Get the new list.
        data2 = self.data[start_index:end_index + 1]
        
        # Pass the data to the charts dialog.
        self.show_chart_generic(data = data2)
    
    
    def chart_selected(self):
        """Gets the selected dates to for the charts to display."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(self.data) == 0:
            show_no_data_dialog(self, "Charts - %s" % self.last_profile)
            return
        
        # Get the dates.
        dates = []
        for i in self.data:
            dates.append([i[0]])
        
        # Get the selected dates.
        info_dlg = DateSelectionDialog(self, "Charts for Selected Dates - %s" % self.last_profile, dates)
        response = info_dlg.run()
        model, treeiter = info_dlg.treeview.get_selection().get_selected_rows()
        info_dlg.destroy()
        
        # If the user did not click OK or nothing was selected, don't continue.
        if response != Gtk.ResponseType.OK or treeiter == None:
            return
        
        # Get the dates.
        ndates = []
        for i in treeiter:
            ndates.append(model[i][0])
        
        # Get the data.
        ndata = []
        for i in range(0, len(self.data)):
            if self.data[i][0] in ndates:
                ndata.append(self.data[i])
        
        # If there is no data, don't continue.
        if len(ndata) == 0:
            return
        
        # Pass the data to the charts dialog.
        self.show_chart_generic(data = ndata)
    
    
    def show_chart_generic(self, data = False):
        """Shows a chart about the data."""
        
        if data == False:
            data = self.data
        
        # If there is no data, tell the user and don't show the chart dialog.
        if len(data) == 0:
            show_no_data_dialog(self, "Charts - %s" % self.last_profile)
            return
        
        # Get the chart data.
        data2 = [
            charts.temp_chart(data, self.units),
            charts.chil_chart(data, self.units),
            charts.prec_chart(data, self.units),
            charts.wind_chart(data, self.units),
            charts.humi_chart(data, self.units),
            charts.airp_chart(data, self.units),
            charts.visi_chart(data, self.units)
        ]
        
        # Show the chart.
        chart_dlg = GenericChartDialog(self, "Charts - %s" % self.last_profile, data2)
        response = chart_dlg.run()
        
        # If the user clicked Export:
        if response == DialogResponse.EXPORT:
            
            # Get the filename.
            response2, filename = show_export_dialog(self, "Export Charts - %s" % self.last_profile)
            
            # Export the info.
            if response2 == Gtk.ResponseType.OK:
                chart_columns = ["Day", "Value", "Average Difference", "Low Difference", "High Difference", "Median Difference"]
                export.html_generic([["Temperature Chart", chart_columns, data2[0]],
                                     ["Wind Chill Chart", chart_columns, data2[1]],
                                     ["Precipitation Chart", chart_columns, data2[2]],
                                     ["Wind Chart", chart_columns, data2[3]],
                                     ["Humidity Chart", chart_columns, data2[4]],
                                     ["Air Pressure Chart", chart_columns, data2[5]],
                                     ["Visibility Chart", chart_columns, data2[6]]], filename)
        
        # Close the dialog.
        chart_dlg.destroy()
    
    
    def graph_range(self):
        """Gets the range for the graph to display."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(self.data) == 0:
            
            # Show the dialog.
            show_no_data_dialog(self, "Graphs - %s" % self.last_profile)
            return
        
        # Get the first and last entered dates.
        day_start = dates.split_date(self.data[0][0])
        day_end = dates.split_date(self.data[len(self.data) - 1][0])
        
        # Get a list of datetimes from the dates.
        datelist = dates.date_list_datetime(datasets.get_column(self.data, 0))
        
        # Get the starting and ending dates.
        cal_dlg = CalendarRangeDialog(self, "Graphs in Range - %s" % self.last_profile, day_start, day_end)
        response = cal_dlg.run()
        year1, month1, day1 = cal_dlg.start_cal.get_date()
        year2, month2, day2 = cal_dlg.end_cal.get_date()
        date1 = "%d/%d/%d" % (day1, month1 + 1, year1)
        date2 = "%d/%d/%d" % (day2, month2 + 1, year2)
        cal_dlg.destroy()
        
        # If the user did not click OK, don't continue.
        if response != Gtk.ResponseType.OK:
            return
        
        # Get the indices.
        dt_start = datetime.datetime(year1, month1 + 1, day1)
        start_index = dates.date_above(dt_start, datelist)
        dt_end = datetime.datetime(year2, month2 + 1, day2)
        end_index = dates.date_below(dt_end, datelist)
        
        # Check to make sure these dates are valid, and cancel the action if not.
        if start_index == -1:
            show_error_dialog(self, "Graphs in Range - %s" % self.last_profile, "%s is not a valid date.\n\nThis date is not present and is not before any other dates." % date1)
            return
        if end_index == -1:
            show_error_dialog(self, "Graphs in Range - %s" % self.last_profile, "%s is not a valid date.\n\nThis date is not present and is not after any other dates." % date2)
            return
        if end_index < start_index:
            show_error_dialog(self, "Graphs in Range - %s" % self.last_profile, "The ending date must be after the starting date.")
            return
        
        # Get the new list.
        data2 = self.data[start_index:end_index + 1]
        
        # Pass the data to the charts dialog.
        self.show_graph_generic(data = data2)
    
    
    def graph_selected(self):
        """Gets the selected dates to for the graphs to display."""
        
        # If there is no data, tell the user and don't show the info dialog.
        if len(self.data) == 0:
            show_no_data_dialog(self, "Graphs - %s" % self.last_profile)
            return
        
        # Get the dates.
        dates = []
        for i in self.data:
            dates.append([i[0]])
        
        # Get the selected dates.
        info_dlg = DateSelectionDialog(self, "Graphs for Selected Dates - %s" % self.last_profile, dates)
        response = info_dlg.run()
        model, treeiter = info_dlg.treeview.get_selection().get_selected_rows()
        info_dlg.destroy()
        
        # If the user did not click OK or nothing was selected, don't continue.
        if response != Gtk.ResponseType.OK or treeiter == None:
            return
        
        # Get the dates.
        ndates = []
        for i in treeiter:
            ndates.append(model[i][0])
        
        # Get the data.
        ndata = []
        for i in range(0, len(self.data)):
            if self.data[i][0] in ndates:
                ndata.append(self.data[i])
        
        # If there is no data, don't continue.
        if len(ndata) == 0:
            return
        
        # Pass the data to the charts dialog.
        self.show_graph_generic(data = ndata)
    
    
    def show_graph_generic(self, data = False):
        """Shows graphs of the data."""
        
        if data == False:
            data = self.data
        
        # If matplotlib isn't installed, don't continue.
        if not self.matplotlib_installed:
            show_alert_dialog(self, "Graphs - %s" % self.last_profile, "The matplotlib library must be installed to view graphs.\n\nIn most Linux distributions this module can be found using a package manager. Source code and Windows downloads can also be found at http://matplotlib.org/")
            return
        
        # Get the data for the graphs.
        data2 = graphs.get_data(data)
        
        # Show the graph.
        graph_dlg = GenericGraphDialog(self, "Graphs - %s" % self.last_profile, data2, self.last_profile, self.units, self.config)
        response = graph_dlg.run()
        graph_dlg.destroy()
    
    
    def select_data_subset(self, event):
        """Shows the data selection dialog."""
        
        # Show the condition selection dialog.
        sel_dlg = DataSubsetSelectionDialog(self, self.last_profile, self.data, self.config, self.units)
    
    
    def import_file(self, event):
        """Imports data from a file."""
        
        validate_desc = {1: "No error, this should never display.",
                         0: "Data is not a list.",
                         -1: "One or more items in the data are not lists.",
                         -2: "One or more lists do not have the correct length.",
                         -3: "One or more data fields are not strings."}
        
        # Get the filename.
        response, filename = show_file_dialog(self, "Import - %s" % self.last_profile)
        
        # If the user did not click OK, don't continue.
        if response != Gtk.ResponseType.OK:
            return
            
        # Confirm that the user wants to overwrite the data, if the current profile isn't blank.
        if len(self.data) > 0:
            response2 = show_question_dialog(self, "Import - %s" % self.last_profile, "Are you sure you want to import the data?\n\nAll current data will be overwritten.")
            if response2 != Gtk.ResponseType.OK:
                return
        
        # Read and add the data.
        ndata = io.read_profile(filename = filename)
        
        # If the imported data is empty or invalid, don't continue.
        if len(ndata) == 0:
            show_alert_dialog(self, "Import - %s" % self.last_profile, "The selected file contains no data to import.")
            return
        validate_error = validate.validate_data(ndata)
        if validate_error != 1:
            show_error_dialog(self, "Import - %s" % self.last_profile, "The data in the selected file is not valid. %s" % validate_desc[validate_error])
            return
        
        # Ask the user what dates they want to import.
        if not self.config["import_all"]:
            date_dlg = ImportSelectionDialog(self, "Import - %s" % self.last_profile, datasets.get_column(ndata, 0))
            response = date_dlg.run()
            model, treeiter = date_dlg.treeview.get_selection().get_selected_rows()
            date_dlg.destroy()
        
        else:
            response = DialogResponse.IMPORT_ALL
        
        # If the user did not press OK or nothing was selected, don't continue:
        if response != DialogResponse.IMPORT_ALL and response != DialogResponse.IMPORT:
            return
        if response == DialogResponse.IMPORT and treeiter == None:
            return
        
        # Clear the data.
        self.data[:] = []
        self.liststore.clear()
        
        # If the user selected certain dates, only import those.
        if response == DialogResponse.IMPORT:
            
            # Get the dates.
            dates = []
            for i in treeiter:
                dates.append(model[i][0])
            
            # Get the new data list.
            for i in ndata:
                if i[0] in dates:
                    self.data.append(i)
        
        # If the user pressed Import All, import all of the data.
        if response == DialogResponse.IMPORT_ALL:
            self.data = ndata[:]
        
        # Add the data.
        self.update_list()
        
        # Update the title and save the data.
        self.update_title()
        self.save()
    
    
    def import_merge(self, event):
        """Imports data and merges it into the current list."""
        
        validate_desc = {1: "No error, this should never display.",
                         0: "Data is not a list.",
                         -1: "One or more items in the data are not lists.",
                         -2: "One or more lists do not have the correct length.",
                         -3: "One or more data fields are not strings."}
        
        # Get the filename.
        response, filename = show_file_dialog(self, "Import and Merge - %s" % self.last_profile)
        
        # If the user did not click OK, don't continue.
        if response != Gtk.ResponseType.OK:
            return
            
        # Read the data.
        data2 = io.read_profile(filename = filename)
        
        # If the imported data is empty or invalid, don't continue.
        if len(data2) == 0:
            show_alert_dialog(self, "Import and Merge - %s" % self.last_profile, "The selected file contains no data to import.")
            return
        validate_error = validate.validate_data(data2)
        if validate_error != 1:
            show_error_dialog(self, "Import and Merge - %s" % self.last_profile, "The data in the selected file is not valid. %s" % validate_desc[validate_error])
            return
        
        # Ask the user what dates they want to import.
        if not self.config["import_all"]:
            date_dlg = ImportSelectionDialog(self, "Import and Merge - %s" % self.last_profile, datasets.get_column(data2, 0))
            response = date_dlg.run()
            model, treeiter = date_dlg.treeview.get_selection().get_selected_rows()
            date_dlg.destroy()
        
        else:
            response = DialogResponse.IMPORT_ALL
        
        # If the user did not press OK or nothing was selected, don't continue:
        if response != DialogResponse.IMPORT_ALL and response != DialogResponse.IMPORT:
            return
        if response == DialogResponse.IMPORT and treeiter == None:
            return
        
        # If the user selected certain dates, only import those.
        if response == DialogResponse.IMPORT:
            
            # Get the dates.
            dates = []
            for i in treeiter:
                dates.append(model[i][0])
            
            # Get the new data list.
            data3 = []
            for i in data2:
                if i[0] in dates:
                    data3.append(i)
        
        # If the user pressed Import All, import all of the data.
        if response == DialogResponse.IMPORT_ALL:
            data3 = data2[:]
        
        # Filter the new data to make sure there are no duplicates.
        new_data = []
        date_col = datasets.get_column(self.data, 0)
        for i in data3:
            
            # If the date already appears, don't include it.
            if i[0] not in date_col:
                new_data.append(i)
        
        # Append, sort, and add the data.
        self.data += new_data
        self.data = sorted(self.data, key = lambda x: datetime.datetime.strptime(x[0], "%d/%m/%Y"))
        self.update_list()
        
        # Update the title and save the data.
        self.update_title()
        self.save()      
    
    
    def import_new_dataset(self, event):
        """Imports data from a file and inserts it in a new profile."""
        
        validate_desc = {1: "No error, this should never display.",
                         0: "Data is not a list.",
                         -1: "One or more items in the data are not lists.",
                         -2: "One or more lists do not have the correct length.",
                         -3: "One or more data fields are not strings."}
        
        # Get the new profile name.
        new_dlg = DatasetNameDialog(self, "Import as New Dataset")
        response = new_dlg.run()
        name = new_dlg.nam_ent.get_text().lstrip().rstrip()
        new_dlg.destroy()
        
        # If the user did not press OK, don't continue.
        if response != Gtk.ResponseType.OK:
            return
            
        # Validate the name. If it contains a non-alphanumeric character or is just space,
        # show a dialog and cancel the action.
        valid = validate.validate_profile(self.main_dir, name)
        if valid != "":
            show_error_dialog(self, "Import as New Dataset", valid)
            return

        # Get the filename.
        response, filename = show_file_dialog(self, "Import as New Dataset - %s" % name)
        
        # If the user did not press OK, don't continue.
        if response != Gtk.ResponseType.OK:
            return
        
        # Read and add the data.
        ndata = io.read_profile(filename = filename)
        
        # If the imported data is empty or invalid, don't continue.
        if len(ndata) == 0:
            show_alert_dialog(self, "Import as New Dataset - %s" % name, "The selected file contains no data to import.")
            return
        validate_error = validate.validate_data(ndata)
        if validate_error != 1:
            show_error_dialog(self, "Import as New Dataset - %s" % name, "The data in the selected file is not valid. %s" % validate_desc[validate_error])
            return
        
        # Ask the user what dates they want to import.
        if not self.config["import_all"]:
            date_dlg = ImportSelectionDialog(self, "Import as New Profile - %s" % name, datasets.get_column(ndata, 0))
            response = date_dlg.run()
            model, treeiter = date_dlg.treeview.get_selection().get_selected_rows()
            date_dlg.destroy()
        
        else:
            response = DialogResponse.IMPORT_ALL
        
        # If the user did not press OK or nothing was selected, don't continue:
        if response != DialogResponse.IMPORT_ALL and response != DialogResponse.IMPORT:
            return
        if response == DialogResponse.IMPORT and treeiter == None:
            return
            
        # Create the dataset directory and file.
        self.last_profile = name
        io.write_blank_profile(self.main_dir, name)
        
        # Clear the data.
        self.data[:] = []
        self.liststore.clear()
        
        # If the user selected certain dates, only import those.
        if response == DialogResponse.IMPORT:
            
            # Get the dates.
            dates = []
            for i in treeiter:
                dates.append(model[i][0])
            
            # Get the new data list.
            for i in ndata:
                if i[0] in dates:
                    self.data.append(i)
        
        # If the user pressed Import All, import all of the data.
        if response == DialogResponse.IMPORT_ALL:
            self.data = ndata[:]
        
        # Add the data.
        self.update_list()
        
        # Update the title and save the data.
        self.update_title()
        self.save()
    
    
    def export_file(self, event):
        """Exports the data to a file."""
        
        # If there is no data, tell the user and cancel the action.
        if len(self.data) == 0:
            show_alert_dialog(self, "Export - %s" % self.last_profile, "There is no data to export.")
            return
        
        # Get the filename.
        response, filename = show_save_dialog(self, "Export - %s" % self.last_profile)
        
        # If the user did not press OK, don't continue.
        if response != Gtk.ResponseType.OK and response != DialogResponse.EXPORT_CSV and response != DialogResponse.EXPORT_HTML:
            return
        
        # Error checking for when the HTML and CSV options are chosen. GTK will allow these
        # to be clicked when no filename has been entered, causing an error. Check to make sure
        # there was a filename to work around this.
        if (response == DialogResponse.EXPORT_CSV or response == DialogResponse.EXPORT_HTML) and not filename:
            return
        
        # Export the data.
        if response == Gtk.ResponseType.OK:
            io.write_profile(filename = filename, data = self.data)
        elif response == DialogResponse.EXPORT_CSV:
            export.csv(self.data, self.units, filename)
        elif response == DialogResponse.EXPORT_HTML:
            data_list = [["WeatherLog Data - %s - %s to %s" % (self.last_profile, (self.data[0][0] if len(self.data) != 0 else "None"), (self.data[len(self.data)-1][0] if len(self.data) != 0 else "None")),
                           ["Date", "Temperature (%s)" % self.units["temp"], "Wind Chill (%s)" % self.units["temp"],
                            "Precipitation (%s)" % self.units["prec"], "Wind (%s)" % self.units["wind"],
                            "Humidity (%%)", "Air Pressure (%s)" % self.units["airp"], "Visibility (%s)" % self.units["visi"],
                            "Cloud Cover", "Notes"],
                            data]]
            export.html_generic(data_list, filename)
    
    
    def export_pastebin(self, event):
        """Exports the data to Pastebin."""
        
        # If there is no data, tell the user and cancel the action.
        if len(self.data) == 0:
            show_alert_dialog(self, "Export to Pastebin - %s" % self.last_profile, "There is no data to export.")
            return
        
        # Show the dialog and get the user's response.
        pas_dlg = ExportPastebinDialog(self, "Export to Pastebin - %s" % self.last_profile)
        response = pas_dlg.run()
        name = pas_dlg.nam_ent.get_text()
        mode = pas_dlg.for_com.get_active_text().lower()
        pas_dlg.destroy()
        
        # If the user didn't click OK, don't continue.
        if response != Gtk.ResponseType.OK:
            return
        
        # Convert the data.
        if mode == "html":
            new_data = export.html(self.data, self.units)
        elif mode == "csv":
            new_data = export.csv(self.data, self.units)
        elif mode == "json":
            new_data = json.dumps(self.data)
        
        # Build the api string.
        api = {"api_option": "paste",
               "api_dev_key": self.config["pastebin"],
               "api_paste_code": new_data}
        if mode == "html":
            api["api_paste_format"] = "html5"
        elif mode == "raw":
            api["api_paste_format"] = "javascript"
        if name.lstrip().rstrip() != "":
            api["api_paste_name"] = name.lstrip().rstrip()
        
        # Upload the text.
        try:
            pastebin = urlopen("http://pastebin.com/api/api_post.php", urlencode(api))
            result = pastebin.read()
            pastebin.close()
            
            # Tell the user the URL.
            show_alert_dialog(self, "Export to Pastebin - %s" % self.last_profile, "The data has been uploaded to Pastebin, and can be accessed at the following URL:\n\n%s" % result)
            
        except:
            show_error_dialog(self, "Export to Pastebin - %s" % self.last_profile, "The data could not be uploaded to Pastebin.")
    
    
    def clear(self, event):
        """Clears the data."""
        
        # Only show the dialog if the user wants that.
        if self.config["confirm_del"]:
            response = show_question_dialog(self, "Clear Current Data - %s" % self.last_profile, "Are you sure you want to clear the data?\n\nThis action cannot be undone.")
            if response != Gtk.ResponseType.OK:
                return
        
        # Clear the data.
        self.data[:] = []
        self.liststore.clear()
        
        # Update the title and save the data.
        self.update_title()
        self.save()
        
    
    def clear_all(self, event):
        """Clears all data."""
        
        # Only show the confirmation dialog if the user wants that.
        if self.config["confirm_del"]:
            response = show_question_dialog(self, "Clear All Data", "Are you sure you want to clear all the data?\n\nThis action cannot be undone.")
            if response != Gtk.ResponseType.OK:
                return

        # Clear the old data and reset the profile name.
        self.data[:] = []
        self.liststore.clear()
        self.last_profile = "Main Dataset"
        
        # Restore all files to their default states.
        shutil.rmtree(self.main_dir)
        shutil.rmtree(self.conf_dir)
        launch.check_files_exist(self.main_dir, self.conf_dir)
        
        # Set the default config.
        self.config = {"pre-fill": False,
                  "restore": True,
                  "location": "",
                  "units": "metric",
                  "pastebin": "d2314ff616133e54f728918b8af1500e",
                  "show_units": True,
                  "show_dates": True,
                  "confirm_del": True,
                  "show_pre-fill": True,
                  "confirm_exit": False,
                  "import_all": False}
        
        # Configure the units.
        self.units = launch.get_units(config)
        
        # Update the main window.
        self.temp_col.set_title("Temperature (%s)" % self.units["temp"])
        self.chil_col.set_title("Wind Chill (%s)" % self.units["temp"])
        self.prec_col.set_title("Precipitation (%s)" % self.units["prec"])
        self.wind_col.set_title("Wind (%s)" % self.units["wind"])
        self.humi_col.set_title("Humidity (%)")
        self.visi_col.set_title("Visibility (%s)" % self.units["visi"])
        self.airp_col.set_title("Air Pressure (%s)" % self.units["airp"])
        
        # Update the title and save the data.
        self.update_title()
        self.save(from_options = True)
    
    
    def switch_dataset(self, event):
        """Switches profiles."""
        
        # Get the list of profiles
        profiles = io.get_profile_list(self.main_dir, self.last_profile)
        
        # If there are no other profiles, cancel the action.
        if len(profiles) == 0:
            show_alert_dialog(self, "Switch Dataset", "There are no other datasets.")
            return
        
        # Get the profile to switch to.
        swi_dlg = DatasetSelectionDialog(self, "Switch Dataset", profiles)
        response = swi_dlg.run()
        model, treeiter = swi_dlg.treeview.get_selection().get_selected()
        swi_dlg.destroy()
        
        # If the user did not press OK or nothing was selected, don't continue:
        if response != Gtk.ResponseType.OK or treeiter == None:
            return
        
        # Get the profile name and clear the old data.
        name = model[treeiter][0]
        self.data[:] = []
        self.liststore.clear()
        
        # Read the data and switch to the other profile.
        self.data = io.read_profile(main_dir = self.main_dir, name = name)
        self.last_profile = name
        self.update_list()
        
        # Update the title and save the data.
        self.update_title()
        self.save()
    
    
    def add_dataset(self, event):
        """Adds a new dataset."""
        
        # Get the name for the new profile.
        new_dlg = DatasetNameDialog(self, "Add Dataset")
        response = new_dlg.run()
        name = new_dlg.nam_ent.get_text().lstrip().rstrip()
        new_dlg.destroy()
        
        # If the user did not press OK, don't continue:
        if response != Gtk.ResponseType.OK:
            return
        
        # Validate the name. If the name isn't valid, don't continue.
        valid = validate.validate_profile(self.main_dir, name)
        if valid.endswith("\".\")."):
            show_error_dialog(self, "Add Dataset", valid)
            return
        
        # If the name is already in use, ask the user is they want to delete the old profile.
        elif valid.endswith("already in use."):
            del_old = show_question_dialog(self, "Add Dataset", "%s\n\nWould you like to delete the existing dataset?" % valid)
            if del_old != Gtk.ResponseType.OK:
                return
            
            # Delete the existing profile.
            shutil.rmtree("%s/profiles/%s" % (self.main_dir, name))
        
        # Create the new profile and clear the old data.
        io.write_blank_profile(self.main_dir, name)
        launch.create_metadata(self.main_dir, name)
        self.last_profile = name
        self.data[:] = []
        self.liststore.clear()
        
        # Update the title.
        self.save()
        self.update_title()
    
    
    def remove_dataset(self, event):
        """Removes a dataset."""
        
        # Get the list of profiles.
        profiles = io.get_profile_list(self.main_dir, self.last_profile)
        
        # If there are no other profiles, cancel the action.
        if len(profiles) == 0:
            show_alert_dialog(self, "Remove Datasets", "There are no other datasets.")
            return
        
        # Get the profiles to remove.
        rem_dlg = DatasetSelectionDialog(self, "Remove Datasets", profiles, select_mode = "multiple")
        response = rem_dlg.run()
        model, treeiter = rem_dlg.treeview.get_selection().get_selected_rows()
        rem_dlg.destroy()
        
        # If the user did not press OK or nothing was selected, don't continue:
        if response != Gtk.ResponseType.OK or treeiter == None:
            return
        
        # Get the profiles.
        profiles = []
        for i in treeiter:
            profiles.append(model[i][0])
        
        # Only show the confirmation dialog if the user wants that.
        if self.config["confirm_del"]:
            response = show_question_dialog(self, "Remove Datasets", "Are you sure you want to remove the dataset%s?\n\nThis action cannot be undone." % ("" if len(profiles) == 1 else "s"))
            if response != Gtk.ResponseType.OK:
                return
        
        # Delete the selected profiles.
        for name in profiles:
            shutil.rmtree("%s/profiles/%s" % (self.main_dir, name))
    
    
    def rename_dataset(self, event):
        """Renames the current dataset."""
        
        # Get the new profile name.
        ren_dlg = DatasetNameDialog(self, "Rename Current Dataset")
        response = ren_dlg.run()
        name = ren_dlg.nam_ent.get_text().lstrip().rstrip()
        ren_dlg.destroy()
        
        # If the user did not press OK, don't continue:
        if response != Gtk.ResponseType.OK:
            return
        
        # Validate the name. If the name isn't valid, don't continue.
        valid = validate.validate_profile(self.main_dir, name)
        if valid.endswith("\".\")."):
            show_error_dialog(self, "Rename Current Dataset", valid)
            return
        
        # If the name is already in use, ask the user is they want to delete the old profile.
        elif valid.endswith("already in use."):
            del_old = show_question_dialog(self, "Rename Current Dataset", "%s\n\nWould you like to delete the existing dataset?" % valid)
            if del_old != Gtk.ResponseType.OK:
                return
            
            # Delete the existing profile.
            shutil.rmtree("%s/profiles/%s" % (self.main_dir, name))
            
        # Rename the directory.
        os.rename("%s/profiles/%s" % (self.main_dir, self.last_profile), "%s/profiles/%s" % (self.main_dir, name))
        now = datetime.datetime.now()
        modified = "%d/%d/%d" % (now.day, now.month, now.year)
        creation, modified2 = io.get_metadata(main_dir, last_profile)
        io.write_metadata(self.main_dir, self.last_profile, creation, modified)
        
        # Clear the old data.
        self.data[:] = []
        self.liststore.clear()
        
        # Read the data and switch to the new profile.
        self.data = io.read_profile(main_dir = self.main_dir, name = name)
        self.last_profile = name
        self.update_list()
        
        # Update the title.
        self.update_title()
    
    
    def merge_datasets(self, event):
        """Merges two datasets."""
        
        # Get the list of profiles.
        profiles = io.get_profile_list(self.main_dir, self.last_profile)
        
        # If there are no other profiles, tell the user and cancel the action.
        if len(profiles) == 0:
            show_alert_dialog(self, "Merge Datasets", "There are no other datasets.")
            return
        
        # Get the profile to merge.
        mer_dlg = DatasetSelectionDialog(self, "Merge Datasets", profiles)
        response = mer_dlg.run()
        model, treeiter = mer_dlg.treeview.get_selection().get_selected()
        mer_dlg.destroy()
        
        # If the user did not press OK or nothing was selected, don't continue:
        if response != Gtk.ResponseType.OK or treeiter == None:
            return
        
        # Get the profile name and read the data.
        name = model[treeiter][0]
        data2 = io.read_profile(main_dir = self.main_dir, name = name)
        
        # Filter the new data to make sure there are no duplicates.
        new_data = []
        date_col = datasets.get_column(self.data, 0)
        for i in data2:
            
            # If the date already appears, don't include it.
            if i[0] not in date_col:
                new_data.append(i)
        
        # Append, sort, and update the data.
        self.data += new_data
        self.data = sorted(self.data, key = lambda x: datetime.datetime.strptime(x[0], "%d/%m/%Y"))
        self.update_list()
        
        # Update the title and save the data.
        self.update_title()
        self.save()
        
        # Delete the directory of the profile that was merged in.
        shutil.rmtree("%s/profiles/%s" % (self.main_dir, name))
        
    
    def data_dataset_new(self, event):
        """Copies or moves data to a new dataset."""
        
        # If there is no data, tell the user and don't continue.
        if len(self.data) == 0:
            show_no_data_dialog(self, "Copy Data to New Dataset")
            return
        
        # Get the dates.
        dates = []
        dates2 = []
        for i in self.data:
            dates.append([i[0]])
            dates2.append(i[0])
        
        # Get the profile name.
        new_dlg = DatasetNameDialog(self, "Copy Data to New Dataset")
        response = new_dlg.run()
        name = new_dlg.nam_ent.get_text().lstrip().rstrip()
        new_dlg.destroy()
        
        # If the user did not press OK, don't continue:
        if response != Gtk.ResponseType.OK:
            return
        
        # Validate the name. If the name isn't valid, don't continue.
        valid = validate.validate_profile(self.main_dir, name)
        if valid != "":
            show_error_dialog(self, "Copy Data to New Dataset", valid)
            return
            
        # Get the dates to move or copy.
        buttons = [["Cancel", Gtk.ResponseType.CANCEL], ["Move Data", 34], ["Copy Data", 35]]
        date_dlg = DateSelectionDialog(self, "Copy Data to New Dataset", dates, buttons)
        response = date_dlg.run()
        model, treeiter = date_dlg.treeview.get_selection().get_selected_rows()
        date_dlg.destroy()
        
        # If the user did not click OK or nothing was selected, don't continue:
        if (response != 34 and response != 35) or treeiter == None:
            return
        
        # Create the directory and file.
        io.write_blank_profile(self.main_dir, name)
        launch.create_metadata(self.main_dir, name)
        
        # Get the dates.
        ndates = []
        for i in treeiter:
            ndates.append(model[i][0])
        
        # Get the data.
        ndata = []
        for i in range(0, len(self.data)):
            if self.data[i][0] in ndates:
                ndata.append(self.data[i])
        
        # If the user wants to move the data, delete the items in the current profile.
        if response == DialogResponse.MOVE_DATA:
            
            self.data = [x for x in data if x[0] not in ndates]
        
            # Reset the list.
            self.update_list()
        
            # Update the title.
            self.update_title()
        
        # Put the data in the new profile.
        io.write_profile(main_dir = self.main_dir, name = name, data = ndata)
    
    
    def data_dataset_existing(self, event):
        """Copies or moves data to an existing dataset."""
        
        # If there is no data, tell the user and don't continue.
        if len(data) == 0:
            show_no_data_dialog(self, "Copy Data to Existing Dataset")
            return
        
        # Get the dates.
        dates = []
        dates2 = []
        for i in self.data:
            dates.append([i[0]])
            dates2.append(i[0])
        
        # Get the profile list.
        profiles = io.get_profile_list(self.main_dir, self.last_profile)
        
        # If there are no other profiles, don't continue.
        if len(profiles) == 0:
            show_alert_dialog(self, "Copy Data to Existing Dataset", "There are no other datasets.")
            return
        
        # Get the profile.
        exi_dlg = DatasetSelectionDialog(self, "Copy Data to Existing Dataset", profiles)
        response = exi_dlg.run()
        model, treeiter = exi_dlg.treeview.get_selection().get_selected()
        exi_dlg.destroy()
        
        # If the user did not click OK or nothing was selected, don't continue:
        if response != Gtk.ResponseType.OK or treeiter == None:
            return
            
        # Get the profile name.
        name = model[treeiter][0]
        
        # Get the dates to move or copy.
        buttons = [["Cancel", Gtk.ResponseType.CANCEL], ["Move Data", 34], ["Copy Data", 35]]
        date_dlg = DateSelectionDialog(self, "Copy Data to Existing Dataset", dates, buttons)
        response = date_dlg.run()
        model, treeiter = date_dlg.treeview.get_selection().get_selected_rows()
        date_dlg.destroy()
        
        # If the user did not click OK or nothing was selected, don't continue:
        if (response != 34 and response != 35) or treeiter == None:
            return
            
        # Get the dates.
        ndates = []
        for i in treeiter:
            ndates.append(model[i][0])
        
        # Get the data.
        ndata = []
        for i in range(0, len(self.data)):
            if self.data[i][0] in ndates:
                ndata.append(self.data[i])

        # If the user wants to move the data, delete the items in the current profile.
        if response == DialogResponse.MOVE_DATA:
            
            self.data = [x for x in data if x[0] not in ndates]
        
            # Reset the list.
            self.update_list()
        
            # Set the new title.
            self.update_title()
        
        # Load the data.
        data2 = io.read_profile(main_dir = self.main_dir, name = name)
        
        # Filter the new data to make sure there are no duplicates.
        new_data = []
        date_col = datasets.get_column(data2, 0)
        for i in ndata:
            
            # If the date already appears, don't include it.
            if i[0] not in date_col:
                new_data.append(i)
        
        # Append and sort the data.
        data2 += new_data
        data2 = sorted(data2, key = lambda x: datetime.datetime.strptime(x[0], '%d/%m/%Y'))
        
        # Save the data.
        io.write_profile(main_dir = self.main_dir, name = name, data = data2)
        now = datetime.datetime.now()
        modified = "%d/%d/%d" % (now.day, now.month, now.year)
        creation, modified2 = io.get_metadata(self.main_dir, self.last_profile)
        io.write_metadata(main_dir, last_profile, creation, modified)
    
    
    def options(self, event):
        """Shows the Options dialog."""
        
        current_units = self.config["units"]
        
        # Get the new options.
        opt_dlg = OptionsDialog(self, self.config)
        response = opt_dlg.run()
        prefill = opt_dlg.pre_chk.get_active()
        restore = opt_dlg.win_chk.get_active()
        location = opt_dlg.loc_ent.get_text()
        units_ = opt_dlg.unit_com.get_active_text().lower()
        pastebin = opt_dlg.paste_ent.get_text()
        show_dates = opt_dlg.date_chk.get_active()
        show_units = opt_dlg.unit_chk.get_active()
        confirm_del = opt_dlg.del_chk.get_active()
        show_prefill = opt_dlg.pdl_chk.get_active()
        confirm_exit = opt_dlg.cex_chk.get_active()
        import_all = opt_dlg.imp_chk.get_active()
        truncate_notes = opt_dlg.trun_chk.get_active()
        graph_color = convert.rgba_to_hex(opt_dlg.graph_color_btn.get_rgba())
        opt_dlg.destroy()
        
        # If the user did not press OK or Reset, don't continue.
        if response != Gtk.ResponseType.OK and response != DialogResponse.RESET:
            return
        
        # If the user pressed Reset, get the default fields.
        if response == DialogResponse.RESET:
            
            # Confirm that the user wants to reset.
            reset = show_question_dialog(opt_dlg, "Options", "Are you sure you want to reset the options to the default values?")
            if response == Gtk.ResponseType.CANCEL:
                return
            
            # Get the default options.
            prefill = False
            restore = True
            location = ""
            units_ = "metric"
            pastebin = "d2314ff616133e54f728918b8af1500e"
            show_dates = True
            show_units = True
            confirm_del = True
            show_prefill = True
            confirm_exit = False
            import_all = False
            truncate_notes = True
            graph_color = "#0000FF"
        
        # Set the configuration.
        self.config["pre-fill"] = prefill
        self.config["restore" ] = restore
        self.config["location"] = location
        self.config["units"] = units_
        self.config["pastebin"] = pastebin
        self.config["show_dates"] = show_dates
        self.config["show_units"] = show_units
        self.config["confirm_del"] = confirm_del
        self.config["show_pre-fill"] = show_prefill
        self.config["confirm_exit"] = confirm_exit
        self.config["import_all"] = import_all
        self.config["truncate_notes"] = truncate_notes
        self.config["graph_color"] = graph_color
        
        # Configure the units.
        self.units = launch.get_units(self.config)
        
        # If the units changed, ask the user if they want to convert the data.
        if current_units != self.config["units"]:
            response = show_question_dialog(opt_dlg, "Options", "The units have changed from %s to %s.\n\nWould you like to convert the current data to the new units?" % (current_units, self.config["units"]))
            if response == Gtk.ResponseType.OK:
                
                # Convert the data.
                new_data = convert.convert(self.data, units_)
                
                # Update the list.
                self.data[:] = []
                self.data[:] = new_data[:]
                self.update_list()
        
        # Add/remove the units from the column titles.
        if not self.config["show_units"]:
            self.temp_col.set_title("Temperature")
            self.chil_col.set_title("Wind Chill")
            self.prec_col.set_title("Precipitation")
            self.wind_col.set_title("Wind")
            self.humi_col.set_title("Humidity")
            self.visi_col.set_title("Visibility")
            self.airp_col.set_title("Air Pressure")
        else:
            self.temp_col.set_title("Temperature (%s)" % self.units["temp"])
            self.chil_col.set_title("Wind Chill (%s)" % self.units["temp"])
            self.prec_col.set_title("Precipitation (%s)" % self.units["prec"])
            self.wind_col.set_title("Wind (%s)" % self.units["wind"])
            self.humi_col.set_title("Humidity (%)")
            self.visi_col.set_title("Visibility (%s)" % self.units["visi"])
            self.airp_col.set_title("Air Pressure (%s)" % self.units["airp"])
        
        # Update the title and save the data.
        self.update_title()
        self.update_list()
        self.save(from_options = True)
    
    
    def save(self, from_options = False):
        """Saves the data."""
        
        # If saving the options, don't write all the profile data.
        if not from_options:
            
            # Save the current profile.
            io.write_profile(self.main_dir, self.last_profile, data = self.data)
            
            # Save the creation and last modified dates.
            now = datetime.datetime.now()
            modified = "%d/%d/%d" % (now.day, now.month, now.year)
            creation, modified2 = io.get_metadata(self.main_dir, self.last_profile)
            io.write_metadata(self.main_dir, self.last_profile, creation, modified)
            
            # Save the last profile.
            io.write_last_profile(self.conf_dir, self.last_profile)
        
        # Save the configuration.
        io.write_config(self.conf_dir, self.config)
    
    
    def update_list(self):
        """Updates the list of weather data."""
        
        # Truncate the note fields before the data is added to the interface.
        new_data = copy.deepcopy(self.data)
        if self.config["truncate_notes"]:
            for row in new_data:
                note = row[9]
                newline_split = False
                if "\n" in note:
                    note = note.splitlines()[0]
                    newline_split = True
                if len(note) > 46:
                    note = note[0:40] + " [...]"
                elif newline_split:
                    note = note + " [...]"
                row[9] = note
            
        self.liststore.clear()
        for i in new_data:
            self.liststore.append(i)
        
    
    def update_title(self):
        """Updates the window title."""
        
        if self.config["show_dates"]:
            self.set_title("WeatherLog - %s - %s to %s" % (self.last_profile, (self.data[0][0] if len(self.data) != 0 else "None"), (self.data[len(self.data)-1][0] if len(self.data) != 0 else "None")))
        else:
            self.set_title("WeatherLog - %s" % self.last_profile)
    
    
    def show_about(self, event):
        """Shows the About dialog."""
        
        # Load the icon.
        img_file = open(self.ICON_MEDIUM, "rb")
        img_bin = img_file.read()
        img_file.close()
        loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        loader.write(img_bin)
        loader.close()
        pixbuf = loader.get_pixbuf()
        
        # Create the dialog.
        about_dlg = Gtk.AboutDialog(self)
        
        # Set the details.
        about_dlg.set_title("About WeatherLog")
        about_dlg.set_program_name(self.TITLE)
        about_dlg.set_logo(pixbuf)
        about_dlg.set_version(self.VERSION)
        about_dlg.set_comments("WeatherLog is an application for keeping track of the weather\nand getting information about past trends.")
        about_dlg.set_copyright("Copyright (c) 2013-2015 Adam Chesak")
        about_dlg.set_authors(["Adam Chesak <achesak@yahoo.com>"])
        about_dlg.set_license(license_text)
        about_dlg.set_website("http://achesak.github.io/weatherlog")
        about_dlg.set_website_label("http://achesak.github.io/weatherlog")
        
        # Show the dialog.
        about_dlg.show_all()
        about_dlg.run()
        about_dlg.destroy()

    
    def show_help(self, event):
        """Shows the help in a web browser."""
        
        # Open the help file.
        webbrowser.open_new("weatherlog_resources/help/help.html")    
    

    def exit(self, x = False, y = False):
        """Closes the application."""
        
        # Confirm that the user wants to exit, if needed.
        if self.config["confirm_exit"]:
            
            response = show_question_dialog(self, "Quit", "Are you sure you want to close WeatherLog?")
            if response != Gtk.ResponseType.OK:
                return
        
        # Close the  application.
        Gtk.main_quit()


# Show the window and start the application.
if __name__ == "__main__" and len(sys.argv) == 1:
    
    # Show the window and start the application.
    win = WeatherLog()
    win.connect("delete-event", win.exit)
    win.show_all()
    Gtk.main()
