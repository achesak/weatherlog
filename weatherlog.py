#!/usr/bin/env python
# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog
# Version 5.0
#
# WeatherLog is an application for keeping track of the weather and
# getting information about past trends.
#
# Released under the GNU General Public License version 3.
#
################################################################################


# Import Gtk and Gdk for the interface.
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio
# Import webbrowser for opening the help in the user's browser.
import webbrowser
# Import datetime for date operations.
import datetime
import os
import os.path
# Import sys for closing the application.
import sys

# Import URLError for error checking
try:
    from urllib2 import URLError
except ImportError:
    from urllib.request import URLError

# Tell Python not to create bytecode files, as they mess with the git repo.
# This line can be removed be the user, if desired.
sys.dont_write_bytecode = True

# Import application modules.
from resources.constants import *
import resources.launch as launch
import resources.datasets as datasets
import resources.dates as dates
import resources.validate as validate
import resources.convert as convert
import resources.io as io
import resources.export as export
import resources.info as info
import resources.tables as tables
import resources.graphs as graphs
import resources.filter_data as filter_data
import resources.pastebin as pastebin
import resources.commands as commands

# Import UI builders.
import resources.ui.info_builder as info_builder
import resources.ui.table_builder as table_builder
import resources.ui.graph_builder as graph_builder

# Import dialogs.
from resources.dialogs.add_dialog import AddNewDialog
from resources.dialogs.edit_dialog import EditDialog
from resources.dialogs.entry_dialog import GenericEntryDialog
from resources.dialogs.date_selection_dialog import DateSelectionDialog
from resources.dialogs.calendar_range_dialog import CalendarRangeDialog
from resources.dialogs.info_dialog import InfoDialog
from resources.dialogs.dataset_dialog import DatasetDialog
from resources.dialogs.dataset_add_select_dialog import DatasetAddSelectionDialog
from resources.dialogs.data_subset_selection_dialog import DataSubsetSelectionDialog
from resources.dialogs.data_subset_dialog import DataSubsetDialog
from resources.dialogs.export_pastebin_dialog import ExportPastebinDialog
from resources.dialogs.weather_dialog import CurrentWeatherDialog
from resources.dialogs.preferences_dialog import PreferencesDialog
from resources.dialogs.about_dialog import WeatherLogAboutDialog
from resources.dialogs.misc_dialogs import *

# Tell Python not to create bytecode files, as they mess with the git repo.
# This line can be removed be the user, if desired.
sys.dont_write_bytecode = True


# noinspection PyUnusedLocal,PyAttributeOutsideInit,PyUnboundLocalVariable
class WeatherLog(Gtk.Application):
    """Creates the WeatherLog application."""

    def __init__(self, *args, **kwargs):
        """Initializes the application."""

        super(WeatherLog, self).__init__(*args, application_id="com.achesak.weatherlog", **kwargs)
        self.window = None

    def do_startup(self):
        """Application startup."""

        Gtk.Application.do_startup(self)

        # Get the application's data, constants, and user data.
        self.version, self.title, self.menu_data, self.file_menu_data, self.style_data, self.icon_small, \
            self.icon_medium, self.default_width, self.default_height, self.help_link = launch.get_ui_info()
        self.main_dir, self.conf_dir = launch.get_main_dir()
        self.config = launch.get_config(self.conf_dir)
        launch.ensure_files_exist(self.main_dir, self.conf_dir)

        self.last_dataset, self.original_dataset, self.dataset_exists, self.last_width, self.last_height = \
            launch.get_restore_data(self.main_dir, self.conf_dir, self.config, self.default_width, self.default_height)
        self.units = launch.get_units(self.config)
        self.data = io.read_dataset(self.main_dir, self.last_dataset)

        self.weather_codes = launch.get_weather_codes()
        self.pastebin_constants = launch.get_pastebin_constants()
        self.graph_data = launch.get_graph_data()

        # Build the app menu.
        action = Gio.SimpleAction.new("weather", None)
        action.connect("activate", lambda x, y: self.get_weather())
        self.add_action(action)
        action = Gio.SimpleAction.new("subset", None)
        action.connect("activate", lambda x, y: self.select_data_subset())
        self.add_action(action)
        action = Gio.SimpleAction.new("range", None)
        action.connect("activate", lambda x, y: self.data_range())
        self.add_action(action)
        action = Gio.SimpleAction.new("options", None)
        action.connect("activate", lambda x, y: self.preferences())
        self.add_action(action)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", lambda x, y: self.show_about())
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", lambda x, y: self.exit(x, y))
        self.add_action(action)

        # Build the non-menu actions.
        action = Gio.SimpleAction.new("add", None)
        action.connect("activate", lambda x, y: self.add_new())
        self.add_action(action)
        action = Gio.SimpleAction.new("edit", None)
        action.connect("activate", lambda x, y: self.edit())
        self.add_action(action)
        action = Gio.SimpleAction.new("remove", None)
        action.connect("activate", lambda x, y: self.remove())
        self.add_action(action)
        action = Gio.SimpleAction.new("search", None)
        action.connect("activate", lambda x, y: self.focus_search())
        self.add_action(action)
        action = Gio.SimpleAction.new("import", None)
        action.connect("activate", lambda x, y: self.import_data())
        self.add_action(action)
        action = Gio.SimpleAction.new("import_new_dataset", None)
        action.connect("activate", lambda x, y: self.import_new_dataset())
        self.add_action(action)
        action = Gio.SimpleAction.new("export", None)
        action.connect("activate", lambda x, y: self.export_file())
        self.add_action(action)
        action = Gio.SimpleAction.new("export_pastebin", None)
        action.connect("activate", lambda x, y: self.export_pastebin())
        self.add_action(action)

        self.set_accels_for_action("app.add", ["<Primary>n"])
        self.set_accels_for_action("app.remove", ["<Primary>r"])
        self.set_accels_for_action("app.search", ["<Primary>f"])
        self.set_accels_for_action("app.import", ["<Primary>o"])
        self.set_accels_for_action("app.export", ["<Primary>s"])

        builder = Gtk.Builder.new_from_string(self.menu_data, -1)
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        """Application activate."""

        if not self.window:
            self.window = Gtk.ApplicationWindow(application=self, title="WeatherLog")

        # Create the user interface.
        self.create_interface()

        # If the dataset could not be found, tell the user and save as the default dataset.
        if not self.dataset_exists:
            show_alert_dialog(self.window, self.title,
                              "The dataset \"%s\" could not be found and was not loaded." % self.original_dataset)
            self.save()

        # Add the data.
        self.update_list()
        self.update_title()

        self.window.present()
        self.window.show_all()

    def create_interface(self):
        """Creates the user interface."""

        # Create the window.
        self.window.set_default_size(self.last_width, self.last_height)
        self.window.set_icon_from_file(self.icon_small)
        self.window.set_title("WeatherLog")

        # Create the header bar.
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.window.set_titlebar(self.header)

        # Create the main UI.
        self.liststore = Gtk.ListStore(str, str, str, str, str, str, str, str, str, str)
        self.treeview = Gtk.TreeView(model=self.liststore)
        date_text = Gtk.CellRendererText()
        self.date_col = Gtk.TreeViewColumn("Date", date_text, text=DatasetColumn.DATE)
        self.date_col.set_resizable(True)
        self.treeview.append_column(self.date_col)
        temp_text = Gtk.CellRendererText()
        self.temp_col = Gtk.TreeViewColumn("Temperature (%s)" % self.units["temp"], temp_text,
                                           text=DatasetColumn.TEMPERATURE)
        self.temp_col.set_resizable(True)
        self.treeview.append_column(self.temp_col)
        chil_text = Gtk.CellRendererText()
        self.chil_col = Gtk.TreeViewColumn("Wind Chill (%s)" % self.units["temp"], chil_text,
                                           text=DatasetColumn.WIND_CHILL)
        self.chil_col.set_resizable(True)
        self.treeview.append_column(self.chil_col)
        prec_text = Gtk.CellRendererText()
        self.prec_col = Gtk.TreeViewColumn("Precipitation (%s)" % self.units["prec"], prec_text,
                                           text=DatasetColumn.PRECIPITATION)
        self.prec_col.set_resizable(True)
        self.treeview.append_column(self.prec_col)
        wind_text = Gtk.CellRendererText()
        self.wind_col = Gtk.TreeViewColumn("Wind (%s)" % self.units["wind"], wind_text, text=DatasetColumn.WIND)
        self.wind_col.set_resizable(True)
        self.treeview.append_column(self.wind_col)
        humi_text = Gtk.CellRendererText()
        self.humi_col = Gtk.TreeViewColumn("Humidity (%)", humi_text, text=DatasetColumn.HUMIDITY)
        self.humi_col.set_resizable(True)
        self.treeview.append_column(self.humi_col)
        airp_text = Gtk.CellRendererText()
        self.airp_col = Gtk.TreeViewColumn("Air Pressure (%s)" % self.units["airp"], airp_text,
                                           text=DatasetColumn.AIR_PRESSURE)
        self.airp_col.set_resizable(True)
        self.treeview.append_column(self.airp_col)
        visi_text = Gtk.CellRendererText()
        self.visi_col = Gtk.TreeViewColumn("Visibility (%s)" % self.units["visi"], visi_text,
                                           text=DatasetColumn.VISIBILITY)
        self.visi_col.set_resizable(True)
        self.treeview.append_column(self.visi_col)
        clou_text = Gtk.CellRendererText()
        self.clou_col = Gtk.TreeViewColumn("Cloud Cover", clou_text, text=DatasetColumn.CLOUD_COVER)
        self.clou_col.set_resizable(True)
        self.treeview.append_column(self.clou_col)
        note_text = Gtk.CellRendererText()
        self.note_col = Gtk.TreeViewColumn("Notes", note_text, text=DatasetColumn.NOTES)
        self.note_col.set_resizable(True)
        self.treeview.append_column(self.note_col)
        self.update_columns()

        # Create the data frame.
        self.data_frame = Gtk.ScrolledWindow()
        self.data_frame.set_hexpand(True)
        self.data_frame.set_vexpand(True)
        self.data_frame.add(self.treeview)

        # Set up the tabs.
        info_builder.info_builder(self)
        table_builder.table_builder(self)
        graph_builder.graph_builder(self)

        # Create the stack.
        self.stack = Gtk.Stack()
        self.stack.set_hexpand(True)
        self.stack.set_vexpand(True)
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.set_stack(self.stack)
        self.header.set_custom_title(self.stack_switcher)

        # Create the header bar buttons: data buttons
        data_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(data_btn_box.get_style_context(), "linked")
        self.add_btn = Gtk.Button()
        add_img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="list-add-symbolic"), Gtk.IconSize.BUTTON)
        self.add_btn.add(add_img)
        self.add_btn.set_tooltip_text("Add more data (Control-N)")
        self.edit_btn = Gtk.Button()
        edit_img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="edit-symbolic"), Gtk.IconSize.BUTTON)
        self.edit_btn.add(edit_img)
        self.edit_btn.set_tooltip_text("Edit data")
        self.remove_btn = Gtk.Button()
        remove_img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="list-remove-symbolic"), Gtk.IconSize.BUTTON)
        self.remove_btn.add(remove_img)
        self.remove_btn.set_tooltip_text("Remove data (Control-R)")
        data_btn_box.add(self.add_btn)
        data_btn_box.add(self.edit_btn)
        data_btn_box.add(self.remove_btn)

        # Create the header bar buttons: search entry
        self.search_ent = Gtk.SearchEntry()
        self.search_ent.set_placeholder_text("Search")
        self.search_ent.set_tooltip_text("Search for data (Control-F)")

        # Create the header bar buttons: dataset button
        self.dataset_btn = Gtk.Button(label="Datasets")

        # Create the header bar buttons: file menu button
        self.file_btn = Gtk.MenuButton()
        file_img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="document-open-symbolic"), Gtk.IconSize.BUTTON)
        self.file_btn.add(file_img)
        file_builder = Gtk.Builder.new_from_string(self.file_menu_data, -1)
        file_menu = file_builder.get_object("file-menu")
        self.file_popover = Gtk.Popover.new_from_model(self.file_btn, file_menu)
        self.file_btn.set_popover(self.file_popover)

        # Set up the header bar buttons.
        self.header.pack_start(data_btn_box)
        self.header.pack_start(self.search_ent)
        self.header.pack_end(self.file_btn)
        self.header.pack_end(self.dataset_btn)

        # Set up the stack.
        self.stack.add_titled(self.data_frame, "data", "Data")
        self.stack.add_titled(self.info_frame, "info", "Info")
        self.stack.add_titled(self.table_frame, "tables", "Tables")
        self.stack.add_titled(self.graph_frame, "graphs", "Graphs")

        # Build the UI.
        self.window.add(self.stack)
        self.treeview.grab_focus()

        # Bind the button events.
        self.add_btn.connect("clicked", lambda x: self.add_new())
        self.edit_btn.connect("clicked", lambda x: self.edit())
        self.remove_btn.connect("clicked", lambda x: self.remove())
        self.search_ent.connect("activate", lambda x: self.search())
        self.dataset_btn.connect("clicked", lambda x: self.manage_datasets())

        # Bind the events.
        self.window.connect("delete-event", self.delete_event)
        self.treeview.connect("button-press-event", self.context_event)
        self.treeview.connect("row-activated", self.activated_event)
        self.treeview.connect("key-press-event", self.treeview_keypress)
        self.search_ent.connect("changed", self.update_search_style)

        # Create the CSS provider.
        self.style_provider = Gtk.CssProvider()
        self.style_context = Gtk.StyleContext()
        self.style_context.add_provider_for_screen(Gdk.Screen.get_default(), self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.style_provider.load_from_data(self.style_data)

    def delete_event(self, widget, event):
        """Saves the restore data."""

        width, height = self.window.get_size()
        io.write_restore_data(self.conf_dir, self.last_dataset, height, width)
        self.exit()

    def context_event(self, widget, event):
        """Opens the context menu."""

        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            self.context_menu.popup(None, None, None, None, event.button, event.time)
            return True

    def activated_event(self, widget, treepath, column):
        """Opens the edit dialog on double click."""

        tree_sel = self.treeview.get_selection()
        tm, ti = tree_sel.get_selected()
        date = tm.get_value(ti, 0)
        self.edit(date)

    def treeview_keypress(self, widget, event):
        """Checks the treeview for keypress events."""

        # On 'Delete', remove selected row(s).
        if event.keyval == Gdk.KEY_Delete:
            try:
                tree_sel = self.treeview.get_selection()
                tm, ti = tree_sel.get_selected()
                date = tm.get_value(ti, 0)

                self.remove(date)

            except TypeError:
                pass

    def focus_search(self):
        """Focuses on the search entry."""

        self.search_ent.grab_focus()

    def update_search_style(self, event):
        """Clears the 'not found' search styling."""

        self.search_ent.get_style_context().remove_class("search-not-found")

    def add_new(self, prefill_data=None):
        """Shows the dialog for input of new data."""

        if prefill_data is None:
            prefill_data = []

        # Get the data to add.
        new_dlg = AddNewDialog(self.window, self.last_dataset, self.config["city"], self.config["zipcode"],
                               self.config["pre-fill"], self.units, self.config,
                               prefill_data)
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
        note = new_dlg.note_buffer.get_text(new_dlg.note_buffer.get_start_iter(), new_dlg.note_buffer.get_end_iter(),
                                            True).strip()

        temp_unit = new_dlg.temp_unit.get_active_text()
        chil_unit = new_dlg.chil_unit.get_active_text()
        prec_unit = new_dlg.prec_unit.get_active_text()
        wind_unit = new_dlg.wind_unit.get_active_text()
        visi_unit = new_dlg.visi_unit.get_active_text()

        new_dlg.destroy()
        if response != Gtk.ResponseType.OK:
            return

        # If the precipitation or wind are zero, set the appropriate type/direction to "None".
        if not prec:
            prec_type = "None"
        if not wind:
            wind_dir = "None"

        # If the date has already been entered, tell the user and prompt to continue.
        if date in datasets.get_column(self.data, DatasetColumn.DATE):
            overwrite = show_question_dialog(self.window, "Add New Data",
                                             "The date %s has already been entered.\n\nOverwrite with new data?" % date)

            if overwrite == Gtk.ResponseType.OK:
                index = datasets.get_column(self.data, DatasetColumn.DATE).index(date)
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
        self.data = sorted(self.data, key=lambda x: datetime.datetime.strptime(x[DatasetColumn.DATE], "%d/%m/%Y"))

        # Update and save the data.
        self.update_list()
        self.update_title()
        self.save()
        self.debug("add_new", new_data)

    def edit(self, edit_date=None):
        """Edits a row of data."""

        # If there is no data don't show the date selection.
        if len(self.data) == 0:
            return

        # Get the selected date.
        selected_dates = datasets.get_column_list(self.data, [0])
        if edit_date is not None:
            date = edit_date

        else:
            try:
                tree_sel = self.treeview.get_selection()
                tm, ti = tree_sel.get_selected()
                date = tm.get_value(ti, 0)

            except TypeError:

                # If no date was selected, show the dialog to select one.
                dat_dlg = DateSelectionDialog(self.window, "Edit Data", self.last_dataset,
                                              selected_dates, buttons=[["Edit", Gtk.ResponseType.OK]],
                                              multi_select=False)
                response = dat_dlg.run()
                model, treeiter = dat_dlg.treeview.get_selection().get_selected()
                dat_dlg.destroy()

                # If the user did not click OK or nothing was selected, don't continue.
                if response != Gtk.ResponseType.OK or treeiter is None:
                    return

                # Get the date.
                date = model[treeiter][0]

        # Get the index of the date.
        index = datasets.get_column(self.data, DatasetColumn.DATE).index(date)

        # Get the new data.
        edit_dlg = EditDialog(self.window, self.last_dataset, self.data[index], date, self.units)
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
        note = edit_dlg.note_buffer.get_text(edit_dlg.note_buffer.get_start_iter(), edit_dlg.note_buffer.get_end_iter(),
                                             True).strip()
        temp_unit = edit_dlg.temp_unit.get_active_text()
        chil_unit = edit_dlg.chil_unit.get_active_text()
        prec_unit = edit_dlg.prec_unit.get_active_text()
        wind_unit = edit_dlg.wind_unit.get_active_text()
        visi_unit = edit_dlg.visi_unit.get_active_text()
        edit_dlg.destroy()

        if response == Gtk.ResponseType.CANCEL:
            return

        # Remove the row if the user wants to.
        if response == DialogResponse.REMOVE:
            # Confirm that the user wants to delete the row.
            if self.config["confirm_del"]:
                response = show_question_dialog(self.window, "Remove Data",
                                                "Are you sure you want to delete the data for %s? This action cannot be undone." % date)
                if response != Gtk.ResponseType.OK:
                    return

            # Delete the selected dates.
            del self.data[index]

            # Update and save the data.
            self.update_list()
            self.update_title()
            self.save()

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

        # Update and save the data.
        self.update_list()
        self.save()
        self.debug("edit", new_data)

    def remove(self, date=None):
        """Removes a row of data from the list."""

        # If there is no data don't show the date selection.
        if len(self.data) == 0:
            return

        ndates = []
        if not date:

            # Get the dates.
            selected_dates = datasets.get_column_list(self.data, [0])

            # Get the dates to remove.
            rem_dlg = DateSelectionDialog(self.window, "Remove Data", self.last_dataset, selected_dates,
                                          buttons=[["Remove", Gtk.ResponseType.OK]])
            response = rem_dlg.run()
            model, treeiter = rem_dlg.treeview.get_selection().get_selected_rows()
            rem_dlg.destroy()

            if response != Gtk.ResponseType.OK or treeiter is None:
                return

            # Get the dates.
            ndates = []
            for i in treeiter:
                ndates.append(model[i][0])

            if len(ndates) == 0:
                return

        else:
            ndates.append(date)

        # Confirm that the user wants to delete the row.
        if self.config["confirm_del"]:
            selected_dates = "\n\nSelected date%s:" % ("s" if len(ndates) > 1 else "")
            for date in ndates:
                selected_dates += "\n" + date
            response = show_question_dialog(self.window, "Remove Data",
                                            "Are you sure you want to delete the selected date%s? This action cannot be undone.%s" % (
                                                "s" if len(ndates) > 1 else "", selected_dates))
            if response != Gtk.ResponseType.OK:
                return

        # Delete the selected dates.
        for i in ndates:
            index = datasets.get_column(self.data, DatasetColumn.DATE).index(i)
            del self.data[index]

        # Update and save the data.
        self.update_list()
        self.update_title()
        self.save()

    def get_weather(self):
        """Gets the current weather."""

        # Check if the API key is set.
        if not self.config["openweathermap"]:
            show_error_dialog(self.window, "Get Weather", "No API key. Please check the key entered in the Options window.")
            return

        # Show the weather.
        info_dlg = CurrentWeatherDialog(self.window, "Current Weather", self.config, self.units, self.weather_codes)
        response = info_dlg.run()
        info_dlg.destroy()

    def data_range(self):
        """Gets the range for the data to display."""

        if len(self.data) == 0:
            show_no_data_dialog(self.window, "Data in Range")
            return

        # Get the first and last entered dates.
        day_start = dates.split_date(self.data[0][DatasetColumn.DATE])
        day_end = dates.split_date(self.data[len(self.data) - 1][DatasetColumn.DATE])
        datelist = dates.date_list_datetime(datasets.get_column(self.data, DatasetColumn.DATE))

        # Get the starting and ending dates.
        cal_dlg = CalendarRangeDialog(self.window, "Data in Range", self.last_dataset, day_start, day_end)
        response = cal_dlg.run()
        year1, month1, day1 = cal_dlg.start_cal.get_date()
        year2, month2, day2 = cal_dlg.end_cal.get_date()
        date1 = "%d/%d/%d" % (day1, month1 + 1, year1)
        date2 = "%d/%d/%d" % (day2, month2 + 1, year2)
        cal_dlg.destroy()

        # If the user did not click OK, don't continue.
        if response != DialogResponse.VIEW_INFO:
            return

        # Get the indices.
        dt_start = datetime.datetime(year1, month1 + 1, day1)
        start_index = dates.date_above(dt_start, datelist)
        dt_end = datetime.datetime(year2, month2 + 1, day2)
        end_index = dates.date_below(dt_end, datelist)

        # Check to make sure these dates are valid, and cancel the action if not.
        if start_index == DateValidation.INVALID:
            show_error_dialog(self.window, "Data in Range",
                              "%s is not a valid date.\n\nThis date is not present and is not before any other dates."
                              % date1)
            return
        if end_index == DateValidation.INVALID:
            show_error_dialog(self.window, "Data in Range",
                              "%s is not a valid date.\n\nThis date is not present and is not after any other dates."
                              % date2)
            return
        if end_index < start_index:
            show_error_dialog(self.window, "Data in Range", "The ending date must be after the starting date.")
            return

        # Get the new list.
        data2 = self.data[start_index:end_index + 1]

        self.show_info_generic(data=data2)

    def show_info_generic(self, data=None):
        """Shows info about the data."""

        # Get the info.
        info_data = [
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
        table_data = [
            tables.temp_table(data, self.units),
            tables.chil_table(data, self.units),
            tables.prec_table(data, self.units),
            tables.wind_table(data, self.units),
            tables.humi_table(data, self.units),
            tables.airp_table(data, self.units),
            tables.visi_table(data, self.units)
        ]
        graph_data = graphs.get_data(data)

        # Show the info.
        info_dlg = InfoDialog(self.window, "Data", self.last_dataset, info_data, table_data, graph_data, self.config, self.graph_data)
        response = info_dlg.run()
        info_dlg.destroy()

        # Export the data:
        if response == DialogResponse.EXPORT:
            response2, filename = show_export_dialog(self.window, "Export Info")
            if response2 == Gtk.ResponseType.OK:
                export.html_generic([["Overview", ["Field", "Value"], info_data[0]],
                                     ["Temperature", ["Field", "Value"], info_data[1]],
                                     ["Wind Chill", ["Field", "Value"], info_data[2]],
                                     ["Precipitation", ["Field", "Value"], info_data[3]],
                                     ["Wind", ["Field", "Value"], info_data[4]],
                                     ["Humidity", ["Field", "Value"], info_data[5]],
                                     ["Air Pressure", ["Field", "Value"], info_data[6]],
                                     ["Visibility", ["Field", "Value"], info_data[7]],
                                     ["Cloud Cover", ["Field", "Value"], info_data[8]],
                                     ["Notes", ["Field", "Value"], info_data[9]]], filename)
                
            response2, filename = show_export_dialog(self.window, "Export Tables")
            if response2 == Gtk.ResponseType.OK:
                table_columns = ["Day", "Value", "Average Difference", "Low Difference", "High Difference",
                                 "Median Difference"]
                export.html_generic([["Temperature", table_columns, table_data[0]],
                                     ["Wind Chill", table_columns, table_data[1]],
                                     ["Precipitation", table_columns, table_data[2]],
                                     ["Wind", table_columns, table_data[3]],
                                     ["Humidity", table_columns, table_data[4]],
                                     ["Air Pressure", table_columns, table_data[5]],
                                     ["Visibility", table_columns, table_data[6]]], filename)

    def search(self):
        """Searches for data."""

        # Get the search term.
        search_term = self.search_ent.get_text().lstrip().rstrip()
        if not search_term or len(self.data) == 0:
            return

        # Filter and display the data.
        filtered = filter_data.filter_quick(self.data, search_term, self.config["default_case_insensitive"])

        # If nothing found, set the background color of the entry to red.
        if len(filtered) == 0:
            self.search_ent.get_style_context().add_class("search-not-found")
            return

        sub_dlg = DataSubsetDialog(self.window, "Search", "Search results for \"%s\"" % search_term, filtered, self.units,
                                   self.config)
        response = sub_dlg.run()
        sub_dlg.destroy()

        # Export the data:
        if response == DialogResponse.EXPORT:
            response2, filename = show_export_dialog(self.window, "Search Results")
            if response2 == Gtk.ResponseType.OK:
                data_list = [["WeatherLog Search Results - %s - %s to %s" % (
                    self.last_dataset, (filtered[0][0] if len(filtered) != 0 else "None"),
                    (filtered[len(filtered) - 1][0] if len(filtered) != 0 else "None")),
                              ["Date", "Temperature (%s)" % self.units["temp"], "Wind Chill (%s)" % self.units["temp"],
                               "Precipitation (%s)" % self.units["prec"], "Wind (%s)" % self.units["wind"],
                               "Humidity (%)", "Air Pressure (%s)" % self.units["airp"],
                               "Visibility (%s)" % self.units["visi"],
                               "Cloud Cover", "Notes"],
                              filtered]]
                export.html_generic(data_list, filename)

    def select_data_subset(self):
        """Shows the data selection dialog."""

        if len(self.data) == 0:
            show_no_data_dialog(self.window, "View Data Subset")
            return

        # Show the condition selection dialog.
        sel_dlg = DataSubsetSelectionDialog(self.last_dataset, self.data, self.config, self.units)

    def import_data(self):
        """Imports data and merges it into the current list."""

        # Get the filename.
        response, filename = show_import_dialog(self.window, "Import")

        if response != Gtk.ResponseType.OK and response != DialogResponse.IMPORT_OVERWRITE:
            return

        # Error checking for when the Import and Overwrite option is chosen. GTK will allow this
        # to be clicked when no filename has been entered, causing an error. Check to make sure
        # there was a filename to work around this.
        if (response == DialogResponse.IMPORT_OVERWRITE) and (not filename or not os.path.isfile(filename)):
            show_error_dialog(self.window, "Import", "No filename entered.")
            return

        # If the imported data is invalid, don't continue.
        try:
            validate_error = validate.validate_data(filename)
        except:
            show_error_dialog(self.window, "Import",
                              "Error importing data. Is the data in the correct format?")
            return
        if validate_error != ImportValidation.VALID:
            show_error_dialog(self.window, "Import",
                              "The data in the selected file is not valid. %s" % validate.validate_dataset_strings[validate_error])
            return

        # Confirm that the user wants to overwrite the data, if the current dataset isn't blank.
        if response == DialogResponse.IMPORT_OVERWRITE and len(self.data) > 0:
            response2 = show_question_dialog(self.window, "Import",
                                             "Are you sure you want to import the data?\n\nAll current data will be overwritten.")
            if response2 != Gtk.ResponseType.OK:
                return

        # Read the data.
        data2 = io.read_dataset(filename=filename)

        # Ask the user what dates they want to import.
        treeiter = None
        model = None
        if not self.config["import_all"]:
            buttons = [["Import", Gtk.ResponseType.OK], ["Import All", DialogResponse.IMPORT_ALL]]
            date_dlg = DateSelectionDialog(self.window, "Import", self.last_dataset, datasets.conflict_exists(datasets.get_column(self.data, 0), datasets.get_column(data2, 0)), buttons=buttons, show_conflicts=True, import_mode=True)
            response3 = date_dlg.run()
            model, treeiter = date_dlg.treeview.get_selection().get_selected_rows()
            date_dlg.destroy()

        else:
            response3 = DialogResponse.IMPORT_ALL

        if response3 != DialogResponse.IMPORT_ALL and response3 != Gtk.ResponseType.OK:
            return
        if response3 == Gtk.ResponseType.OK and treeiter is None:
            return

        # If the user selected certain dates, only import those.
        if response3 == Gtk.ResponseType.OK:

            # Get the dates.
            selected_dates = []
            for i in treeiter:
                selected_dates.append(model[i][0])

            # Get the new data list.
            data3 = []
            for i in data2:
                if i[0] in selected_dates:
                    data3.append(i)

        # If the user pressed Import All, import all of the data.
        elif response3 == DialogResponse.IMPORT_ALL:
            data3 = data2[:]

        # Overwrite or merge the data:
        if response == DialogResponse.IMPORT_OVERWRITE:
            self.data = data3[:]

        else:

            # Filter the new data to make sure there are no duplicates.
            new_data = []
            date_col = datasets.get_column(self.data, DatasetColumn.DATE)
            for i in data3:

                # If the date already appears, don't include it.
                if i[DatasetColumn.DATE] not in date_col:
                    new_data.append(i)

            self.data += new_data

        # Update and save the data.
        self.data = sorted(self.data, key=lambda x: datetime.datetime.strptime(x[0], "%d/%m/%Y"))
        self.update_list()
        self.update_title()
        self.save()

    def import_new_dataset(self):
        """Imports data from a file and inserts it in a new dataset."""

        # Get the filename.
        response, filename = show_file_dialog(self.window, "Import as New Dataset")

        if response != Gtk.ResponseType.OK:
            return

        # If the imported data is invalid, don't continue.
        try:
            validate_error = validate.validate_data(filename)
        except:
            show_error_dialog(self.window, "Import",
                              "Error importing data. Is the data in the correct format?")
            return
        if validate_error != ImportValidation.VALID:
            show_error_dialog(self.window, "Import as New Dataset",
                              "The data in the selected file is not valid. %s" % validate.validate_dataset_strings[validate_error])
            return

        # Get the new dataset name.
        new_dlg = GenericEntryDialog(self.window, title="Import as New Dataset", message="Enter dataset name")
        response = new_dlg.run()
        name = new_dlg.nam_ent.get_text().lstrip().rstrip()
        new_dlg.destroy()

        if response != Gtk.ResponseType.OK:
            return

        # Validate the name. If it contains a non-alphanumeric character or is just space,
        # show a dialog and cancel the action.
        valid = validate.validate_dataset(self.main_dir, name)
        if valid != DatasetValidation.VALID:
            show_error_dialog(self.window, "Import as New Dataset",
                              validate.validate_dataset_name_strings[valid])
            return

        ndata = io.read_dataset(filename=filename)

        # Ask the user what dates they want to import.
        if not self.config["import_all"]:
            buttons = [["Import", Gtk.ResponseType.OK], ["Import All", DialogResponse.IMPORT_ALL]]
            date_dlg = DateSelectionDialog(self.window, "Import as New Dataset", name, datasets.get_column(ndata, 0), buttons=buttons, import_mode=True)
            response = date_dlg.run()
            model, treeiter = date_dlg.treeview.get_selection().get_selected_rows()
            date_dlg.destroy()

        else:
            response = DialogResponse.IMPORT_ALL

        if response != DialogResponse.IMPORT_ALL and response != Gtk.ResponseType.OK:
            return
        if response == Gtk.ResponseType.OK and treeiter is None:
            return

        # Create the dataset directory and file.
        self.last_dataset = name
        io.write_blank_dataset(self.main_dir, name)
        io.write_metadata(self.main_dir, name, now=True)

        # Clear the data.
        self.data[:] = []
        self.liststore.clear()

        # If the user selected certain dates, only import those.
        if response == Gtk.ResponseType.OK:

            # Get the dates.
            dates_list = []
            for i in treeiter:
                dates_list.append(model[i][0])

            for i in ndata:
                if i[DatasetColumn.DATE] in dates_list:
                    self.data.append(i)

        # If the user pressed Import All, import all of the data.
        elif response == Gtk.ResponseType.OKL:
            self.data = ndata[:]

        # Update and save the data.
        self.update_list()
        self.update_title()
        self.save()

    def export_file(self):
        """Exports the data to a file."""

        if len(self.data) == 0:
            show_no_data_dialog(self.window, "Export", message="There is no data to export.")
            return

        # Get the filename.
        response, filename = show_save_dialog(self.window, "Export")

        if response != Gtk.ResponseType.OK and response != DialogResponse.EXPORT_CSV and response != DialogResponse.EXPORT_HTML and response != DialogResponse.EXPORT_JSON:
            return

        # Error checking for when the HTML, CSV, or JSON options are chosen. GTK will allow these
        # to be clicked when no filename has been entered, causing an error. Check to make sure
        # there was a filename to work around this.
        if (response == DialogResponse.EXPORT_CSV or response == DialogResponse.EXPORT_HTML or response == DialogResponse.EXPORT_JSON) and not filename:
            show_error_dialog(self.window, "Export", "No filename entered.")
            return

        # Export the data.
        if response == Gtk.ResponseType.OK:
            io.write_dataset(filename=filename, data=self.data)
        elif response == DialogResponse.EXPORT_JSON:
            export.json(self.data, self.config, filename)
        elif response == DialogResponse.EXPORT_CSV:
            export.csv(self.data, self.units, filename)
        elif response == DialogResponse.EXPORT_HTML:
            data_list = [[self.update_title(),
                          ["Date", "Temperature (%s)" % self.units["temp"], "Wind Chill (%s)" % self.units["temp"],
                           "Precipitation (%s)" % self.units["prec"], "Wind (%s)" % self.units["wind"],
                           "Humidity (%)", "Air Pressure (%s)" % self.units["airp"],
                           "Visibility (%s)" % self.units["visi"],
                           "Cloud Cover", "Notes"],
                          self.data]]
            export.html_generic(data_list, filename)

    def export_pastebin(self):
        """Exports the data to Pastebin."""

        if len(self.data) == 0:
            show_no_data_dialog(self.window, "Export to Pastebin",
                                message="There is no data to export.")
            return

        if len(self.config["pastebin"].lstrip().rstrip()) == 0:
            show_error_dialog(self.window, "Export to Pastebin",
                              "No API key. Please check the key entered in the Options window.")
            return

        # Show the dialog and get the user's response.
        pas_dlg = ExportPastebinDialog(self.window, "Export to Pastebin", self.last_dataset, self.config)
        response = pas_dlg.run()
        name = pas_dlg.nam_ent.get_text()
        mode = pas_dlg.for_com.get_active_text().lower()
        expires = pas_dlg.exi_com.get_active_text()
        exposure = pas_dlg.exo_com.get_active_text()
        pas_dlg.destroy()

        if response != Gtk.ResponseType.OK:
            return

        # Upload the data.
        pastebin_response, result = pastebin.upload_pastebin(self.data, name, mode, expires, exposure, self.units,
                                                             self.config, self.update_title())

        # Check the return response.
        if pastebin_response == PastebinExport.INVALID_KEY:
            show_error_dialog(self.window, "Export to Pastebin", "Invalid API key. Please check the key entered in the Options window.")
        elif pastebin_response == PastebinExport.ERROR:
            show_error_dialog(self.window, "Export to Pastebin", "The data could not be uploaded to Pastebin:\n\n%s" % result)
        elif pastebin_response == PastebinExport.NO_CONSTANTS:
            show_error_dialog(self.window, "Export to Pastebin", "Missing constants file. The data could not be uploaded to Pastebin.")
        elif pastebin_response == PastebinExport.SUCCESS:
            response = show_alert_dialog(self.window, "Export to Pastebin", "The data has been uploaded to Pastebin, and can be accessed at the following URL:\n\n%s\n\nPress \"OK\" to open the link in a web browser." % result,
                                         show_cancel=True)
            if response == Gtk.ResponseType.OK:
                webbrowser.open(result)

    def manage_datasets(self):
        """Opens the dataset management dialog."""

        # Show the dataset dialog.
        dat_dlg = DatasetDialog(self.window, self.main_dir, self.last_dataset, self.config)
        response = dat_dlg.run()
        dat_dlg.destroy()

        # Get the dataset name.
        name = dat_dlg.switch_name
        if name is None:
            return

        # Clear the old data.
        self.data[:] = []
        self.liststore.clear()

        # Read the data and switch to the other dataset.
        self.data = io.read_dataset(main_dir=self.main_dir, name=name)
        self.last_dataset = name

        # Update and save the data.
        self.update_list()
        self.update_title()
        self.save()

    def copy_data_dataset(self, event):
        """Copies or moves data to another dataset."""

        if len(self.data) == 0:
            show_no_data_dialog(self.window, "Copy Data", message="There is no data to copy.")
            return

        # Get the dates and datasets.
        dates_list = datasets.get_column_list(self.data, [0])
        dates2 = datasets.get_column(self.data, 0)
        dataset_list = io.get_dataset_list(self.main_dir, self.last_dataset)

        # Get the new name or selected dataset.
        dat_dlg = DatasetAddSelectionDialog(self.window, "Copy Data", dataset_list, self.main_dir, self.last_dataset)
        response1 = dat_dlg.run()
        new_name = dat_dlg.add_ent.get_text().lstrip().rstrip()
        model1, treeiter1 = dat_dlg.treeview.get_selection().get_selected()
        dat_dlg.destroy()

        if response1 != DialogResponse.USE_SELECTED:
            return

        # Get the selected name.
        try:
            sel_name = model1[treeiter1][0]
        except TypeError:
            return

        # Get the dates to move or copy.
        buttons = [["Move", DialogResponse.MOVE_DATA], ["Copy", DialogResponse.COPY_DATA]]
        if response1 == DialogResponse.USE_NEW:
            date_dlg = DateSelectionDialog(self.window, "Copy Data", "", dates_list, buttons, DialogResponse.COPY_DATA)
        else:
            conflicts = datasets.conflict_exists(
                datasets.get_column(io.read_dataset(main_dir=self.main_dir, name=sel_name), 0),
                datasets.get_column(self.data, 0))
            date_dlg = DateSelectionDialog(self.window, "Copy Data", "", conflicts, buttons, DialogResponse.COPY_DATA,
                                           show_conflicts=True)
        response2 = date_dlg.run()
        model2, treeiter2 = date_dlg.treeview.get_selection().get_selected_rows()
        date_dlg.destroy()

        # If the user did not click OK or nothing was selected, don't continue:
        if (response2 != DialogResponse.MOVE_DATA and response2 != DialogResponse.COPY_DATA) or treeiter2 is None:
            return

        # Get the dates.
        ndates = []
        for i in treeiter2:
            ndates.append(model2[i][0])

        # Get the data.
        ndata = []
        for i in range(0, len(self.data)):
            if self.data[i][DatasetColumn.DATE] in ndates:
                ndata.append(self.data[i])

        # If the user wants to move the data, delete the items in the current dataset.
        if response2 == DialogResponse.MOVE_DATA:
            self.data = [x for x in self.data if x[DatasetColumn.DATE] not in ndates]

        # Load the data.
        data2 = io.read_dataset(main_dir=self.main_dir, name=sel_name)

        # Filter the new data to make sure there are no duplicates.
        new_data = []
        date_col = datasets.get_column(data2, DatasetColumn.DATE)
        for i in ndata:

            if i[DatasetColumn.DATE] not in date_col:
                new_data.append(i)

        # Append and sort the data.
        data2 += new_data
        data2 = sorted(data2, key=lambda n: datetime.datetime.strptime(n[0], '%d/%m/%Y'))

        # Save the data.
        self.save()
        io.write_dataset(main_dir=self.main_dir, name=sel_name, data=data2)
        now = datetime.datetime.now()
        modified = "%d/%d/%d" % (now.day, now.month, now.year)
        creation, modified2 = io.get_metadata(self.main_dir, self.last_dataset)
        io.write_metadata(self.main_dir, self.last_dataset, creation, modified)

        # Update the title and data.
        self.update_list()
        self.update_title()

    def preferences(self):
        """Shows the Preferences dialog."""

        current_units = self.config["units"]

        # Get the new options.
        opt_dlg = PreferencesDialog(self.window, self.config)
        response = opt_dlg.run()
        new_config = self.config
        new_config["pre-fill"] = opt_dlg.pre_chk.get_active()
        new_config["restore"] = opt_dlg.win_chk.get_active()
        new_config["units"] = opt_dlg.unit_com.get_active_text().lower()
        new_config["show_units"] = opt_dlg.unit_chk.get_active()
        new_config["confirm_del"] = opt_dlg.del_chk.get_active()
        new_config["import_all"] = opt_dlg.imp_chk.get_active()
        new_config["truncate_notes"] = opt_dlg.trun_chk.get_active()
        new_config["graph_color"] = convert.rgba_to_hex(opt_dlg.graph_color_btn.get_rgba())[0:7]
        new_config["line_width"] = opt_dlg.width_sbtn.get_value()
        new_config["line_style"] = opt_dlg.line_com.get_active_text()
        new_config["hatch_style"] = opt_dlg.hatch_com.get_active_text()
        new_config["pastebin"] = opt_dlg.pname_ent.get_text()
        new_config["pastebin_format"] = opt_dlg.pform_com.get_active_text()
        new_config["pastebin_expires"] = self.pastebin_constants["expires"][opt_dlg.pexpi_com.get_active_text()]
        new_config["pastebin_exposure"] = self.pastebin_constants["exposure"][opt_dlg.pexpo_com.get_active_text()]
        new_config["default_case_insensitive"] = opt_dlg.case_chk.get_active()
        new_config["zipcode"] = opt_dlg.zip_ent.get_text()
        new_config["city"] = opt_dlg.cit_ent.get_text()
        new_config["country"] = opt_dlg.cnt_ent.get_text()
        new_config["location_type"] = "city" if opt_dlg.use_city_rbtn.get_active() else "zip"
        new_config["openweathermap"] = opt_dlg.owm_ent.get_text()
        new_config["default_selection_mode"] = opt_dlg.smode_com.get_active_text()
        new_config["reset_search"] = opt_dlg.rsearch_chk.get_active()
        opt_dlg.destroy()

        # If the user did not press OK or Reset, don't continue.
        if response != Gtk.ResponseType.OK and response != DialogResponse.RESET:
            return

        # If the user pressed Reset, set all options to default.
        if response == DialogResponse.RESET:

            reset = show_question_dialog(opt_dlg, "Preferences",
                                         "Are you sure you want to reset the preferences to the default values?")
            if reset == Gtk.ResponseType.CANCEL:
                return

            self.config = launch.get_config(self.conf_dir, get_default=True)

        else:
            self.config = new_config

        # Configure the units.
        self.units = launch.get_units(self.config)
        if current_units != self.config["units"]:
            response = show_question_dialog(self.window, "Preferences",
                                            "The units have changed from %s to %s.\n\nWould you like to convert the current data to the new units?" % (
                                                current_units, self.config["units"]))
            if response == Gtk.ResponseType.OK:
                # Convert the data.
                new_data = convert.convert(self.data, self.config["units"])
                self.data[:] = []
                self.data[:] = new_data[:]

        # Update the interface and save the data.
        self.update_columns()
        self.update_title()
        self.update_list()
        self.save()

    def show_about(self):
        """Shows the About dialog."""

        # Load the icon.
        img_file = open(self.icon_medium, "rb")
        img_bin = img_file.read()
        img_file.close()
        loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        loader.write(img_bin)
        loader.close()
        pixbuf = loader.get_pixbuf()

        # Read the license
        license_file = open("LICENSE.md", "r")
        license_text = license_file.read()
        license_file.close()

        # Show the dialog.
        about_dlg = WeatherLogAboutDialog(self.window, self.title, self.version, pixbuf, license_text)
        about_dlg.run()
        about_dlg.destroy()

    def save(self):
        """Saves the data."""

        # Save the current dataset.
        io.write_dataset(self.main_dir, self.last_dataset, data=self.data)

        # Save the creation and last modified dates.
        now = datetime.datetime.now()
        modified = "%d/%d/%d" % (now.day, now.month, now.year)
        creation, modified2 = io.get_metadata(self.main_dir, self.last_dataset)
        io.write_metadata(self.main_dir, self.last_dataset, creation, modified)

        # Save the configuration.
        io.write_config(self.conf_dir, self.config)

    def update_list(self):
        """Updates the list of weather data."""

        # Truncate the note fields before the data is added to the interface.
        if self.config["truncate_notes"]:
            new_data = datasets.truncate_column(self.data, DatasetColumn.NOTES, 46)
        else:
            new_data = self.data

        self.liststore.clear()
        for i in new_data:
            self.liststore.append(i)

        # Update the button interactivity.
        btns_active = len(self.data) != 0
        self.edit_btn.set_sensitive(btns_active)
        self.remove_btn.set_sensitive(btns_active)

        self.update_data()

    def update_title(self):
        """Updates the window title."""

        self.dataset_btn.set_label(self.last_dataset)

    def update_columns(self):
        """Updates the list column titles."""

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

    def update_data(self):
        """Updates the Info, Tables, and Graphs tabs."""

        # Clear the existing info data.
        self.info_gen_list.clear()
        self.info_temp_list.clear()
        self.info_chil_list.clear()
        self.info_prec_list.clear()
        self.info_wind_list.clear()
        self.info_humi_list.clear()
        self.info_airp_list.clear()
        self.info_visi_list.clear()
        self.info_clou_list.clear()
        self.info_note_list.clear()

        # Clear the existing table data.
        self.table_temp_list.clear()
        self.table_chil_list.clear()
        self.table_prec_list.clear()
        self.table_wind_list.clear()
        self.table_humi_list.clear()
        self.table_airp_list.clear()
        self.table_visi_list.clear()

        # Clear the existing graph data.
        graph_builder.clear_graphs(self)

        if len(self.data) == 0:
            return

        # Get the info data.
        info_data = [
            info.general_info(self.data, self.units),
            info.temp_info(self.data, self.units),
            info.chil_info(self.data, self.units),
            info.prec_info(self.data, self.units),
            info.wind_info(self.data, self.units),
            info.humi_info(self.data, self.units),
            info.airp_info(self.data, self.units),
            info.visi_info(self.data, self.units),
            info.clou_info(self.data, self.units),
            info.note_info(self.data, self.units)
        ]

        # Add the info data.
        for i in info_data[0]:
            self.info_gen_list.append(i)
        for i in info_data[1]:
            self.info_temp_list.append(i)
        for i in info_data[2]:
            self.info_chil_list.append(i)
        for i in info_data[3]:
            self.info_prec_list.append(i)
        for i in info_data[4]:
            self.info_wind_list.append(i)
        for i in info_data[5]:
            self.info_humi_list.append(i)
        for i in info_data[6]:
            self.info_airp_list.append(i)
        for i in info_data[7]:
            self.info_visi_list.append(i)
        for i in info_data[8]:
            self.info_clou_list.append(i)
        for i in info_data[9]:
            self.info_note_list.append(i)

        # Get the table data.
        table_data = [
            tables.temp_table(self.data, self.units),
            tables.chil_table(self.data, self.units),
            tables.prec_table(self.data, self.units),
            tables.wind_table(self.data, self.units),
            tables.humi_table(self.data, self.units),
            tables.airp_table(self.data, self.units),
            tables.visi_table(self.data, self.units)
        ]

        # Add the table data.
        for i in table_data[0]:
            self.table_temp_list.append(i)
        for i in table_data[1]:
            self.table_chil_list.append(i)
        for i in table_data[2]:
            self.table_prec_list.append(i)
        for i in table_data[3]:
            self.table_wind_list.append(i)
        for i in table_data[4]:
            self.table_humi_list.append(i)
        for i in table_data[5]:
            self.table_airp_list.append(i)
        for i in table_data[6]:
            self.table_visi_list.append(i)

        # Get the graph data.
        graph_data = graphs.get_data(self.data)
        lines = self.graph_data["lines"]
        hatches = self.graph_data["hatches"]

        # Add the graph data.
        self.graph_temp_graph.plot(graph_data["date_ticks"], graph_data["temp_data"], color=self.config["graph_color"],
                                   linewidth=self.config["line_width"], linestyle=lines[self.config["line_style"]])
        self.graph_temp_graph.set_xticks(graph_data["date_ticks"])
        self.graph_temp_graph.set_xticklabels(graph_data["date_labels"], rotation="vertical")
        self.graph_chil_graph.plot(graph_data["date_ticks"], graph_data["chil_data"], color=self.config["graph_color"],
                                   linewidth=self.config["line_width"], linestyle=lines[self.config["line_style"]])
        self.graph_chil_graph.set_xticks(graph_data["date_ticks"])
        self.graph_chil_graph.set_xticklabels(graph_data["date_labels"], rotation="vertical")
        self.graph_prec_graph.plot(graph_data["date_ticks"], graph_data["prec_data"], color=self.config["graph_color"],
                                   linewidth=self.config["line_width"], linestyle=lines[self.config["line_style"]])
        self.graph_prec_graph.set_xticks(graph_data["date_ticks"])
        self.graph_prec_graph.set_xticklabels(graph_data["date_labels"], rotation="vertical")
        self.graph_pramt_graph.bar([0, 1, 2, 3], graph_data["prec_amount"], width=0.5, color=self.config["graph_color"],
                                   hatch=hatches[self.config["hatch_style"]])
        self.graph_prday_graph.bar([0, 1, 2, 3, 4], graph_data["prec_days"], width=0.5,
                                   color=self.config["graph_color"], hatch=hatches[self.config["hatch_style"]])
        self.graph_wind_graph.plot(graph_data["date_ticks"], graph_data["wind_data"], color=self.config["graph_color"],
                                   linewidth=self.config["line_width"], linestyle=lines[self.config["line_style"]])
        self.graph_wind_graph.set_xticks(graph_data["date_ticks"])
        self.graph_wind_graph.set_xticklabels(graph_data["date_labels"], rotation="vertical")
        self.graph_humi_graph.plot(graph_data["date_ticks"], graph_data["humi_data"], color=self.config["graph_color"],
                                   linewidth=self.config["line_width"], linestyle=lines[self.config["line_style"]])
        self.graph_humi_graph.set_xticks(graph_data["date_ticks"])
        self.graph_humi_graph.set_xticklabels(graph_data["date_labels"], rotation="vertical")
        self.graph_airp_graph.plot(graph_data["date_ticks"], graph_data["airp_data"], color=self.config["graph_color"],
                                   linewidth=self.config["line_width"], linestyle=lines[self.config["line_style"]])
        self.graph_airp_graph.set_xticks(graph_data["date_ticks"])
        self.graph_airp_graph.set_xticklabels(graph_data["date_labels"], rotation="vertical")
        self.graph_airc_graph.bar([0, 1, 2], graph_data["airp_change"], width=0.5, color=self.config["graph_color"],
                                  hatch=hatches[self.config["hatch_style"]])
        self.graph_visi_graph.plot(graph_data["date_ticks"], graph_data["visi_data"], color=self.config["graph_color"],
                                   linewidth=self.config["line_width"], linestyle=lines[self.config["line_style"]])
        self.graph_visi_graph.set_xticks(graph_data["date_ticks"])
        self.graph_visi_graph.set_xticklabels(graph_data["date_labels"], rotation="vertical")
        self.graph_clou_graph.bar([0, 1, 2, 3, 4], graph_data["clou_days"], width=0.5, color=self.config["graph_color"],
                                  hatch=hatches[self.config["hatch_style"]])
        self.graph_ctyp_graph.bar([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], graph_data["clou_types"], width=0.5,
                                  color=self.config["graph_color"], hatch=hatches[self.config["hatch_style"]])

    def debug(self, caller, data):
        """Debug mode function."""

        if self.config["debug_mode"]:
            print("Dataset - main dir - conf dir: %s - %s - %s" % (self.last_dataset, self.main_dir, self.conf_dir))
            print("Caller function: %s" % caller)
            print("Data: %s" % data)

    def exit(self, x=False, y=False):
        """Closes the application."""

        self.save()
        self.quit()

# Show the window and start the application.
if __name__ == "__main__" and len(sys.argv) == 1:

    win = WeatherLog()
    win.run()

# Commands:
elif __name__ == "__main__" and len(sys.argv) == 2:

    if sys.argv[1] == "purge":
        commands.purge()
