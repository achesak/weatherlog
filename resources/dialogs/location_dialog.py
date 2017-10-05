# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/location_dialog.py
# This dialog enters a location.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk


class LocationDialog(Gtk.Dialog):
    """Shows the dialog for entering a location."""
    
    def __init__(self, parent, config):
        """Create the dialog."""
        
        Gtk.Dialog.__init__(self, "Get Current Weather", parent, Gtk.DialogFlags.MODAL, use_header_bar=True)
        self.set_size_request(400, 0)
        self.add_button("OK", Gtk.ResponseType.OK)

        # Create the header bar.
        header = self.get_header_bar()
        header.set_title("Get Current Weather")
        header.set_subtitle("Enter location")
        header.set_show_close_button(True)
        
        # Create the grid.
        loc_grid = Gtk.Grid()
        loc_grid.set_column_spacing(3)
        loc_grid.set_row_spacing(3)
        self.get_content_area().add(loc_grid)

        # Create the frame and location entry.
        self.nam_ent = Gtk.Entry()
        self.nam_ent.set_placeholder_text("Location")
        self.nam_ent.set_hexpand(True)
        loc_grid.add(self.nam_ent)
        
        # Create the location type frame and radiobuttons; default to type set in options.
        type_grid = Gtk.Grid()
        type_grid.set_column_spacing(5)
        type_grid.set_row_spacing(5)
        type_grid.set_margin_top(5)
        type_grid.set_margin_bottom(5)
        type_grid.set_margin_right(5)
        type_grid.set_margin_left(5)
        type_lbl = Gtk.Label("Location is a...")
        type_lbl.set_alignment(0, 0.5)
        type_lbl.set_margin_right(20)
        self.use_city_rbtn = Gtk.RadioButton.new_with_label_from_widget(None, "City")
        self.use_city_rbtn.set_margin_right(20)
        self.use_zip_rbtn = Gtk.RadioButton.new_with_label_from_widget(self.use_city_rbtn, "Zip code")
        if config["location_type"] == "city":
            self.use_city_rbtn.set_active(True)
        else:
            self.use_zip_rbtn.set_active(True)
        type_grid.add(type_lbl)
        type_grid.attach_next_to(self.use_city_rbtn, type_lbl, Gtk.PositionType.RIGHT, 1, 1)
        type_grid.attach_next_to(self.use_zip_rbtn, self.use_city_rbtn, Gtk.PositionType.RIGHT, 1, 1)
        loc_grid.attach_next_to(type_grid, self.nam_ent, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Connect 'Enter' key to the OK button.
        self.nam_ent.set_activates_default(True)
        ok_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
