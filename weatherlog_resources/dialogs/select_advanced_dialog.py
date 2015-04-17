# -*- coding: utf-8 -*-


# This file defines the advanced dialog for selecting data.


# Import GTK for the dialog.
from gi.repository import Gtk
# Import generic dialogs.
from weatherlog_resources.dialogs.misc_dialogs import *


class SelectDataAdvancedDialog(Gtk.Window):
    """Shows the advanced data selection dialog."""
    def __init__(self, parent, profile):
        """Create the dialog."""
        
        # Create the window
        Gtk.Window.__init__(self)
        self.set_title("Select Data - %s" % profile)
        self.set_resizable(True)
        self.set_default_size(300, 300)
        self.used_fields = []
        
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
        sel_grid.add(self.treeview)
        
        # Create the buttons.
        sel_box = Gtk.Box()
        self.ok_btn = Gtk.Button(label = "OK")
        sel_box.pack_end(self.ok_btn, True, True, 0)
        self.cancel_btn = Gtk.Button(label = "Cancel")
        sel_box.pack_end(self.cancel_btn, True, True, 0)
        self.remove_btn = Gtk.Button(label = "Remove")
        sel_box.pack_end(self.remove_btn, True, True, 0)
        self.add_btn = Gtk.Button(label = "Add")
        self.add_btn.connect("clicked", self.add_condition)
        sel_box.pack_end(self.add_btn, True, True, 0)
        sel_grid.attach_next_to(sel_box, self.treeview, Gtk.PositionType.BOTTOM, 1, 1)
        
        """
        # Create the selection mode label and combobox.
        mode_lbl = Gtk.Label("Selection mode: ")
        sel_grid.add(mode_lbl)
        self.mode_com = Gtk.ComboBoxText()
        for i in ["match all", "match at least one", "match none"]:
            self.mode_com.append_text(i)
        self.mode_com.set_active(0)
        sel_grid.attach_next_to(self.mode_com, mode_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the main grid.
        sel_list = Gtk.Grid()
        sel_box.add(sel_list)
        
        # Create the temperature row.
        self.sel_chk1 = Gtk.CheckButton("Temperature ")
        sel_list.add(self.sel_chk1)
        self.op_com1 = Gtk.ComboBoxText()
        for i in ["equal to", "not equal to", "greater than", "less than", "greater than or equal to", "less than or equal to", "between", "between (inclusive)", "outside", "outside (inclusive)"]:
            self.op_com1.append_text(i)
        self.op_com1.set_active(0)
        sel_list.attach_next_to(self.op_com1, self.sel_chk1, Gtk.PositionType.RIGHT, 1, 1)
        self.value_ent1 = Gtk.Entry()
        sel_list.attach_next_to(self.value_ent1, self.op_com1, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the precipitation amount row.
        self.sel_chk2 = Gtk.CheckButton("Precipitation amount ")
        sel_list.attach_next_to(self.sel_chk2, self.sel_chk1, Gtk.PositionType.BOTTOM, 1, 1)
        self.op_com2 = Gtk.ComboBoxText()
        for i in ["equal to", "not equal to", "greater than", "less than", "greater than or equal to", "less than or equal to", "between", "between (inclusive)", "outside", "outside (inclusive)"]:
            self.op_com2.append_text(i)
        self.op_com2.set_active(0)
        sel_list.attach_next_to(self.op_com2, self.sel_chk2, Gtk.PositionType.RIGHT, 1, 1)
        self.value_ent2 = Gtk.Entry()
        sel_list.attach_next_to(self.value_ent2, self.op_com2, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the precipitation type row.
        self.sel_chk3 = Gtk.CheckButton("Precipitation type ")
        sel_list.attach_next_to(self.sel_chk3, self.sel_chk2, Gtk.PositionType.BOTTOM, 1, 1)
        self.op_com3 = Gtk.ComboBoxText()
        for i in ["equal to", "not equal to"]:
            self.op_com3.append_text(i)
        self.op_com3.set_active(0)
        sel_list.attach_next_to(self.op_com3, self.sel_chk3, Gtk.PositionType.RIGHT, 1, 1)
        self.value_ent3 = Gtk.Entry()
        sel_list.attach_next_to(self.value_ent3, self.op_com3, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the wind speed row.
        self.sel_chk4 = Gtk.CheckButton("Wind speed ")
        sel_list.attach_next_to(self.sel_chk4, self.sel_chk3, Gtk.PositionType.BOTTOM, 1, 1)
        self.op_com4 = Gtk.ComboBoxText()
        for i in ["equal to", "not equal to", "greater than", "less than", "greater than or equal to", "less than or equal to", "between", "between (inclusive)", "outside", "outside (inclusive)"]:
            self.op_com4.append_text(i)
        self.op_com4.set_active(0)
        sel_list.attach_next_to(self.op_com4, self.sel_chk4, Gtk.PositionType.RIGHT, 1, 1)
        self.value_ent4 = Gtk.Entry()
        sel_list.attach_next_to(self.value_ent4, self.op_com4, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the wind direction row.
        self.sel_chk5 = Gtk.CheckButton("Wind direction ")
        sel_list.attach_next_to(self.sel_chk5, self.sel_chk4, Gtk.PositionType.BOTTOM, 1, 1)
        self.op_com5 = Gtk.ComboBoxText()
        for i in ["equal to", "not equal to"]:
            self.op_com5.append_text(i)
        self.op_com5.set_active(0)
        sel_list.attach_next_to(self.op_com5, self.sel_chk5, Gtk.PositionType.RIGHT, 1, 1)
        self.value_ent5 = Gtk.Entry()
        sel_list.attach_next_to(self.value_ent5, self.op_com5, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the humidity row.
        self.sel_chk6 = Gtk.CheckButton("Humidity ")
        sel_list.attach_next_to(self.sel_chk6, self.sel_chk5, Gtk.PositionType.BOTTOM, 1, 1)
        self.op_com6 = Gtk.ComboBoxText()
        for i in ["equal to", "not equal to", "greater than", "less than", "greater than or equal to", "less than or equal to", "between", "between (inclusive)", "outside", "outside (inclusive)"]:
            self.op_com6.append_text(i)
        self.op_com6.set_active(0)
        sel_list.attach_next_to(self.op_com6, self.sel_chk6, Gtk.PositionType.RIGHT, 1, 1)
        self.value_ent6 = Gtk.Entry()
        sel_list.attach_next_to(self.value_ent6, self.op_com6, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the air pressure row.
        self.sel_chk7 = Gtk.CheckButton("Air pressure ")
        sel_list.attach_next_to(self.sel_chk7, self.sel_chk6, Gtk.PositionType.BOTTOM, 1, 1)
        self.op_com7 = Gtk.ComboBoxText()
        for i in ["equal to", "not equal to", "greater than", "less than", "greater than or equal to", "less than or equal to", "between", "between (inclusive)", "outside", "outside (inclusive)"]:
            self.op_com7.append_text(i)
        self.op_com7.set_active(0)
        sel_list.attach_next_to(self.op_com7, self.sel_chk7, Gtk.PositionType.RIGHT, 1, 1)
        self.value_ent7 = Gtk.Entry()
        sel_list.attach_next_to(self.value_ent7, self.op_com7, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the air pressure change row.
        self.sel_chk8 = Gtk.CheckButton("Air pressure change ")
        sel_list.attach_next_to(self.sel_chk8, self.sel_chk7, Gtk.PositionType.BOTTOM, 1, 1)
        self.op_com8 = Gtk.ComboBoxText()
        for i in ["equal to", "not equal to"]:
            self.op_com8.append_text(i)
        self.op_com8.set_active(0)
        sel_list.attach_next_to(self.op_com8, self.sel_chk8, Gtk.PositionType.RIGHT, 1, 1)
        self.value_ent8 = Gtk.Entry()
        sel_list.attach_next_to(self.value_ent8, self.op_com8, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the cloud cover row.
        self.sel_chk9 = Gtk.CheckButton("Cloud cover ")
        sel_list.attach_next_to(self.sel_chk9, self.sel_chk8, Gtk.PositionType.BOTTOM, 1, 1)
        self.op_com9 = Gtk.ComboBoxText()
        for i in ["equal to", "not equal to"]:
            self.op_com9.append_text(i)
        self.op_com9.set_active(0)
        sel_list.attach_next_to(self.op_com9, self.sel_chk9, Gtk.PositionType.RIGHT, 1, 1)
        self.value_ent9 = Gtk.Entry()
        sel_list.attach_next_to(self.value_ent9, self.op_com9, Gtk.PositionType.RIGHT, 1, 1)
        """
        
        # Show the dialog.
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
        
        if field in self.used_fields:
            show_error_dialog(self, "Add Condition", "A condition for %s has already been entered." % field)
            return True
        return False
    
    
    def check_two(self, operator, value):
        """Checks if there are two values, if the operator requires that."""
        
        if operator == "Between" or operator ==  "Between (Inclusive)" or operator ==  "Outside" or \
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
        add_dlg.run()
        field = field_com.get_active_text()
        condition = cond_com.get_active_text()
        value = value_ent.get_text()
        
        # Validate the data, and add if it's acceptable.
        if not self.check_operator(field, condition) and not self.check_used(field) and not self.check_two(condition, value):
            self.liststore.append([field, condition, value])
            self.used_fields.append(field)
        
        # Close the dialog.
        add_dlg.destroy()
