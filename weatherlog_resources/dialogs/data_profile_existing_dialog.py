# -*- coding: utf-8 -*-


# This file defines the Copy/Move to Existing Profile dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class ProfileDataExistingDialog(Gtk.Dialog):
    """Shows the "Copy/Move to Existing Profile" dialog."""
    def __init__(self, parent, profiles, mode):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "%s Data to Existing Profile" % mode, parent, Gtk.DialogFlags.MODAL)
        # Don't allow the user to resize the window.
        self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        pro_box = self.get_content_area()
        pro_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        pro_box.add(pro_grid)
        
        # Create the label and combobox.
        pro_lbl = Gtk.Label("Choose profile: ")
        pro_lbl.set_alignment(0, 0.5)
        pro_grid.add(pro_lbl)
        self.pro_com = Gtk.ComboBoxText()
        for i in profiles:
            self.pro_com.append_text(i)
        self.pro_com.set_active(0)
        pro_grid.attach_next_to(self.pro_com, pro_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
