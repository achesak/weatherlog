# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/quick_search_dialog.py
# This dialog enters a new row of data.
#
################################################################################


# Import time for getting the current date.
import time
# Import GTK for the dialog.
from gi.repository import Gtk

# Import application modules.
from weatherlog_resources.dialogs.misc_dialogs import *
from weatherlog_resources.dialogs.calendar_dialog import CalendarDialog
import weatherlog_resources.get_weather as get_weather
import weatherlog_resources.degrees as degrees
import weatherlog_resources.clouds as clouds


class AddNewDialog(Gtk.Dialog):
    """Shows the "Add New" dialog."""

    def __init__(self, parent, dataset, user_location, user_zipcode, prefill, show_prefill_dlg, units, config,
                 prefill_data=()):
        """Create the dialog."""

        # Determine the default units.
        unit = 0
        if config["units"] == "imperial":
            unit = 1

        # Get the current date.
        date = time.strftime("%d/%m/%Y")

        Gtk.Dialog.__init__(self, "Add New Data - %s" % dataset, parent, Gtk.DialogFlags.MODAL)
        self.set_size_request(500, 600)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)

        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
        new_grid.set_column_spacing(3)
        new_grid.set_row_spacing(3)
        new_box.add(new_grid)

        # Date entry
        date_lbl = Gtk.Label("Date: ")
        date_lbl.set_alignment(0, 0.5)
        new_grid.add(date_lbl)
        self.date_ent = Gtk.Entry()
        self.date_ent.set_text(date)
        self.date_ent.set_editable(False)
        new_grid.attach_next_to(self.date_ent, date_lbl, Gtk.PositionType.RIGHT, 1, 1)
        date_btn = Gtk.Button("Select Date")
        date_btn.connect("clicked", lambda event: self.select_date())
        new_grid.attach_next_to(date_btn, self.date_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Temperature entry
        temp_lbl = Gtk.Label("Temperature: ")
        temp_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(temp_lbl, date_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        if units["temp"].encode("utf-8") == "°C":
            temp_adj = Gtk.Adjustment(lower=-100, upper=100, step_increment=1)
        else:
            temp_adj = Gtk.Adjustment(lower=-150, upper=150, step_increment=1)
        self.temp_sbtn = Gtk.SpinButton(digits=2, adjustment=temp_adj)
        self.temp_sbtn.set_numeric(False)
        self.temp_sbtn.set_value(0)
        new_grid.attach_next_to(self.temp_sbtn, temp_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.temp_unit = Gtk.ComboBoxText()
        for i in ["°C", "°F"]:
            self.temp_unit.append_text(i)
        self.temp_unit.set_active(unit)
        new_grid.attach_next_to(self.temp_unit, self.temp_sbtn, Gtk.PositionType.RIGHT, 1, 1)

        # Wind Chill entry
        chil_lbl = Gtk.Label("Wind Chill: ")
        chil_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(chil_lbl, temp_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        if units["temp"].encode("utf-8") == "°C":
            chil_adj = Gtk.Adjustment(lower=-100, upper=100, step_increment=1)
        else:
            chil_adj = Gtk.Adjustment(lower=-150, upper=150, step_increment=1)
        self.chil_sbtn = Gtk.SpinButton(digits=2, adjustment=chil_adj)
        self.chil_sbtn.set_numeric(False)
        self.chil_sbtn.set_value(0)
        new_grid.attach_next_to(self.chil_sbtn, chil_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.chil_unit = Gtk.ComboBoxText()
        for i in ["°C", "°F"]:
            self.chil_unit.append_text(i)
        self.chil_unit.set_active(unit)
        new_grid.attach_next_to(self.chil_unit, self.chil_sbtn, Gtk.PositionType.RIGHT, 1, 1)

        # Precipitation entry
        prec_lbl = Gtk.Label("Precipitation: ")
        prec_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(prec_lbl, chil_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        prec_adj = Gtk.Adjustment(lower=0, upper=100, step_increment=1)
        self.prec_sbtn = Gtk.SpinButton(digits=2, adjustment=prec_adj)
        self.prec_sbtn.set_numeric(False)
        self.prec_sbtn.set_value(0)
        new_grid.attach_next_to(self.prec_sbtn, prec_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.prec_unit = Gtk.ComboBoxText()
        for i in ["cm", "in"]:
            self.prec_unit.append_text(i)
        self.prec_unit.set_active(unit)
        new_grid.attach_next_to(self.prec_unit, self.prec_sbtn, Gtk.PositionType.RIGHT, 1, 1)

        # Precipitation Type entry
        prec_lbl2 = Gtk.Label("Precipitation Type: ")
        prec_lbl2.set_alignment(0, 0.5)
        new_grid.attach_next_to(prec_lbl2, prec_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.prec_com = Gtk.ComboBoxText()
        for i in ["None", "Rain", "Snow", "Hail", "Sleet"]:
            self.prec_com.append_text(i)
        self.prec_com.set_active(0)
        new_grid.attach_next_to(self.prec_com, prec_lbl2, Gtk.PositionType.RIGHT, 2, 1)

        # Wind Speed entry
        wind_lbl = Gtk.Label("Wind Speed: ")
        wind_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(wind_lbl, prec_lbl2, Gtk.PositionType.BOTTOM, 1, 1)
        wind_adj = Gtk.Adjustment(lower=0, upper=500, step_increment=1)
        self.wind_sbtn = Gtk.SpinButton(digits=2, adjustment=wind_adj)
        self.wind_sbtn.set_numeric(False)
        self.wind_sbtn.set_value(0)
        new_grid.attach_next_to(self.wind_sbtn, wind_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.wind_unit = Gtk.ComboBoxText()
        for i in ["kph", "mph"]:
            self.wind_unit.append_text(i)
        self.wind_unit.set_active(unit)
        new_grid.attach_next_to(self.wind_unit, self.wind_sbtn, Gtk.PositionType.RIGHT, 1, 1)

        # Wind Direction entry
        wind_lbl2 = Gtk.Label("Wind Direction: ")
        wind_lbl2.set_alignment(0, 0.5)
        new_grid.attach_next_to(wind_lbl2, wind_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.wind_com = Gtk.ComboBoxText()
        for i in ["None", "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW",
                  "NNW"]:
            self.wind_com.append_text(i)
        self.wind_com.set_active(0)
        new_grid.attach_next_to(self.wind_com, wind_lbl2, Gtk.PositionType.RIGHT, 2, 1)

        # Humidity entry
        humi_lbl = Gtk.Label("Humidity %: ")
        humi_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(humi_lbl, wind_lbl2, Gtk.PositionType.BOTTOM, 1, 1)
        humi_adj = Gtk.Adjustment(lower=0, upper=100, step_increment=1)
        self.humi_sbtn = Gtk.SpinButton(digits=2, adjustment=humi_adj)
        self.humi_sbtn.set_numeric(False)
        self.humi_sbtn.set_value(0)
        new_grid.attach_next_to(self.humi_sbtn, humi_lbl, Gtk.PositionType.RIGHT, 2, 1)

        # Air Pressure entry
        airp_lbl = Gtk.Label("Air Pressure: ")
        airp_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(airp_lbl, humi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        airp_adj = Gtk.Adjustment(lower=0, upper=2000, step_increment=1)
        self.airp_sbtn = Gtk.SpinButton(digits=2, adjustment=airp_adj)
        self.airp_sbtn.set_numeric(False)
        self.airp_sbtn.set_value(0)
        new_grid.attach_next_to(self.airp_sbtn, airp_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.airp_unit = Gtk.ComboBoxText()
        for i in ["hPa", "mbar"]:
            self.airp_unit.append_text(i)
        self.airp_unit.set_active(unit)
        new_grid.attach_next_to(self.airp_unit, self.airp_sbtn, Gtk.PositionType.RIGHT, 1, 1)

        # Air Pressure Change entry
        airp_lbl2 = Gtk.Label("Air Pressure Change: ")
        airp_lbl2.set_alignment(0, 0.5)
        new_grid.attach_next_to(airp_lbl2, airp_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.airp_com = Gtk.ComboBoxText()
        for i in ["Steady", "Rising", "Falling"]:
            self.airp_com.append_text(i)
        self.airp_com.set_active(0)
        new_grid.attach_next_to(self.airp_com, airp_lbl2, Gtk.PositionType.RIGHT, 2, 1)

        # Visibility entry
        visi_lbl = Gtk.Label("Visibility: ")
        visi_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(visi_lbl, airp_lbl2, Gtk.PositionType.BOTTOM, 1, 1)
        visi_adj = Gtk.Adjustment(lower=0, upper=1000, step_increment=1)
        self.visi_sbtn = Gtk.SpinButton(digits=2, adjustment=visi_adj)
        self.visi_sbtn.set_numeric(False)
        self.visi_sbtn.set_value(0)
        new_grid.attach_next_to(self.visi_sbtn, visi_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.visi_unit = Gtk.ComboBoxText()
        for i in ["km", "mi"]:
            self.visi_unit.append_text(i)
        self.visi_unit.set_active(unit)
        new_grid.attach_next_to(self.visi_unit, self.visi_sbtn, Gtk.PositionType.RIGHT, 1, 1)

        # Cloud Cover entry
        clou_lbl = Gtk.Label("Cloud Cover: ")
        clou_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(clou_lbl, visi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.clou_com = Gtk.ComboBoxText()
        for i in ["Sunny", "Mostly Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy"]:
            self.clou_com.append_text(i)
        self.clou_com.set_active(0)
        new_grid.attach_next_to(self.clou_com, clou_lbl, Gtk.PositionType.RIGHT, 2, 1)

        # Cloud Type entry
        clou_lbl2 = Gtk.Label("Cloud Type: ")
        clou_lbl2.set_alignment(0, 0.5)
        new_grid.attach_next_to(clou_lbl2, clou_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.clou_com2 = Gtk.ComboBoxText()
        for i in ["None", "Unknown", "Cirrus", "Cirrocumulus", "Cirrostratus", "Cumulonimbus", "Altocumulus",
                  "Altostratus",
                  "Stratus", "Cumulus", "Stratocumulus"]:
            self.clou_com2.append_text(i)
        self.clou_com2.set_active(0)
        new_grid.attach_next_to(self.clou_com2, clou_lbl2, Gtk.PositionType.RIGHT, 2, 1)

        # Notes entry
        note_lbl = Gtk.Label("Notes: ", valign=Gtk.Align.START)
        note_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(note_lbl, clou_lbl2, Gtk.PositionType.BOTTOM, 1, 1)
        self.note_view = Gtk.TextView()
        self.note_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.note_buffer = self.note_view.get_buffer()
        note_win = Gtk.ScrolledWindow()
        note_win.set_hexpand(True)
        note_win.set_vexpand(True)
        note_win.set_size_request(100, 100)
        note_win.add(self.note_view)
        new_grid.attach_next_to(note_win, note_lbl, Gtk.PositionType.RIGHT, 2, 1)

        # Pre-fill from given values, if there are any.
        station = False
        if len(prefill_data) > 0:
            self.temp_sbtn.set_value(prefill_data[0])
            self.chil_sbtn.set_value(prefill_data[1])
            self.wind_sbtn.set_value(prefill_data[2])
            self.wind_com.set_active(
                ["None", "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW",
                 "NNW"].index(prefill_data[3]))
            self.humi_sbtn.set_value(prefill_data[4])
            self.airp_sbtn.set_value(prefill_data[5])
            self.airp_com.set_active(prefill_data[6])

        # Pre-fill the fields, if the user wants that.
        elif prefill and (user_location or user_zipcode):
            station, data = get_weather.get_prefill_data(units, config)

            if not station:
                error_message = data if isinstance(data, str) else data["error"]
                show_error_dialog(self, "Add New Data - %s" % dataset, "Error:\n\n%s" % error_message)
            else:
                self.temp_sbtn.set_value(data["temp"])
                self.chil_sbtn.set_value(data["chil"])
                self.wind_sbtn.set_value(data["wind"])
                self.wind_com.set_active(
                    ["None", "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW",
                     "NW", "NNW"].index(degrees.degree_to_direction(data["wind_dir"])))
                self.humi_sbtn.set_value(data["humi"])
                self.airp_sbtn.set_value(data["airp"])
                self.clou_com.set_active(clouds.percent_to_term(data["clou"]))

        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()

        # Show the dialog.
        self.show_all()

        # Show the dialog saying data has been prefilled.
        if show_prefill_dlg and prefill and (user_location or user_zipcode) and station:
            show_alert_dialog(self, "Add New Data - %s" % dataset,
                              "Some fields have been automatically filled using data from OpenWeatherMap." +
                              "\n\nLocation is set to %s." % station)

    def select_date(self):
        """Shows the date selection dialog."""

        # Show the dialog and get the date.
        date_dlg = CalendarDialog(self, "Add New Data", "Select date: ")
        date_dlg.run()
        year, month, day = date_dlg.info_cal.get_date()

        year, month, day = str(year), str(month + 1), str(day)
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day
        date = "%s/%s/%s" % (day, month, year)
        date_dlg.close()

        # Insert the date.
        self.date_ent.set_text(date)
