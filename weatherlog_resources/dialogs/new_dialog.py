# -*- coding: utf-8 -*-


# This file defines the Add New dialog.


# Import GTK for the dialog.
from gi.repository import Gtk
# Import the dialogs.
from weatherlog_resources.dialogs.misc_dialogs import *
# Import pywapi to pre-fill the fields.
import weatherlog_resources.dialogs.pywapi.pywapi as pywapi
# Import function to convert degrees to a wind direction.
from .. import utility_functions


class AddNewDialog(Gtk.Dialog):
    """Shows the "Add New" dialog."""
    def __init__(self, parent, profile, user_location, prefill, show_prefill_dlg, units, prefill_data = []):
        """Create the dialog."""
        
        # Determine the default units.
        unit = 0
        if units["prec"] == "in":
            unit = 1
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Add New - %s" % profile, parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        
        # Create the tab notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grids.
        new_box = self.get_content_area()
        new_grid1 = Gtk.Grid()
        new_grid2 = Gtk.Grid()
        new_grid3 = Gtk.Grid()
        new_grid1_lbl = Gtk.Label("Date")
        new_grid2_lbl = Gtk.Label("Data 1")
        new_grid3_lbl = Gtk.Label("Data 2")
        
        # Date entry
        date_lbl = Gtk.Label("Date: ")
        date_lbl.set_alignment(0, 0.5)
        new_grid1.add(date_lbl)
        self.date_cal = Gtk.Calendar()
        new_grid1.attach_next_to(self.date_cal, date_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Temperature entry
        temp_lbl = Gtk.Label("Temperature: ")
        temp_lbl.set_alignment(0, 0.5)
        new_grid2.add(temp_lbl)
        if units["temp"] == "°C":
            temp_adj = Gtk.Adjustment(lower = -100, upper = 100, step_increment = 1)
        else:
            temp_adj = Gtk.Adjustment(lower = -150, upper = 150, step_increment = 1)
        self.temp_sbtn = Gtk.SpinButton(digits = 2, adjustment = temp_adj)
        self.temp_sbtn.set_numeric(False)
        self.temp_sbtn.set_value(0)
        new_grid2.attach_next_to(self.temp_sbtn, temp_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.temp_unit = Gtk.ComboBoxText()
        for i in ["°C", "°F"]:
            self.temp_unit.append_text(i)
        self.temp_unit.set_active(unit)
        new_grid2.attach_next_to(self.temp_unit, self.temp_sbtn, Gtk.PositionType.RIGHT, 1, 1)
        
        # Wind Chill entry
        chil_lbl = Gtk.Label("Wind Chill: ")
        chil_lbl.set_alignment(0, 0.5)
        new_grid2.attach_next_to(chil_lbl, temp_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        if units["temp"] == "°C":
            chil_adj = Gtk.Adjustment(lower = -100, upper = 100, step_increment = 1)
        else:
            chil_adj = Gtk.Adjustment(lower = -150, upper = 150, step_increment = 1)
        self.chil_sbtn = Gtk.SpinButton(digits = 2, adjustment = chil_adj)
        self.chil_sbtn.set_numeric(False)
        self.chil_sbtn.set_value(0)
        new_grid2.attach_next_to(self.chil_sbtn, chil_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.chil_unit = Gtk.ComboBoxText()
        for i in ["°C", "°F"]:
            self.chil_unit.append_text(i)
        self.chil_unit.set_active(unit)
        new_grid2.attach_next_to(self.chil_unit, self.chil_sbtn, Gtk.PositionType.RIGHT, 1, 1)
        
        # Precipitation entry
        prec_lbl = Gtk.Label("Precipitation: ")
        prec_lbl.set_alignment(0, 0.5)
        new_grid2.attach_next_to(prec_lbl, chil_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        prec_adj = Gtk.Adjustment(lower = 0, upper = 100, step_increment = 1)
        self.prec_sbtn = Gtk.SpinButton(digits = 2, adjustment = prec_adj)
        self.prec_sbtn.set_numeric(False)
        self.prec_sbtn.set_value(0)
        new_grid2.attach_next_to(self.prec_sbtn, prec_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.prec_unit = Gtk.ComboBoxText()
        for i in ["cm", "in"]:
            self.prec_unit.append_text(i)
        self.prec_unit.set_active(unit)
        new_grid2.attach_next_to(self.prec_unit, self.prec_sbtn, Gtk.PositionType.RIGHT, 1, 1)
        
        # Precipitation Type entry
        prec_lbl2 = Gtk.Label("Precipitation Type: ")
        prec_lbl2.set_alignment(0, 0.5)
        new_grid2.attach_next_to(prec_lbl2, prec_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.prec_com = Gtk.ComboBoxText()
        for i in ["None", "Rain", "Snow", "Hail", "Sleet"]:
            self.prec_com.append_text(i)
        self.prec_com.set_active(0)
        new_grid2.attach_next_to(self.prec_com, prec_lbl2, Gtk.PositionType.RIGHT, 2, 1)
        
        # Wind Speed entry
        wind_lbl = Gtk.Label("Wind Speed: ")
        wind_lbl.set_alignment(0, 0.5)
        new_grid2.attach_next_to(wind_lbl, prec_lbl2, Gtk.PositionType.BOTTOM, 1, 1)
        wind_adj = Gtk.Adjustment(lower = 0, upper = 500, step_increment = 1)
        self.wind_sbtn = Gtk.SpinButton(digits = 2, adjustment = wind_adj)
        self.wind_sbtn.set_numeric(False)
        self.wind_sbtn.set_value(0)
        new_grid2.attach_next_to(self.wind_sbtn, wind_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.wind_unit = Gtk.ComboBoxText()
        for i in ["kph", "mph"]:
            self.wind_unit.append_text(i)
        self.wind_unit.set_active(unit)
        new_grid2.attach_next_to(self.wind_unit, self.wind_sbtn, Gtk.PositionType.RIGHT, 1, 1)
        
        # Wind Direction entry
        wind_lbl2 = Gtk.Label("Wind Direction: ")
        wind_lbl2.set_alignment(0, 0.5)
        new_grid2.attach_next_to(wind_lbl2, wind_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.wind_com = Gtk.ComboBoxText()
        for i in ["None", "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]:
            self.wind_com.append_text(i)
        self.wind_com.set_active(0)
        new_grid2.attach_next_to(self.wind_com, wind_lbl2, Gtk.PositionType.RIGHT, 2, 1)
        
        # Humidity entry
        humi_lbl = Gtk.Label("Humidity %: ")
        humi_lbl.set_alignment(0, 0.5)
        new_grid3.add(humi_lbl)
        humi_adj = Gtk.Adjustment(lower = 0, upper = 100, step_increment = 1)
        self.humi_sbtn = Gtk.SpinButton(digits = 2, adjustment = humi_adj)
        self.humi_sbtn.set_numeric(False)
        self.humi_sbtn.set_value(0)
        new_grid3.attach_next_to(self.humi_sbtn, humi_lbl, Gtk.PositionType.RIGHT, 2, 1)
        
        # Air Pressure entry
        airp_lbl = Gtk.Label("Air Pressure: ")
        airp_lbl.set_alignment(0, 0.5)
        new_grid3.attach_next_to(airp_lbl, humi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        airp_adj = Gtk.Adjustment(lower = 0, upper = 2000, step_increment = 1)
        self.airp_sbtn = Gtk.SpinButton(digits = 2, adjustment = airp_adj)
        self.airp_sbtn.set_numeric(False)
        self.airp_sbtn.set_value(0)
        new_grid3.attach_next_to(self.airp_sbtn, airp_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.airp_unit = Gtk.ComboBoxText()
        for i in ["hPa", "mbar"]:
            self.airp_unit.append_text(i)
        self.airp_unit.set_active(unit)
        new_grid3.attach_next_to(self.airp_unit, self.airp_sbtn, Gtk.PositionType.RIGHT, 1, 1)
        
        # Air Pressure Change entry
        airp_lbl2 = Gtk.Label("Air Pressure Change: ")
        airp_lbl2.set_alignment(0, 0.5)
        new_grid3.attach_next_to(airp_lbl2, airp_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.airp_com = Gtk.ComboBoxText()
        for i in ["Steady", "Rising", "Falling"]:
            self.airp_com.append_text(i)
        self.airp_com.set_active(0)
        new_grid3.attach_next_to(self.airp_com, airp_lbl2, Gtk.PositionType.RIGHT, 2, 1)
        
        # Cloud Cover entry
        clou_lbl = Gtk.Label("Cloud Cover: ")
        clou_lbl.set_alignment(0, 0.5)
        new_grid3.attach_next_to(clou_lbl, airp_lbl2, Gtk.PositionType.BOTTOM, 1, 1)
        self.clou_com = Gtk.ComboBoxText()
        for i in ["Sunny", "Mostly Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy"]:
            self.clou_com.append_text(i)
        self.clou_com.set_active(0)
        new_grid3.attach_next_to(self.clou_com, clou_lbl, Gtk.PositionType.RIGHT, 2, 1)
        
        # Cloud Type entry
        clou_lbl2 = Gtk.Label("Cloud Type: ")
        clou_lbl2.set_alignment(0, 0.5)
        new_grid3.attach_next_to(clou_lbl2, clou_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.clou_com2 = Gtk.ComboBoxText()
        for i in ["None", "Unknown", "Cirrus", "Cirrocumulus", "Cirrostratus", "Cumulonimbus", "Altocumulus", "Altostratus",
                  "Stratus", "Cumulus", "Stratocumulus"]:
            self.clou_com2.append_text(i)
        self.clou_com2.set_active(0)
        new_grid3.attach_next_to(self.clou_com2, clou_lbl2, Gtk.PositionType.RIGHT, 2, 1)
        
        # Visibility entry
        visi_lbl = Gtk.Label("Visibility: ")
        visi_lbl.set_alignment(0, 0.5)
        new_grid3.attach_next_to(visi_lbl, clou_lbl2, Gtk.PositionType.BOTTOM, 1, 1)
        visi_adj = Gtk.Adjustment(lower = 0, upper = 1000, step_increment = 1)
        self.visi_sbtn = Gtk.SpinButton(digits = 2, adjustment = visi_adj)
        self.visi_sbtn.set_numeric(False)
        self.visi_sbtn.set_value(0)
        new_grid3.attach_next_to(self.visi_sbtn, visi_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.visi_unit = Gtk.ComboBoxText()
        for i in ["km", "mi"]:
            self.visi_unit.append_text(i)
        self.visi_unit.set_active(unit)
        new_grid3.attach_next_to(self.visi_unit, self.visi_sbtn, Gtk.PositionType.RIGHT, 1, 1)
        
        # Notes entry
        note_lbl = Gtk.Label("Notes: ")
        note_lbl.set_alignment(0, 0.5)
        new_grid3.attach_next_to(note_lbl, visi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.note_ent = Gtk.Entry()
        new_grid3.attach_next_to(self.note_ent, note_lbl, Gtk.PositionType.RIGHT, 2, 1)
        
        # Add the notebook.
        self.get_content_area().add(notebook)
        
        # Add the tabs to the notebook.
        notebook.append_page(new_grid1, new_grid1_lbl)
        notebook.append_page(new_grid2, new_grid2_lbl)
        notebook.append_page(new_grid3, new_grid3_lbl)
        
        # Pre-fill from given values, if there are any.
        if len(prefill_data) > 0:
            self.temp_sbtn.set_value(prefill_data[0])
            self.wind_sbtn.set_value(prefill_data[1])
            self.wind_com.set_active(["None", "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"].index(prefill_data[2]))
            self.humi_sbtn.set_value(prefill_data[3])
            self.airp_sbtn.set_value(prefill_data[4])
            self.airp_com.set_active(["Steady", "Rising", "Falling"].index(prefill_data[5]))
            station = False
        
        # Pre-fill the fields, if the user wants that.
        elif prefill and user_location and len(user_location) == 5:
            station = self.prefill(user_location, units, profile)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
        
        # Show the dialog saying data has been prefilled.
        if show_prefill_dlg and prefill and user_location and len(user_location) == 5 and station:
            
            # Show the dialog.
            show_alert_dialog(self, "Add New - %s" % profile, "Temperature, wind, humidity, and air pressure have been pre-filled using data from Yahoo! Weather.\n\nLocation is set to %s, at %s." % (user_location, station))
    
    
    def prefill(self, user_location, units, profile):
        """Pre-fill the fields."""
        
        # Get the data.
        data = pywapi.get_weather_from_yahoo(user_location, units = ("metric" if units["prec"] == "cm" else "imperial"))
        
        # If there was an error, tell the user and cancel the action.
        if "error" in data:
            show_error_dialog(self, "Add New - %s" % profile, "There was an error getting the data from Yahoo! Weather.\n\nDebug: %s" % data["error"])
            return False
        
        # Set the temperature field.
        self.temp_sbtn.set_value(float(data["condition"]["temp"]))
        
        # Set the wind fields.
        try:
            self.wind_com.set_active(["None", "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"].index(utility_functions.degree_to_direction(float(data["wind"]["direction"]))))
        except:
            self.wind_com.set_active(0)
        try:
            self.wind_sbtn.set_value(float(data["wind"]["speed"]))
        except:
            self.wind_sbtn.set_value(0.0)
        
        # Set the humidity field.
        self.humi_sbtn.set_value(float(data["atmosphere"]["humidity"]))
        
        # Set the air pressure fields.
        self.airp_sbtn.set_value(float(data["atmosphere"]["pressure"]))
        if units["airp"] == "mbar":
            new_pressure = float(data["atmosphere"]["pressure"]) * 33.86389
            self.airp_sbtn.set_value(new_pressure)
        self.airp_com.set_active(int(data["atmosphere"]["rising"]))
        
        # Return the location.
        return "%s, %s" % (data["location"]["city"], data["location"]["country"])
