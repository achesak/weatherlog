# -*- coding: utf-8 -*-


# This file defines the Remove Profile dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class RemoveProfileDialog(Gtk.Dialog):
    """Shows the "Remove Profile" dialog."""
    def __init__(self, parent, profiles):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Remove Profile", parent, Gtk.DialogFlags.MODAL)
        
        # Add the buttons.
        self.add_button("OK", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        
        # Create the grid.
        rem_box = self.get_content_area()
        rem_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        rem_box.add(rem_grid)
        
        # Create the label and combobox.
        rem_lbl = Gtk.Label("Choose profile: ")
        rem_lbl.set_alignment(0, 0.5)
        rem_grid.add(rem_lbl)
        self.rem_com = Gtk.ComboBoxText()
        for i in profiles:
            self.rem_com.append_text(i)
        self.rem_com.set_active(0)
        rem_grid.attach_next_to(self.rem_com, rem_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
