# -*- coding: utf-8 -*-


# This file defines the dialog for specifying a location.


# Import GTK for the dialog.
from gi.repository import Gtk


class LocationDialog(Gtk.Dialog):
    """Shows the "Get Current Weather" dialog."""
    
    def __init__(self, parent, message):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, "Get Current Weather", parent, Gtk.DialogFlags.MODAL)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the frame.
        loc_frame = Gtk.Frame()
        loc_frame.set_label(message)
        self.get_content_area().add(loc_frame)
        
        # Create the entry.
        self.loc_ent = Gtk.Entry()
        loc_frame.add(self.loc_ent)
        
        # Connect 'Enter' key to the OK button.
        self.loc_ent.set_activates_default(True)
        ok_btn = self.get_widget_for_response(response_id = Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
