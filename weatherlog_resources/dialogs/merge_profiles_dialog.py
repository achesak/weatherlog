# -*- coding: utf-8 -*-


# This file defines the Merge Profiles dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class MergeProfilesDialog(Gtk.Dialog):
    """Shows the "Merge Profiles" dialog."""
    def __init__(self, parent, profiles):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Merge Profiles", parent, Gtk.DialogFlags.MODAL)
        # Don't allow the user to resize the window.
        self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        mer_box = self.get_content_area()
        mer_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        mer_box.add(mer_grid)
        
        # Create the label and combobox.
        mer_lbl = Gtk.Label("Choose profile: ")
        mer_lbl.set_alignment(0, 0.5)
        mer_grid.add(mer_lbl)
        self.mer_com = Gtk.ComboBoxText()
        for i in profiles:
            self.mer_com.append_text(i)
        self.mer_com.set_active(0)
        mer_grid.attach_next_to(self.mer_com, mer_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
