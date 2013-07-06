# -*- coding: utf-8 -*-


# This file defines the Switch Profile dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class SwitchProfileDialog(Gtk.Dialog):
    """Shows the "Switch Profile" dialog."""
    def __init__(self, parent, profiles):
        """Create the dialog."""
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Switch Profile", parent, Gtk.DialogFlags.MODAL)
        
        # Add the buttons.
        self.add_button("OK", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        
        # Create the grid.
        swi_box = self.get_content_area()
        swi_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        swi_box.add(swi_grid)
        
        # Create the label and combobox.
        swi_lbl = Gtk.Label("Choose profile: ")
        swi_lbl.set_alignment(0, 0.5)
        swi_grid.add(swi_lbl)
        self.swi_com = Gtk.ComboBoxText()
        for i in profiles:
            self.swi_com.append_text(i)
        self.swi_com.set_active(0)
        swi_grid.attach_next_to(self.swi_com, swi_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()