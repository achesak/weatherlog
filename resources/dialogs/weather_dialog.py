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
from resources.constants import *


class CurrentWeatherDialog(Gtk.Dialog):
    """Shows the current weather dialog."""
    
    def __init__(self, parent, title, data, image_path):
        """Create the dialog."""
        
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(600, 700)
        self.add_button("Add", DialogResponse.ADD_DATA)
        self.add_button("Export", DialogResponse.EXPORT)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the tab notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        info_box = self.get_content_area()
        
        # Tab 1: Weather info.
        wea_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        wea_box_lbl = Gtk.Label("Weather")
        wea_img = Gtk.Image.new_from_file(image_path)
        wea_img.props.halign = Gtk.Align.CENTER
        wea_img.set_hexpand(True)
        wea_box.add(wea_img)
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
        wea_box.pack_end(self.wea_tree, True, True, 0)
        wea_win = Gtk.ScrolledWindow()
        wea_win.set_hexpand(True)
        wea_win.set_vexpand(True)
        wea_win.add(wea_box)
        
        # Tab 2: Forecast info.
        for_box = Gtk.Box()
        for_box_lbl = Gtk.Label("Forecast")
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
        
        # Add the tabs to the notebook.
        notebook.append_page(wea_win, wea_box_lbl)
        notebook.append_page(for_win, for_box_lbl)
        info_box.add(notebook)
        
        # Add the data.
        for i in data[0]:
            self.wea_list.append(i)
        for i in data[1]:
            self.for_list.append(i)
        
        # Show the dialog.
        self.show_all()
