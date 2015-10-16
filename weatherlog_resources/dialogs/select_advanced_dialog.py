# -*- coding: utf-8 -*-


# This file defines the advanced dialog for selecting data.


# Import GTK for the dialog.
from gi.repository import Gtk, Gdk
# Import the dataset functions.
import weatherlog_resources.datasets as datasets
# Import the functions for filtering data.
import weatherlog_resources.filter_data as filter_data
# Import the functions for exporting info.
import weatherlog_resources.export as export
# Import the subset display dialog.
from weatherlog_resources.dialogs.data_subset_dialog import DataSubsetDialog
# Import generic dialogs.
from weatherlog_resources.dialogs.misc_dialogs import *


class SelectDataAdvancedDialog(Gtk.Window):
    """Shows the advanced data selection dialog."""
    def __init__(self, parent, profile, data, config, units):
        """Create the dialog."""
        
        # Create the window
        Gtk.Window.__init__(self)
        self.set_title("View Data Subset - %s" % profile)
        self.set_resizable(True)
        self.set_default_size(400, 300)
        self.conditions = []
        self.last_profile = profile
        self.data = data
        self.config = config
        self.units = units
        
        # Create the box
        sel_grid = Gtk.Grid()
        self.add(sel_grid)
        
        # Create the labels and input widgets.
        add_grid = Gtk.Grid()
        mode_lbl = Gtk.Label("Mode:  ")
        mode_lbl.set_alignment(0, 0.5)
        add_grid.add(mode_lbl)
        self.mode_com = Gtk.ComboBoxText()
        for i in ["Match All", "Match At Least One", "Match None"]:
            self.mode_com.append_text(i)
        self.mode_com.set_active(0)
        self.mode_com.set_hexpand(True)
        add_grid.attach_next_to(self.mode_com, mode_lbl, Gtk.PositionType.RIGHT, 1, 1)
        field_lbl = Gtk.Label("Field: ")
        field_lbl.set_alignment(0, 0.5)
        add_grid.attach_next_to(field_lbl, mode_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.field_com = Gtk.ComboBoxText()
        for i in ["Temperature", "Wind Chill", "Precipitation Amount", "Precipition Type", "Wind Speed", "Wind Direction",
                  "Humidity", "Air Pressure Change", "Visibility", "Cloud Cover", "Cloud Type", "Notes"]:
            self.field_com.append_text(i)
        self.field_com.set_active(0)
        add_grid.attach_next_to(self.field_com, field_lbl, Gtk.PositionType.RIGHT, 1, 1)
        cond_lbl = Gtk.Label("Condition: ")
        cond_lbl.set_alignment(0, 0.5)
        add_grid.attach_next_to(cond_lbl, field_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.cond_com = Gtk.ComboBoxText()
        for i in ["Equal To", "Not Equal To", "Greater Than", "Less Than", "Greater Than or Equal To", "Less Than or Equal To",
                  "Between", "Between (Inclusive)", "Outside", "Outside (Inclusive)", "Starts With", "Does Not Start With",
                  "Ends With", "Does Not End With"]:
            self.cond_com.append_text(i)
        self.cond_com.set_active(0)
        add_grid.attach_next_to(self.cond_com, cond_lbl, Gtk.PositionType.RIGHT, 1, 1)
        value_lbl = Gtk.Label("Value: ")
        value_lbl.set_alignment(0, 0.5)
        add_grid.attach_next_to(value_lbl, cond_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.value_ent = Gtk.Entry()
        add_grid.attach_next_to(self.value_ent, value_lbl, Gtk.PositionType.RIGHT, 1, 1)
        sel_grid.add(add_grid)
        
        # Create the data conditions listbox.
        self.liststore = Gtk.ListStore(str, str, str)
        self.treeview = Gtk.TreeView(model = self.liststore)
        field_text = Gtk.CellRendererText()
        self.field_col = Gtk.TreeViewColumn("Field", field_text, text = 0)
        self.treeview.append_column(self.field_col)
        cond_text = Gtk.CellRendererText()
        self.cond_col = Gtk.TreeViewColumn("Condition", cond_text, text = 1)
        self.treeview.append_column(self.cond_col)
        value_text = Gtk.CellRendererText()
        self.value_col = Gtk.TreeViewColumn("Value", value_text, text = 2)
        self.treeview.append_column(self.value_col)
        self.treeview.set_hexpand(True)
        self.treeview.set_vexpand(True)
        self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        sel_grid.attach_next_to(self.treeview, add_grid, Gtk.PositionType.BOTTOM, 1, 1)
        self.treeview.connect("key-press-event", self.treeview_keypress)
        
        # Create the buttons.
        sel_box = Gtk.Box()
        self.ok_btn = Gtk.Button(label = "View")
        self.ok_btn.connect("clicked", self.view_subset)
        sel_box.pack_end(self.ok_btn, True, True, 0)
        self.cancel_btn = Gtk.Button(label = "Cancel")
        self.cancel_btn.connect("clicked", lambda x: self.destroy())
        sel_box.pack_end(self.cancel_btn, True, True, 0)
        self.remove_btn = Gtk.Button(label = "Remove")
        self.remove_btn.connect("clicked", self.remove_condition)
        sel_box.pack_end(self.remove_btn, True, True, 0)
        self.add_btn = Gtk.Button(label = "Add")
        self.add_btn.connect("clicked", self.add_condition)
        sel_box.pack_end(self.add_btn, True, True, 0)
        sel_grid.attach_next_to(sel_box, self.treeview, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Show the window.
        self.show_all()
    
    
    def treeview_keypress(self, widget, event):
        """Checks the treeview for keypress events."""
        
        # On 'Delete', remove selected row(s).
        if event.keyval == Gdk.KEY_Delete:
            self.remove_condition(True)
    
    
    def check_operator(self, field, operator):
        """Checks if the selected operator can be used with the selected field."""
        
        # If the column that is being compared is precipitation type, wind direction, air pressure change, 
        # cloud cover, or cloud type, and the comparison is numerical, don't continue.
        if field == "Precipitation Type" or field == "Wind Direction" or field == "Air Pressure Change" or \
           field == "Cloud Cover" or field == "Cloud Type" or field == "Notes":
            if operator != "Equal To" and operator != "Not Equal To" and operator != "Starts With" and \
               operator != "Does Not Start With" and operator != "Ends With" and operator != "Does Not End With":
                show_error_dialog(self, "Add Condition", "Invalid comparison: %s cannot use the \"%s\" operator." % (field, operator))
                return True
        # If the column that is being compared is a numerical field and the comparison is stricly non-numerical,
        # don't continue.
        else:
            if operator == "Starts With" or operator == "Does Not Start With" or operator == "Ends With" or \
               operator == "Does Not End With":
                show_error_dialog(self, "Add Condition", "Invalid comparison: %s cannot use the \"%s\" operator." % (field, operator))
                return True
        return False
    
    
    def check_used(self, field):
        """Checks if the selected field has already been used."""
        
        if field in datasets.get_column(self.conditions, 0):
            show_error_dialog(self, "Add Condition", "A condition for %s has already been entered." % field)
            return True
        return False
    
    
    def check_one(self, operator, value):
        """Checks if there is one value, if the operator requires that."""
        
        if operator != "Between" and operator !=  "Between (Inclusive)" and operator != "Outside" and \
           operator != "Outside (Inclusive)" and operator != "Equal To" and operator != "Not Equal To":
            if value.count(",") != 0:
                show_error_dialog(self, "Add Condition", "The \"%s\" operator requires only one value to be specified." % operator)
                return True
        return False
    
    
    def check_two(self, operator, value):
        """Checks if there are two values, if the operator requires that."""
        
        if operator == "Between" or operator == "Between (Inclusive)" or operator == "Outside" or \
           operator == "Outside (Inclusive)":
            if value.count(",") != 1:
                show_error_dialog(self, "Add Condition", "The \"%s\" operator requires two values to be specified, separated with a comma." % operator)
                return True
        return False
    
    
    def add_condition(self, widget):
        """Shows the add condition dialog."""
        
        # Get the entered values
        field = self.field_com.get_active_text()
        condition = self.cond_com.get_active_text()
        value = self.value_ent.get_text()
        
        # Validate the data, and add if it's acceptable.
        if not self.check_operator(field, condition) and not self.check_used(field) and not self.check_two(condition, value) and \
           not self.check_one(condition, value) and value.lstrip().rstrip() != "":
            self.liststore.append([field, condition, value])
            self.conditions.append([field, condition, value])
            
            # Clear the fields.
            self.field_com.set_active(0)
            self.cond_com.set_active(0)
            self.value_ent.set_text("")
            
    
    def remove_condition(self, widget):
        """Removes the selected condition."""
        
        # Get the selected conditions.
        model, treeiter = self.treeview.get_selection().get_selected_rows()
        conds = []
        for i in treeiter:
            conds.append(model[i][0])
        
        # Don't continue if nothing was selected.
        if len(conds) == 0:
            return
        
        # Remove the conditions and update the UI.
        for i in conds:
            index = datasets.get_column(self.conditions, 0).index(i)
            del self.conditions[index]
        
        self.liststore.clear()
        for i in self.conditions:
            self.liststore.append(i)
    
    def view_subset(self, widget):
        """Filters the data and displays the subset."""
        
        # Get the selection mode and conditions.
        sel_mode = self.mode_com.get_active_text().lower()
        conditions = []
        for i in self.liststore:
            if i[2].lstrip().rstrip() == "":
                continue
            conditions.append(i[:])
        
        # Loop through the conditions and filter the data.
        filtered = []
        first = True
        for i in conditions:
            
            # Get the filtered list.
            subset = filter_data.filter_data(self.data, i)
            
            # If this is the first condition, add all the data to the filtered list.
            if first:
                filtered += subset
                first = False
            
            # Otherwise, make sure it is combined correctly.
            # AND combination mode:
            elif sel_mode == "match all":
                filtered = filter_data.filter_and(filtered, subset)
            
            # OR combination mode or NOT combination mode:
            elif sel_mode == "match at least one" or sel_mode == "match none":
                filtered = filter_data.filter_or(filtered, subset)
        
        # If the NOT combination mode is used, apply that filter as well.
        if sel_mode == "match none":
            filtered = filter_data.filter_not(filtered, data)
        
        # If there are no items that match the condition, don't show the main dialog.
        if len(filtered) == 0:
            show_alert_dialog(self, "Data Subset - %s" % self.last_profile, "No data matches the specified condition(s).")
            return
        
        # Show the subset.
        sub_dlg = DataSubsetDialog(self, "Data Subset - %s" % self.last_profile, filtered, self.config["show_units"], self.units)
        response = sub_dlg.run()
        sub_dlg.destroy()
        
        # If the user clicked Export:
        if response == 9:
            
            # Get the filename.
            response2, filename = show_export_dialog(self, "Export Data Subset - %s" % self.last_profile)
            
            # Export the info.
            if response2 == Gtk.ResponseType.OK:
                data_list = [["WeatherLog Subset Data - %s - %s to %s" % (self.last_profile, (filtered[0][0] if len(filtered) != 0 else "None"), (filtered[len(filtered)-1][0] if len(filtered) != 0 else "None")),
                               ["Date", "Temperature (%s)" % self.units["temp"], "Wind Chill (%s)" % self.units["temp"],
                                "Precipitation (%s)" % self.units["prec"], "Wind (%s)" % self.units["wind"],
                                "Humidity (%%)", "Air Pressure (%s)" % self.units["airp"], "Visibility (%s)" % self.units["visi"],
                                "Cloud Cover", "Notes"],
                                filtered]]
                export.html_generic(data_list, filename)
