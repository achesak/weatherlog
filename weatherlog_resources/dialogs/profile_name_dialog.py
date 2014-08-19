# -*- coding: utf-8 -*-


# This file defines the generic dialog for entering a profile name.


# Import GTK for the dialog.
from gi.repository import Gtk


class ProfileNameDialog(Gtk.Dialog):
    """Shows the "Add Profile" dialog."""
    def __init__(self, parent, title):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        nam_box = self.get_content_area()
        nam_grid = Gtk.Grid()
        nam_box.add(nam_grid)
        
        # Create the label and entry.
        nam_lbl = Gtk.Label("Enter profile name: ")
        nam_lbl.set_alignment(0, 0.5)
        nam_grid.add(nam_lbl)
        self.nam_ent = Gtk.Entry()
        nam_grid.attach_next_to(self.nam_ent, nam_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()