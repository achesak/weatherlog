# -*- coding: utf-8 -*-


# This file defines the simple dialog for selecting data.


# Import GTK for the dialog.
from gi.repository import Gtk


class SelectDataSimpleDialog(Gtk.Dialog):
    """Shows the simple data selection dialog."""
    def __init__(self, parent, profile):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Select Data - %s" % profile, parent, Gtk.DialogFlags.MODAL)
        # Don't allow the user to resize the window.
        self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        sel_box = self.get_content_area()
        sel_grid = Gtk.Grid()
        sel_box.add(sel_grid)
        
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
        
        # Show the dialog.
        self.show_all()
