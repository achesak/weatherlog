# -*- coding: utf-8 -*-


# This file defines the Copy/Move to New Profile dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class ProfileDataNewDialog(Gtk.Dialog):
    """Shows the "Copy/Move to New Profile" dialog."""
    def __init__(self, parent, mode):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "%s Data to New Profile" % mode, parent, Gtk.DialogFlags.MODAL)
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
        pro_lbl = Gtk.Label("Enter new profile name: ")
        pro_lbl.set_alignment(0, 0.5)
        new_grid.add(pro_lbl)
        self.pro_ent = Gtk.Entry()
        new_grid.attach_next_to(self.pro_ent, pro_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
