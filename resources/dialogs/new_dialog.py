# -*- coding: utf-8 -*-


# This file defines the Add New dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class AddNewDialog(Gtk.Dialog):
    """Shows the "Add New" dialog."""
    def __init__(self, parent):
        """Create the dialog."""
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Add New", parent, Gtk.DialogFlags.MODAL)
        
        # Add the buttons.
        self.add_button("OK", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        
        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        new_box.add(new_grid)
        
        # Create the Date label and entry. Replace with a proper datepicker later?
        date_lbl = Gtk.Label("Date: ")
        date_lbl.set_alignment(0, 0.5)
        new_grid.add(date_lbl)
        self.date_ent = Gtk.Entry()
        new_grid.attach_next_to(self.date_ent, date_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Temperature label and entry.
        temp_lbl = Gtk.Label("Temperature (°C): ")
        temp_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(temp_lbl, date_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.temp_ent = Gtk.Entry()
        new_grid.attach_next_to(self.temp_ent, temp_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Precipitation label, entry, and combobox.
        prec_lbl = Gtk.Label("Precipitation (cm): ")
        prec_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(prec_lbl, temp_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.prec_ent = Gtk.Entry()
        new_grid.attach_next_to(self.prec_ent, prec_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.prec_com = Gtk.ComboBoxText()
        for i in ["Rain", "Snow", "Hail", "Sleet"]:
            self.prec_com.append_text(i)
        new_grid.attach_next_to(self.prec_com, self.prec_ent, Gtk.PositionType.RIGHT, 1, 1)
        # Create the Wind label, entry, and combobox.
        wind_lbl = Gtk.Label("Wind (kph): ")
        wind_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(wind_lbl, prec_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.wind_ent = Gtk.Entry()
        new_grid.attach_next_to(self.wind_ent, wind_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.wind_com = Gtk.ComboBoxText()
        for i in ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]:
            self.wind_com.append_text(i)
        new_grid.attach_next_to(self.wind_com, self.wind_ent, Gtk.PositionType.RIGHT, 1, 1)
        # Create the Humidity label and entry.
        humi_lbl = Gtk.Label("Humidity (%): ")
        humi_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(humi_lbl, wind_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.humi_ent = Gtk.Entry()
        new_grid.attach_next_to(self.humi_ent, humi_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Air Pressure label and entry.
        airp_lbl = Gtk.Label("Air Pressure (Pa): ")
        airp_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(airp_lbl, humi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.airp_ent = Gtk.Entry()
        new_grid.attach_next_to(self.airp_ent, airp_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Cloud Cover label and combobox.
        clou_lbl = Gtk.Label("Cloud Cover: ")
        clou_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(clou_lbl, airp_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.clou_com = Gtk.ComboBoxText()
        for i in ["Sunny", "Mostly Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy"]:
            self.clou_com.append_text(i)
        new_grid.attach_next_to(self.clou_com, clou_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Notes label and entry.
        note_lbl = Gtk.Label("Notes: ")
        note_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(note_lbl, clou_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.note_ent = Gtk.Entry()
        new_grid.attach_next_to(self.note_ent, note_lbl, Gtk.PositionType.RIGHT, 2, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()