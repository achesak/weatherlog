# -*- coding: utf-8 -*-


# This file defines the Add Profile dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class AddProfileDialog(Gtk.Dialog):
    """Shows the "Add Profile" dialog."""
    def __init__(self, parent):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Add Profile", parent, Gtk.DialogFlags.MODAL)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        new_box.add(new_grid)
        
        # Create the label and entry.
        add_lbl = Gtk.Label("Enter profile name: ")
        add_lbl.set_alignment(0, 0.5)
        new_grid.add(add_lbl)
        self.add_ent = Gtk.Entry()
        new_grid.attach_next_to(self.add_ent, add_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
