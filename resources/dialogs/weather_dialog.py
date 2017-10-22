# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/weather_dialog.py
# This dialog displays the current weather conditions, location, and forecast.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk

# Import application modules.
import resources.get_weather as get_weather
from resources.dialogs.misc_dialogs import *

# Import URLError for error checking
try:
    from urllib2 import URLError
except ImportError:
    from urllib.request import URLError


class CurrentWeatherDialog(Gtk.Dialog):
    """Shows the current weather dialog."""
    
    def __init__(self, parent, title, config, units, weather_codes):
        """Create the dialog."""
        
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL, use_header_bar=True)
        self.set_default_size(600, 700)

        self.config = config
        self.units = units
        self.weather_codes = weather_codes
        location = "No location specified"
        location_type = self.config["location_type"]
        if self.config["location_type"] == "city" and self.config["city"].lstrip().rstrip():
            location = self.config["city"].lstrip().rstrip()
        elif self.config["location_type"] == "zip" and self.config["zipcode"].lstrip().rstrip():
            location = self.config["zipcode"].lstrip().rstrip()

        # Create the location entry grid.
        loc_frame = Gtk.Frame()
        loc_frame.set_label("Location")
        loc_frame.set_border_width(10)
        loc_grid = Gtk.Grid()
        loc_grid.set_column_spacing(5)
        loc_grid.set_row_spacing(5)
        loc_frame.add(loc_grid)
        self.get_content_area().add(loc_frame)

        # Create the location entry and button.
        self.nam_ent = Gtk.Entry()
        self.nam_ent.set_placeholder_text("Location")
        self.nam_ent.set_hexpand(True)
        self.nam_ent.set_margin_left(5)
        self.nam_ent.set_margin_top(5)
        self.nam_btn = Gtk.Button(label="Get Weather")
        self.nam_btn.set_margin_top(5)
        self.nam_btn.set_margin_right(5)
        loc_grid.add(self.nam_ent)
        loc_grid.attach_next_to(self.nam_btn, self.nam_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Create the location type frame and radiobuttons; default to type set in options.
        type_grid = Gtk.Grid()
        type_grid.set_column_spacing(5)
        type_grid.set_row_spacing(5)
        type_grid.set_border_width(5)
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

        # Create the stack.
        stack = Gtk.Stack()
        stack.set_hexpand(True)
        stack.set_vexpand(True)
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.get_content_area().add(stack)
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        
        # Tab 1: Weather info.
        wea_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.wea_img = Gtk.Image()
        self.wea_img.props.halign = Gtk.Align.CENTER
        self.wea_img.set_hexpand(True)
        wea_box.add(self.wea_img)
        self.wea_loc_lbl = Gtk.Label()
        self.wea_loc_lbl.set_margin_bottom(20)
        self.wea_loc_lbl.props.halign = Gtk.Align.CENTER
        self.wea_loc_lbl.set_hexpand(True)
        wea_box.pack_start(self.wea_loc_lbl, False, False, 0)
        self.wea_list = Gtk.ListStore(str, str)
        self.wea_tree = Gtk.TreeView(model=self.wea_list)
        self.wea_tree.set_headers_visible(False)
        self.wea_tree.set_hexpand(True)
        wea_field_text = Gtk.CellRendererText()
        wea_field_col = Gtk.TreeViewColumn("Field", wea_field_text, text=0)
        wea_field_col.set_min_width(150)
        wea_field_col.set_expand(True)
        self.wea_tree.append_column(wea_field_col)
        wea_value_text = Gtk.CellRendererText()
        wea_value_col = Gtk.TreeViewColumn("Value", wea_value_text, text=1)
        wea_value_col.set_expand(True)
        self.wea_tree.append_column(wea_value_col)
        wea_win = Gtk.ScrolledWindow()
        wea_win.set_hexpand(True)
        wea_win.set_vexpand(True)
        wea_win.add(self.wea_tree)
        wea_box.pack_end(wea_win, True, True, 0)
        
        # Tab 2: Forecast info.
        for_box = Gtk.Box()
        self.for_list = Gtk.ListStore(str, str)
        self.for_tree = Gtk.TreeView(model=self.for_list)
        self.for_tree.set_headers_visible(False)
        for_field_text = Gtk.CellRendererText()
        for_field_col = Gtk.TreeViewColumn("Field", for_field_text, text=0)
        for_field_col.set_min_width(150)
        for_field_col.set_expand(True)
        self.for_tree.append_column(for_field_col)
        for_value_text = Gtk.CellRendererText()
        for_value_col = Gtk.TreeViewColumn("Value", for_value_text, text=1)
        for_value_col.set_expand(True)
        self.for_tree.append_column(for_value_col)
        for_box.pack_start(self.for_tree, fill=True, expand=True, padding=0)
        for_win = Gtk.ScrolledWindow()
        for_win.set_hexpand(True)
        for_win.set_vexpand(True)
        for_win.add(for_box)

        # Create the header bar.
        header = self.get_header_bar()
        header.set_show_close_button(True)
        header.set_custom_title(stack_switcher)

        # Set up the stack.
        stack.add_titled(wea_box, "weather", "Weather")
        stack.add_titled(for_win, "forecast", "Forecast")

        # Get the data
        if not location.endswith("specified"):
            self.get_weather(location, location_type)

        # Bind the events.
        self.nam_btn.connect("clicked", lambda x: self.get_weather())
        self.nam_ent.connect("activate", lambda x: self.get_weather())
        
        # Show the dialog.
        self.show_all()

    def get_weather(self, location="", location_type=""):
        """Gets the current weather."""

        # Get the location and location type.
        if not location:
            location = self.nam_ent.get_text().lstrip().rstrip()
            location_type = "city" if self.use_city_rbtn.get_active() else "zip"

        # Get the weather data.
        try:
            city, data, location, prefill_data, code = get_weather.get_weather(self.config, self.units, self.weather_codes,
                                                                     location, location_type)
            image_url = get_weather.get_weather_image(code)
        except (URLError, ValueError):
            show_error_dialog(self, "Get Current Weather", "Cannot get current weather; no internet connection or invalid location.")
            return

        # Add the data.
        self.wea_list.clear()
        self.for_list.clear()
        for i in data[0]:
            self.wea_list.append(i)
        for i in data[1]:
            self.for_list.append(i)

        self.wea_loc_lbl.set_markup("<big>" + location + "</big>")
        self.wea_img.set_from_file(image_url)
