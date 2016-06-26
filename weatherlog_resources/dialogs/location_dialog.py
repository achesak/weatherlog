# -*- coding: utf-8 -*-


# This file defines the dialog for entering a location.


# Import GTK for the dialog.
from gi.repository import Gtk


class LocationDialog(Gtk.Dialog):
    """Shows the dialog for entering a location."""
    
    def __init__(self, parent, config):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, "Get Current Weather", parent, Gtk.DialogFlags.MODAL)
        self.set_size_request(300, 0)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        loc_grid = Gtk.Grid()
        loc_grid.set_column_spacing(3)
        loc_grid.set_row_spacing(3)
        self.get_content_area().add(loc_grid)
        
        # Create the location type frame and radiobuttons.
        # Default to type set in options.
        type_frame = Gtk.Frame()
        type_frame.set_label("Location type")
        type_grid = Gtk.Grid()
        type_grid.set_column_spacing(5)
        type_grid.set_row_spacing(5)
        type_frame.add(type_grid)
        self.use_city_rbtn = Gtk.RadioButton.new_with_label_from_widget(None, "City")
        self.use_zip_rbtn = Gtk.RadioButton.new_with_label_from_widget(self.use_city_rbtn, "Zip code")
        if config["location_type"] == "city":
            self.use_city_rbtn.set_active(True)
        else:
            self.use_zip_rbtn.set_active(True)
        type_grid.add(self.use_city_rbtn)
        type_grid.attach_next_to(self.use_zip_rbtn, self.use_city_rbtn, Gtk.PositionType.BOTTOM, 1, 1)
        loc_grid.add(type_frame)
        
        # Create the frame and location entry.
        nam_frame = Gtk.Frame()
        nam_frame.set_label("Location")
        loc_grid.attach_next_to(nam_frame, type_frame, Gtk.PositionType.BOTTOM, 1, 1)
        self.nam_ent = Gtk.Entry()
        self.nam_ent.set_hexpand(True)
        nam_frame.add(self.nam_ent)
        
        # Connect 'Enter' key to the OK button.
        self.nam_ent.set_activates_default(True)
        ok_btn = self.get_widget_for_response(response_id = Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
