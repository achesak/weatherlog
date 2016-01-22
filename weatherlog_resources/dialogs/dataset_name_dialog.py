# -*- coding: utf-8 -*-


# This file defines the generic dialog for entering a dataset name.


# Import GTK for the dialog.
from gi.repository import Gtk


class DatasetNameDialog(Gtk.Dialog):
    """Shows the dialog for adding a dataset."""
    
    def __init__(self, parent, title, message = "Enter dataset name:"):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the frame.
        nam_frame = Gtk.Frame()
        nam_frame.set_label(message)
        self.get_content_area().add(nam_frame)
        
        # Create the label and entry.
        self.nam_ent = Gtk.Entry()
        nam_frame.add(self.nam_ent)
        
        # Connect 'Enter' key to the OK button.
        self.nam_ent.set_activates_default(True)
        ok_btn = self.get_widget_for_response(response_id = Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
