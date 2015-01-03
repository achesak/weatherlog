# -*- coding: utf-8 -*-


# This file defines the Edit dialog.


# Import GTK for the dialog.
from gi.repository import Gtk
# Import the dialogs.
from weatherlog_resources.dialogs.misc_dialogs import *


class EditDialog(Gtk.Dialog):
    """Shows the "Edit" dialog."""
    def __init__(self, parent, profile, data, date, units):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Edit %s - %s" % (date, profile), parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        new_box.add(new_grid)
        
        # Create the Date label and calendar.
        date_lbl = Gtk.Label("Date: ")
        date_lbl.set_alignment(0, 0.5)
        new_grid.add(date_lbl)
        self.date_ent = Gtk.Entry()
        self.date_ent.set_text(date)
        self.date_ent.set_editable(False)
        new_grid.attach_next_to(self.date_ent, date_lbl, Gtk.PositionType.RIGHT, 2, 1)
        
        # Create the Temperature label and spinbutton.
        temp_lbl = Gtk.Label("Temperature (%s): " % units["temp"])
        temp_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(temp_lbl, date_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        if units["temp"] == "°C":
            temp_adj = Gtk.Adjustment(lower = -100, upper = 100, step_increment = 1)
        else:
            temp_adj = Gtk.Adjustment(lower = -150, upper = 150, step_increment = 1)
        self.temp_sbtn = Gtk.SpinButton(digits = 2, adjustment = temp_adj)
        self.temp_sbtn.set_numeric(False)
        self.temp_sbtn.set_value(0)
        new_grid.attach_next_to(self.temp_sbtn, temp_lbl, Gtk.PositionType.RIGHT, 2, 1)
        
        # Create the Precipitation label, spinbutton, and combobox.
        prec_lbl = Gtk.Label("Precipitation (%s): " % units["prec"])
        prec_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(prec_lbl, temp_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        prec_adj = Gtk.Adjustment(lower = 0, upper = 100, step_increment = 1)
        self.prec_sbtn = Gtk.SpinButton(digits = 2, adjustment = prec_adj)
        self.prec_sbtn.set_numeric(False)
        self.prec_sbtn.set_value(0)
        self.prec_sbtn.set_sensitive(False)
        new_grid.attach_next_to(self.prec_sbtn, prec_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.prec_com = Gtk.ComboBoxText()
        for i in ["None", "Rain", "Snow", "Hail", "Sleet"]:
            self.prec_com.append_text(i)
        self.prec_com.set_active(0)
        new_grid.attach_next_to(self.prec_com, self.prec_sbtn, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Wind label, spinbutton, and combobox.
        wind_lbl = Gtk.Label("Wind (%s): " % units["wind"])
        wind_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(wind_lbl, prec_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        wind_adj = Gtk.Adjustment(lower = 0, upper = 500, step_increment = 1)
        self.wind_sbtn = Gtk.SpinButton(digits = 2, adjustment = wind_adj)
        self.wind_sbtn.set_numeric(False)
        self.wind_sbtn.set_value(0)
        self.wind_sbtn.set_sensitive(False)
        new_grid.attach_next_to(self.wind_sbtn, wind_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.wind_com = Gtk.ComboBoxText()
        for i in ["None", "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]:
            self.wind_com.append_text(i)
        self.wind_com.set_active(0)
        new_grid.attach_next_to(self.wind_com, self.wind_sbtn, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Humidity label and spinbutton.
        humi_lbl = Gtk.Label("Humidity (%): ")
        humi_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(humi_lbl, wind_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        humi_adj = Gtk.Adjustment(lower = 0, upper = 100, step_increment = 1)
        self.humi_sbtn = Gtk.SpinButton(digits = 2, adjustment = humi_adj)
        self.humi_sbtn.set_numeric(False)
        self.humi_sbtn.set_value(0)
        new_grid.attach_next_to(self.humi_sbtn, humi_lbl, Gtk.PositionType.RIGHT, 2, 1)
        
        # Create the Air Pressure label, spinbutton, and combobox.
        airp_lbl = Gtk.Label("Air Pressure (%s): " % units["airp"])
        airp_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(airp_lbl, humi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        airp_adj = Gtk.Adjustment(lower = 0, upper = 2000, step_increment = 1)
        self.airp_sbtn = Gtk.SpinButton(digits = 2, adjustment = airp_adj)
        self.airp_sbtn.set_numeric(False)
        self.airp_sbtn.set_value(0)
        new_grid.attach_next_to(self.airp_sbtn, airp_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.airp_com = Gtk.ComboBoxText()
        for i in ["Steady", "Rising", "Falling"]:
            self.airp_com.append_text(i)
        self.airp_com.set_active(0)
        new_grid.attach_next_to(self.airp_com, self.airp_sbtn, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Cloud Cover label and combobox.
        clou_lbl = Gtk.Label("Cloud Cover: ")
        clou_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(clou_lbl, airp_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.clou_com = Gtk.ComboBoxText()
        for i in ["Sunny", "Mostly Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy"]:
            self.clou_com.append_text(i)
        self.clou_com.set_active(0)
        new_grid.attach_next_to(self.clou_com, clou_lbl, Gtk.PositionType.RIGHT, 2, 1)
        
        # Create the Notes label and entry.
        note_lbl = Gtk.Label("Notes: ")
        note_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(note_lbl, clou_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.note_ent = Gtk.Entry()
        new_grid.attach_next_to(self.note_ent, note_lbl, Gtk.PositionType.RIGHT, 2, 1)
        
        # Bind the events for enabling the comboboxes.
        self.prec_com.connect("changed", self.enable_prec)
        self.wind_com.connect("changed", self.enable_wind)
        
        # Set the values.
        self.temp_sbtn.set_value(float(data[1]))
        if data[2] != "None":
            d2 = data[2].split(" ")
            prec_list = ["None", "Rain", "Snow", "Hail", "Sleet"]
            for i in range(0, len(prec_list)):
                if d2[1] == prec_list[i]:
                    self.prec_com.set_active(i)
                    break
            self.prec_sbtn.set_value(float(d2[0]))
        if data[3] != "None":
            d3 = data[3].split(" ")
            wind_list = ["None", "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
            for i in range(0, len(wind_list)):
                if d3[1] == wind_list[i]:
                    self.wind_com.set_active(i)
                    break
            self.wind_sbtn.set_value(float(d3[0]))
        self.humi_sbtn.set_value(float(data[4]))
        d5 = data[5].split(" ")
        airp_list = ["Steady", "Rising", "Falling"]
        for i in range(0, len(airp_list)):
            if d5[1] == airp_list[i]:
                self.airp_com.set_active(i)
                break
        self.airp_sbtn.set_value(float(d5[0]))
        clou_list = ["Sunny", "Mostly Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy"]
        for i in range(0, len(clou_list)):
            if data[6] == clou_list[i]:
                self.clou_com.set_active(i)
                break
        self.note_ent.set_text(data[7])
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
        
    
    def enable_prec(self, widget):
        """Enable or disable the precipitation spinbutton."""
        
        # If the value is None, disable the spinbutton.
        if widget.get_active_text() == "None":
            self.prec_sbtn.set_sensitive(False)
        
		# Otherwise, enable the spinbutton.
        else:
            self.prec_sbtn.set_sensitive(True)
    
    
    def enable_wind(self, widget):
        """Enable or disable the wind spinbutton."""
        
        # If the value is None, disable the spinbutton.
        if widget.get_active_text() == "None":
            self.wind_sbtn.set_sensitive(False)
        
        # Otherwise, enable the spinbutton.
        else:
            self.wind_sbtn.set_sensitive(True)
