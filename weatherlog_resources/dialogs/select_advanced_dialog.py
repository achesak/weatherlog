# -*- coding: utf-8 -*-


# This file defines the advanced dialog for selecting data.


# Import GTK for the dialog.
from gi.repository import Gtk
# Import the dataset functions.
import weatherlog_resources.datasets as datasets
# Import generic dialogs.
from weatherlog_resources.dialogs.misc_dialogs import *


class SelectDataAdvancedDialog(Gtk.Window):
    """Shows the advanced data selection dialog."""
    def __init__(self, parent, profile):
        """Create the dialog."""
        
        # Create the window
        Gtk.Window.__init__(self)
        self.set_title("View Data Subset - %s" % profile)
        self.set_resizable(True)
        self.set_default_size(400, 300)
        self.conditions = []
        
        # Create the box
        sel_grid = Gtk.Grid()
        self.add(sel_grid)
        
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
        sel_grid.add(self.treeview)
        
        # Create the buttons.
        sel_box = Gtk.Box()
        self.ok_btn = Gtk.Button(label = "OK")
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
    
    
    def check_operator(self, field, operator):
        """Checks if the selected operator can be used with the selected field."""
        
        # If the column that is being compared is precipitation type, wind direction, air pressure change, 
        # cloud cover, or cloud type, and the comparison is numerical, don't continue.
        if field == "Precipitation Type" or field == "Wind Direction" or field == "Air Pressure Change" or \
           field == "Cloud Cover" or field == "Cloud Type":
            if operator != "Equal To" and operator != "Not Equal To":
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
        
        # Create the dialog.
        add_dlg = Gtk.Dialog("Add Condition", self, Gtk.DialogFlags.MODAL)
        
        # Add the buttons.
        add_dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        add_dlg.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        add_grid = Gtk.Grid()
        add_dlg.get_content_area().add(add_grid)
        
        # Create the labels and input widgets.
        field_lbl = Gtk.Label("Field: ")
        field_lbl.set_alignment(0, 0.5)
        add_grid.add(field_lbl)
        field_com = Gtk.ComboBoxText()
        for i in ["Temperature", "Wind Chill", "Precipitation Amount", "Precipition Type", "Wind Speed", "Wind Direction",
                  "Humidity", "Air Pressure Change", "Visibility", "Cloud Cover", "Cloud Type"]:
            field_com.append_text(i)
        field_com.set_active(0)
        add_grid.attach_next_to(field_com, field_lbl, Gtk.PositionType.RIGHT, 1, 1)
        cond_lbl = Gtk.Label("Condition: ")
        cond_lbl.set_alignment(0, 0.5)
        add_grid.attach_next_to(cond_lbl, field_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        cond_com = Gtk.ComboBoxText()
        for i in ["Equal To", "Not Equal To", "Greater Than", "Less Than", "Greater Than or Equal To", "Less Than or Equal To",
                  "Between", "Between (Inclusive)", "Outside", "Outside (Inclusive)"]:
            cond_com.append_text(i)
        cond_com.set_active(0)
        add_grid.attach_next_to(cond_com, cond_lbl, Gtk.PositionType.RIGHT, 1, 1)
        value_lbl = Gtk.Label("Value: ")
        value_lbl.set_alignment(0, 0.5)
        add_grid.attach_next_to(value_lbl, cond_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        value_ent = Gtk.Entry()
        add_grid.attach_next_to(value_ent, value_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        
        # Show the dialog and get the input.
        add_dlg.show_all()
        response = add_dlg.run()
        
        if response == Gtk.ResponseType.OK:
            
            field = field_com.get_active_text()
            condition = cond_com.get_active_text()
            value = value_ent.get_text()
            
            # Validate the data, and add if it's acceptable.
            if not self.check_operator(field, condition) and not self.check_used(field) and not self.check_two(condition, value) and \
               not self.check_one(condition, value):
                self.liststore.append([field, condition, value])
                self.conditions.append([field, condition, value])
        
        # Close the dialog.
        add_dlg.destroy()
    
    
    def remove_condition(self, widget):
        """Removes the selected condition."""
        
        # Get the selected conditions.
        model, treeiter = self.treeview.get_selection().get_selected_rows()
        conds = []
        for i in treeiter:
            conds.append(model[i][0])
        
        # Don't continue if nothing was selected.
        if len(conds) == 0:
            show_error_dialog(self, "Remove Condition", "No conditions selected.")
            return
        
        # Confirm that the user wants to remove the selected conditions.
        response = show_question_dialog(self, "Remove Condition", "Are you sure you want to remove the selected condition%s?" % ("s" if len(conds) > 1 else ""))
        if response != Gtk.ResponseType.OK:
            return
        
        # Remove the conditions and update the UI.
        for i in conds:
            index = datasets.get_column(self.conditions, 0).index(i)
            del self.conditions[index]
        
        self.liststore.clear()
        for i in self.conditions:
            self.liststore.append(i)
            
