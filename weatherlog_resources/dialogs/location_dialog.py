# -*- coding: utf-8 -*-


# This file defines the dialog for specifying a location.


# Import GTK for the dialog.
from gi.repository import Gtk


class LocationDialog(Gtk.Dialog):
    """Shows the "Get Current Weather" dialog."""
    def __init__(self, parent, message):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Get Current Weather", parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        loc_box = self.get_content_area()
        loc_grid = Gtk.Grid()
        loc_box.add(loc_grid)
        
        # Create the label and entry.
        loc_lbl = Gtk.Label(message)
        loc_lbl.set_alignment(0, 0.5)
        loc_grid.add(loc_lbl)
        self.loc_ent = Gtk.Entry()
        loc_grid.attach_next_to(self.loc_ent, loc_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Connect 'Enter' key to the OK button.
        self.loc_ent.set_activates_default(True)
        ok_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
