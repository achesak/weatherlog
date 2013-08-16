# -*- coding: utf-8 -*-


# This file defines the Add New dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class OptionsDialog(Gtk.Dialog):
    """Shows the "Options" dialog."""
    def __init__(self, parent, config):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Options", parent, Gtk.DialogFlags.MODAL)
        
        # Add the buttons.
        self.add_button("OK", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        
        # Create the grid.
        opt_box = self.get_content_area()
        opt_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        opt_box.add(opt_grid)
        
        # Create the pre-fill data checkbox.
        self.pre_chk = Gtk.CheckButton("Pre-fill data")
        self.pre_chk.set_active(config["pre-fill"])
        opt_grid.attach(self.pre_chk, 0, 0, 2, 1)
        
        # Create the restore window size checkbox.
        self.win_chk = Gtk.CheckButton("Restore window size")
        self.win_chk.set_active(config["restore"])
        opt_grid.attach_next_to(self.win_chk, self.pre_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the location label and entry.
        loc_lbl = Gtk.Label("Location: ")
        loc_lbl.set_alignment(0, 0.5)
        opt_grid.attach_next_to(loc_lbl, self.win_chk, Gtk.PositionType.BOTTOM, 1, 1)
        self.loc_ent = Gtk.Entry()
        self.loc_ent.set_max_length(5)
        self.loc_ent.connect("changed", self.filter_numbers)
        self.loc_ent.set_text(config["location"])
        opt_grid.attach_next_to(self.loc_ent, loc_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Units label and combobox.
        unit_lbl = Gtk.Label("Units: ")
        unit_lbl.set_alignment(0, 0.5)
        opt_grid.attach_next_to(unit_lbl, loc_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.unit_com = Gtk.ComboBoxText()
        for i in ["Metric", "Imperial"]:
            self.unit_com.append_text(i)
        self.unit_com.set_active(["Metric", "Imperial"].index(config["units"].title()))
        opt_grid.attach_next_to(self.unit_com, unit_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
    
    
    def filter_numbers(self, event):
        """Filters non-numbers out of the entry."""
        
        # Get the text.
        text = self.loc_ent.get_text()
        
        # Only allow numbers. Filter out any other characters.
        self.loc_ent.set_text("".join([i for i in text if i in "0123456789"]))
