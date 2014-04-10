# -*- coding: utf-8 -*-


# This file defines the advanced dialog for selecting data.


# Import GTK for the dialog.
from gi.repository import Gtk


class SelectDataAdvancedDialog(Gtk.Dialog):
    """Shows the advanced data selection dialog."""
    def __init__(self, parent):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Select Data", parent, Gtk.DialogFlags.MODAL)
        # Don't allow the user to resize the window.
        self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        sel_box = self.get_content_area()
        sel_grid = Gtk.Grid()
        sel_box.add(sel_grid)
        
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
        # Create the labels, comboboxes, and entry.
        sel_lbl1 = Gtk.Label("Select ")
        sel_lbl1.set_alignment(0, 0.5)
        sel_grid.add(sel_lbl1)
        self.field_com = Gtk.ComboBoxText()
        for i in ["temperature", "precipitation amount", "precipitation type", "wind speed", "wind direction", "humidity", "air pressure", "air pressure change", "cloud cover"]:
            self.field_com.append_text(i)
        self.field_com.set_active(0)
        sel_grid.attach_next_to(self.field_com, sel_lbl1, Gtk.PositionType.RIGHT, 1, 1)
        sel_lbl2 = Gtk.Label(" that is ")
        sel_lbl2.set_alignment(0, 0.5)
        sel_grid.attach_next_to(sel_lbl2, self.field_com, Gtk.PositionType.RIGHT, 1, 1)
        self.op_com = Gtk.ComboBoxText()
        for i in ["equal to", "not equal to", "greater than", "less than", "greater than or equal to", "less than or equal to", "between", "between (inclusive)", "outside", "outside (inclusive)"]:
            self.op_com.append_text(i)
        self.op_com.set_active(0)
        sel_grid.attach_next_to(self.op_com, sel_lbl2, Gtk.PositionType.RIGHT, 1, 1)
        self.value_ent = Gtk.Entry()
        sel_grid.attach_next_to(self.value_ent, self.op_com, Gtk.PositionType.RIGHT, 1, 1)
        """
        # Show the dialog.
        self.show_all()
