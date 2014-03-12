# -*- coding: utf-8 -*-


# This file defines the Rename Profile dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class RenameProfileDialog(Gtk.Dialog):
    """Shows the "Rename Profile" dialog."""
    def __init__(self, parent):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Rename Profile", parent, Gtk.DialogFlags.MODAL)
        # Don't allow the user to resize the window.
        self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        new_box.add(new_grid)
        
        # Create the label and entry.
        ren_lbl = Gtk.Label("Enter new profile name: ")
        ren_lbl.set_alignment(0, 0.5)
        new_grid.add(ren_lbl)
        self.ren_ent = Gtk.Entry()
        new_grid.attach_next_to(self.ren_ent, ren_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
