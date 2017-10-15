# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/options_dialog.py
# This dialog shows and alters the application configuration.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk, Gdk

# Import application modules.
import resources.convert as convert
from resources.constants import *


class OptionsDialog(Gtk.Dialog):
    """Shows the "Options" dialog."""
    
    def __init__(self, parent, config):
        """Create the dialog."""
        
        Gtk.Dialog.__init__(self, "Preferences", parent, Gtk.DialogFlags.MODAL, use_header_bar=True)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Save", Gtk.ResponseType.OK)
        self.add_button("Reset", DialogResponse.RESET)

        # Create the header bar.
        header = self.get_header_bar()
        header.set_title("Preferences")
        
        # Create the tab notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        
        # Create the General tab.
        gen_grid = Gtk.Grid()
        gen_grid.set_hexpand(True)
        gen_grid.set_vexpand(True)
        gen_grid.set_column_spacing(10)
        gen_grid.set_row_spacing(5)
        gen_grid.set_border_width(10)
        gen_grid_lbl = Gtk.Label("General")

        # Create the units combobox.
        unit_lbl = Gtk.Label("Units: ")
        unit_lbl.set_tooltip_text("Measurement units used for display and conversion.")
        unit_lbl.set_alignment(0, 0.5)
        gen_grid.add(unit_lbl)
        self.unit_com = Gtk.ComboBoxText()
        self.unit_com.set_hexpand(True)
        for i in ["Metric", "Imperial"]:
            self.unit_com.append_text(i)
        self.unit_com.set_active(["Metric", "Imperial"].index(config["units"].title()))
        gen_grid.attach_next_to(self.unit_com, unit_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the weather header label.
        gen_weather_lbl = Gtk.Label()
        gen_weather_lbl.set_markup("<b>Weather</b>")
        gen_weather_lbl.set_alignment(0, 0.5)
        gen_weather_lbl.set_margin_top(10)
        gen_grid.attach_next_to(gen_weather_lbl, unit_lbl, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the pre-fill data checkbox.
        self.pre_chk = Gtk.CheckButton("Automatically fill data")
        self.pre_chk.set_tooltip_text("Automatically fill in fields when adding new data.\n\n" +
                                      "Note that this requires the location to be set as well.")
        self.pre_chk.set_active(config["pre-fill"])
        self.pre_chk.set_margin_left(20)
        gen_grid.attach_next_to(self.pre_chk, gen_weather_lbl, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the location type radiobuttons.
        self.use_city_rbtn = Gtk.RadioButton.new_with_label_from_widget(None, "Use city")
        self.use_zip_rbtn = Gtk.RadioButton.new_with_label_from_widget(self.use_city_rbtn, "Use zip code")
        if config["location_type"] == "city":
            self.use_city_rbtn.set_active(True)
        else:
            self.use_zip_rbtn.set_active(True)
        self.use_city_rbtn.set_margin_left(20)
        gen_grid.attach_next_to(self.use_city_rbtn, self.pre_chk, Gtk.PositionType.BOTTOM, 1, 1)
        gen_grid.attach_next_to(self.use_zip_rbtn, self.use_city_rbtn, Gtk.PositionType.RIGHT, 1, 1)

        # Create the zipcode entry.
        zip_lbl = Gtk.Label("Zip code: ")
        zip_lbl.set_tooltip_text("Zip code used for automatically filling in fields when adding new data.")
        zip_lbl.set_alignment(0, 0.5)
        zip_lbl.set_margin_left(20)
        gen_grid.attach_next_to(zip_lbl, self.use_city_rbtn, Gtk.PositionType.BOTTOM, 1, 1)
        self.zip_ent = Gtk.Entry()
        self.zip_ent.set_hexpand(True)
        self.zip_ent.set_max_length(5)
        self.zip_ent.connect("changed", lambda x: self.filter_numbers())
        self.zip_ent.set_text(config["zipcode"])
        gen_grid.attach_next_to(self.zip_ent, zip_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the city entry.
        cit_lbl = Gtk.Label("City: ")
        cit_lbl.set_tooltip_text("City used for automatically filling in fields when adding new data.")
        cit_lbl.set_alignment(0, 0.5)
        cit_lbl.set_margin_left(20)
        gen_grid.attach_next_to(cit_lbl, zip_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.cit_ent = Gtk.Entry()
        self.cit_ent.set_hexpand(True)
        self.cit_ent.set_text(config["city"])
        gen_grid.attach_next_to(self.cit_ent, cit_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the country code entry.
        cnt_lbl = Gtk.Label("Country: ")
        cnt_lbl.set_tooltip_text("Country code used for automatically filling in fields when adding new data.")
        cnt_lbl.set_alignment(0, 0.5)
        cnt_lbl.set_margin_left(20)
        gen_grid.attach_next_to(cnt_lbl, cit_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.cnt_ent = Gtk.Entry()
        self.cnt_ent.set_hexpand(True)
        self.cnt_ent.set_max_length(2)
        self.cnt_ent.set_text(config["country"])
        gen_grid.attach_next_to(self.cnt_ent, cnt_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the forecast period spinbutton.
        fcast_lbl = Gtk.Label("Forecast period: ")
        fcast_lbl.set_tooltip_text("Number of days for which to display a forecast.")
        fcast_lbl.set_alignment(0, 0.5)
        fcast_lbl.set_margin_left(20)
        gen_grid.attach_next_to(fcast_lbl, cnt_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        fcast_adj = Gtk.Adjustment(lower=1, upper=16, step_increment=1)
        self.fcast_sbtn = Gtk.SpinButton(digits=0, adjustment=fcast_adj)
        self.fcast_sbtn.set_numeric(False)
        self.fcast_sbtn.set_value(config["forecast_period"])
        self.fcast_sbtn.set_hexpand(True)
        gen_grid.attach_next_to(self.fcast_sbtn, fcast_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the search header label.
        gen_search_lbl = Gtk.Label()
        gen_search_lbl.set_markup("<b>Search</b>")
        gen_search_lbl.set_alignment(0, 0.5)
        gen_search_lbl.set_margin_top(10)
        gen_grid.attach_next_to(gen_search_lbl, fcast_lbl, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the default case insensitive checkbox.
        self.case_chk = Gtk.CheckButton("Case insensitive")
        self.case_chk.set_tooltip_text("Default to case insensitive when searching.")
        self.case_chk.set_active(config["default_case_insensitive"])
        self.case_chk.set_margin_left(20)
        gen_grid.attach_next_to(self.case_chk, gen_search_lbl, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the reset search checkbox.
        self.rsearch_chk = Gtk.CheckButton("Reset conditions after subset search")
        self.rsearch_chk.set_tooltip_text("Reset the conditions after subset search completion")
        self.rsearch_chk.set_active(config["reset_search"])
        self.rsearch_chk.set_margin_left(20)
        gen_grid.attach_next_to(self.rsearch_chk, self.case_chk, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the default selection mode combobox.
        smode_lbl = Gtk.Label("Selection mode: ")
        smode_lbl.set_tooltip_text("Default selection mode used with data subsets.")
        smode_lbl.set_alignment(0, 0.5)
        smode_lbl.set_margin_left(20)
        gen_grid.attach_next_to(smode_lbl, self.rsearch_chk, Gtk.PositionType.BOTTOM, 1, 1)
        self.smode_com = Gtk.ComboBoxText()
        self.smode_com.set_hexpand(True)
        for i in ["Match all", "Match at least one", "Match none"]:
            self.smode_com.append_text(i)
        self.smode_com.set_active(["Match all", "Match at least one", "Match none"]
                                  .index(config["default_selection_mode"]))
        gen_grid.attach_next_to(self.smode_com, smode_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Interface tab.
        int_grid = Gtk.Grid()
        int_grid.set_hexpand(True)
        int_grid.set_vexpand(True)
        int_grid.set_column_spacing(10)
        int_grid.set_row_spacing(5)
        int_grid.set_border_width(5)
        int_grid_lbl = Gtk.Label("Interface")
        
        # Create the Restore window size checkbox.
        self.win_chk = Gtk.CheckButton("Restore window size")
        self.win_chk.set_tooltip_text("Automatically restore window size on application " +
                                      "start to the size when previously closed.")
        self.win_chk.set_active(config["restore"])
        int_grid.add(self.win_chk)
        
        # Create the Show units in list checkbox.
        self.unit_chk = Gtk.CheckButton("Show units in list")
        self.unit_chk.set_tooltip_text("Show measurement units in the data list column titles.")
        self.unit_chk.set_active(config["show_units"])
        int_grid.attach_next_to(self.unit_chk, self.win_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the truncate notes checkbox.
        self.trun_chk = Gtk.CheckButton("Truncate notes")
        self.trun_chk.set_tooltip_text("Display the Notes field in a truncated form for long entries.")
        self.trun_chk.set_active(config["truncate_notes"])
        int_grid.attach_next_to(self.trun_chk, self.unit_chk, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the confirm deletions checkbox.
        self.del_chk = Gtk.CheckButton("Confirm deletions")
        self.del_chk.set_tooltip_text("Confirm when deleting data or datasets.")
        self.del_chk.set_active(config["confirm_del"])
        int_grid.attach_next_to(self.del_chk, self.trun_chk, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the import all checkbox.
        self.imp_chk = Gtk.CheckButton("Import all")
        self.imp_chk.set_tooltip_text("Automatically import all data from the file that has been selected to import.")
        self.imp_chk.set_active(config["import_all"])
        int_grid.attach_next_to(self.imp_chk, self.del_chk, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the graphs header label.
        int_graph_lbl = Gtk.Label()
        int_graph_lbl.set_markup("<b>Graphs</b>")
        int_graph_lbl.set_alignment(0, 0.5)
        int_graph_lbl.set_margin_top(10)
        int_grid.attach_next_to(int_graph_lbl, self.imp_chk, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the graph color selector.
        graph_color_lbl = Gtk.Label("Graph color: ")
        graph_color_lbl.set_tooltip_text("Select the color used for the graphs.")
        graph_color_lbl.set_alignment(0, 0.5)
        graph_color_lbl.set_margin_left(20)
        int_grid.attach_next_to(graph_color_lbl, int_graph_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.graph_color_btn = Gtk.ColorButton()
        self.graph_color_btn.set_hexpand(True)
        color_rgba = convert.hex_to_rgba(config["graph_color"])
        default_color = Gdk.RGBA(red=color_rgba[0], green=color_rgba[1], blue=color_rgba[2])
        self.graph_color_btn.set_rgba(default_color)
        int_grid.attach_next_to(self.graph_color_btn, graph_color_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the line width selector.
        width_lbl = Gtk.Label("Line width: ")
        width_lbl.set_tooltip_text("Select the line width.")
        width_lbl.set_alignment(0, 0.5)
        width_lbl.set_margin_left(20)
        int_grid.attach_next_to(width_lbl, graph_color_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        width_adj = Gtk.Adjustment(lower=1, upper=10, step_increment=1)
        self.width_sbtn = Gtk.SpinButton(digits=0, adjustment=width_adj)
        self.width_sbtn.set_numeric(False)
        self.width_sbtn.set_value(config["line_width"])
        int_grid.attach_next_to(self.width_sbtn, width_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the line style selector.
        line_lbl = Gtk.Label("Line style: ")
        line_lbl.set_tooltip_text("Select the style used for graph lines.")
        line_lbl.set_alignment(0, 0.5)
        line_lbl.set_margin_left(20)
        int_grid.attach_next_to(line_lbl, width_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.line_com = Gtk.ComboBoxText()
        for i in ["Solid", "Dashes", "Dots", "Dashes and dots"]:
            self.line_com.append_text(i)
        self.line_com.set_active(["Solid", "Dashes", "Dots", "Dashes and dots"].index(config["line_style"]))
        int_grid.attach_next_to(self.line_com, line_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the bar chart style selector.
        hatch_styles = ["Solid", "Large upward stripes", "Small upward stripes", "Large downward stripes",
                        "Small downward stripes", "Horizontal stripes", "Crosshatch", "Diagonal crosshatch",
                        "Stars", "Dots", "Small circles", "Large circles"]
        hatch_lbl = Gtk.Label("Bar chart style: ")
        hatch_lbl.set_tooltip_text("Select the style used for bar charts.")
        hatch_lbl.set_alignment(0, 0.5)
        hatch_lbl.set_margin_left(20)
        int_grid.attach_next_to(hatch_lbl, line_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.hatch_com = Gtk.ComboBoxText()
        for i in hatch_styles:
            self.hatch_com.append_text(i)
        self.hatch_com.set_active(hatch_styles.index(config["hatch_style"]))
        int_grid.attach_next_to(self.hatch_com, hatch_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Other tab.
        other_grid = Gtk.Grid()
        other_grid.set_hexpand(True)
        other_grid.set_vexpand(True)
        other_grid.set_column_spacing(10)
        other_grid.set_row_spacing(5)
        other_grid.set_border_width(10)
        other_grid_lbl = Gtk.Label("Other")

        # Create the pastebin header label.
        other_pastebin_lbl = Gtk.Label()
        other_pastebin_lbl.set_markup("<b>Pastebin</b>")
        other_pastebin_lbl.set_alignment(0, 0.5)
        other_grid.attach(other_pastebin_lbl, 0, 0, 2, 1)
        
        # Create the pastebin default format combobox.
        pform_lbl = Gtk.Label("Default format: ")
        pform_lbl.set_tooltip_text("Default format")
        pform_lbl.set_alignment(0, 0.5)
        pform_lbl.set_margin_left(20)
        other_grid.attach_next_to(pform_lbl, other_pastebin_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.pform_com = Gtk.ComboBoxText()
        self.pform_com.set_hexpand(True)
        for i in ["JSON", "HTML", "CSV"]:
            self.pform_com.append_text(i)
        self.pform_com.set_active(["JSON", "HTML", "CSV"].index(config["pastebin_format"]))
        other_grid.attach_next_to(self.pform_com, pform_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the pastebin default expiration combobox.
        pexpi_lbl = Gtk.Label("Default expiration: ")
        pexpi_lbl.set_tooltip_text("Default expiration")
        pexpi_lbl.set_alignment(0, 0.5)
        pexpi_lbl.set_margin_left(20)
        other_grid.attach_next_to(pexpi_lbl, pform_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.pexpi_com = Gtk.ComboBoxText()
        self.pexpi_com.set_hexpand(True)
        for i in ["Never", "1 Hour", "1 Day", "1 Week", "2 Weeks", "1 Month"]:
            self.pexpi_com.append_text(i)
        self.pexpi_com.set_active(["N", "1H", "1D", "1W", "2W", "1M"].index(config["pastebin_expires"]))
        other_grid.attach_next_to(self.pexpi_com, pexpi_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the pastebin default exposure combobox.
        pexpo_lbl = Gtk.Label("Default exposure: ")
        pexpo_lbl.set_tooltip_text("Default exposure")
        pexpo_lbl.set_alignment(0, 0.5)
        pexpo_lbl.set_margin_left(20)
        other_grid.attach_next_to(pexpo_lbl, pexpi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.pexpo_com = Gtk.ComboBoxText()
        self.pexpo_com.set_hexpand(True)
        for i in ["Public", "Unlisted"]:
            self.pexpo_com.append_text(i)
        self.pexpo_com.set_active(config["pastebin_exposure"])
        other_grid.attach_next_to(self.pexpo_com, pexpo_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the technical header label.
        other_tech_lbl = Gtk.Label()
        other_tech_lbl.set_markup("<b>Technical</b>")
        other_tech_lbl.set_alignment(0, 0.5)
        other_tech_lbl.set_margin_top(10)
        other_grid.attach_next_to(other_tech_lbl, pexpo_lbl, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the pastebin devkey entry.
        pname_lbl = Gtk.Label("Pastebin key: ")
        pname_lbl.set_tooltip_text("API key used for uploading to Pastebin.com.\n\n" +
                                   "Please replace with your own if you use this feature frequently.")
        pname_lbl.set_alignment(0, 0.5)
        pname_lbl.set_margin_left(20)
        other_grid.attach_next_to(pname_lbl, other_tech_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.pname_ent = Gtk.Entry()
        self.pname_ent.set_hexpand(True)
        self.pname_ent.set_text(config["pastebin"])
        other_grid.attach_next_to(self.pname_ent, pname_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the openweathermap devkey entry.
        owm_lbl = Gtk.Label("OpenWeatherMap key: ")
        owm_lbl.set_tooltip_text("API key used for getting data from OpenWeatherMap.\n\n" +
                                 "Please replace with your own if you use this feature frequently.")
        owm_lbl.set_alignment(0, 0.5)
        owm_lbl.set_margin_left(20)
        other_grid.attach_next_to(owm_lbl, pname_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.owm_ent = Gtk.Entry()
        self.owm_ent.set_hexpand(True)
        self.owm_ent.set_text(config["openweathermap"])
        other_grid.attach_next_to(self.owm_ent, owm_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Display the interface.
        opt_box = self.get_content_area()
        opt_box.add(notebook)
        notebook.append_page(gen_grid, gen_grid_lbl)
        notebook.append_page(int_grid, int_grid_lbl)
        notebook.append_page(other_grid, other_grid_lbl)
        
        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()

    def filter_numbers(self):
        """Filters non-numbers out of the entry."""
        
        text = self.zip_ent.get_text()
        self.zip_ent.set_text("".join([i for i in text if i in "0123456789"]))
