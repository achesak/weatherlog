# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/edit_dialog.py
# This dialog edits an existing row of data.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk

# Import application modules.
import resources.datasets as datasets
from resources.constants import *


class EditDialog(Gtk.Dialog):
    """Shows the "Edit" dialog."""

    def __init__(self, parent, dataset, data, date, units):
        """Create the dialog."""

        # Determine the default units.
        unit = 0
        if units["wind"] == "mph":
            unit = 1

        Gtk.Dialog.__init__(self, "Edit %s" % date, parent, Gtk.DialogFlags.MODAL, use_header_bar=True)
        self.set_size_request(500, 600)
        self.add_button("Save Changes", Gtk.ResponseType.OK)
        self.add_button("Remove", DialogResponse.REMOVE)

        # Create the header bar.
        header = self.get_header_bar()
        header.set_title("Edit %s" % date)
        header.set_subtitle(dataset)
        header.set_show_close_button(True)

        # Create the grids.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
        new_grid.set_column_spacing(3)
        new_grid.set_row_spacing(3)
        new_box.add(new_grid)

        # Temperature entry
        temp_lbl = Gtk.Label("Temperature: ")
        temp_lbl.set_alignment(0, 0.5)
        new_grid.add(temp_lbl)
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

        # Set the values.
        self.temp_sbtn.set_value(float(data[1]))
        self.chil_sbtn.set_value(float(data[2]))
        if data[3] != "None":
            d2 = data[3].split(" ")
            prec_list = ["None", "Rain", "Snow", "Hail", "Sleet"]
            for i in range(0, len(prec_list)):
                if d2[1] == prec_list[i]:
                    self.prec_com.set_active(i)
                    break
            self.prec_sbtn.set_value(float(d2[0]))
        if data[4] != "None":
            d3 = data[4].split(" ")
            wind_list = ["None", "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW",
                         "NW", "NNW"]
            for i in range(0, len(wind_list)):
                if d3[1] == wind_list[i]:
                    self.wind_com.set_active(i)
                    break
            self.wind_sbtn.set_value(float(d3[0]))
        self.humi_sbtn.set_value(float(data[5]))
        d5 = data[6].split(" ")
        airp_list = ["Steady", "Rising", "Falling"]
        for i in range(0, len(airp_list)):
            if d5[1] == airp_list[i]:
                self.airp_com.set_active(i)
                break
        self.airp_sbtn.set_value(float(d5[0]))
        self.visi_sbtn.set_value(float(data[7]))
        clou_list1 = ["Sunny", "Mostly Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy"]
        clou_list2 = ["None", "Unknown", "Cirrus", "Cirrocumulus", "Cirrostratus", "Cumulonimbus", "Altocumulus",
                      "Altostratus",
                      "Stratus", "Cumulus", "Stratocumulus"]
        d81, d82 = datasets.split_list3([data[8]])
        d82 = datasets.strip_items(d82, ["(", ")"])
        for i in range(0, len(clou_list1)):
            if d81[0] == clou_list1[i]:
                self.clou_com.set_active(i)
                break
        for i in range(0, len(clou_list2)):
            if d82[0] == clou_list2[i]:
                self.clou_com2.set_active(i)
                break
        self.note_buffer.set_text(data[9])

        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()

        # Show the dialog.
        self.show_all()
