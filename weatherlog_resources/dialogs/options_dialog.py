# -*- coding: utf-8 -*-


# This file defines the Add New dialog.


# Import GTK for the dialog.
from gi.repository import Gtk, Gdk
# Import convert for converting between color systems.
import weatherlog_resources.convert as convert


class OptionsDialog(Gtk.Dialog):
    """Shows the "Options" dialog."""
    
    def __init__(self, parent, config):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, "Options", parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        self.add_button("Reset", 3)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the tab notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        
        # Create the first grid.
        opt_box = self.get_content_area()
        opt_grid1 = Gtk.Grid()
        opt_grid1.set_column_spacing(10)
        opt_grid1.set_row_spacing(5)
        opt_grid1_lbl = Gtk.Label("General")
        
        # Create the pre-fill data checkbox.
        self.pre_chk = Gtk.CheckButton("Automatically fill data")
        self.pre_chk.set_tooltip_text("Automatically fill in fields when adding new data. Note that this requires the location to be set as well.")
        self.pre_chk.set_active(config["pre-fill"])
        opt_grid1.attach(self.pre_chk, 0, 0, 2, 1)
        
        # Create the confirm deletions checkbox.
        self.del_chk = Gtk.CheckButton("Confirm deletions")
        self.del_chk.set_tooltip_text("Confirm when deleting data or datasets.")
        self.del_chk.set_active(config["confirm_del"])
        opt_grid1.attach_next_to(self.del_chk, self.pre_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the import all checkbox.
        self.imp_chk = Gtk.CheckButton("Import all")
        self.imp_chk.set_tooltip_text("Automatically import all data from the file that has been selected to import.")
        self.imp_chk.set_active(config["import_all"])
        opt_grid1.attach_next_to(self.imp_chk, self.del_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the Location label and entry.
        loc_lbl = Gtk.Label("Location: ")
        loc_lbl.set_tooltip_text("Location used for automatically filling in fields when adding new data. Note that this must be a 5-digit US zip code.")
        loc_lbl.set_alignment(0, 0.5)
        opt_grid1.attach_next_to(loc_lbl, self.imp_chk, Gtk.PositionType.BOTTOM, 1, 1)
        self.loc_ent = Gtk.Entry()
        self.loc_ent.set_max_length(5)
        self.loc_ent.connect("changed", self.filter_numbers)
        self.loc_ent.set_text(config["location"])
        opt_grid1.attach_next_to(self.loc_ent, loc_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Units label and combobox.
        unit_lbl = Gtk.Label("Units: ")
        unit_lbl.set_tooltip_text("Measurement units used for display and conversion.")
        unit_lbl.set_alignment(0, 0.5)
        opt_grid1.attach_next_to(unit_lbl, loc_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.unit_com = Gtk.ComboBoxText()
        for i in ["Metric", "Imperial"]:
            self.unit_com.append_text(i)
        self.unit_com.set_active(["Metric", "Imperial"].index(config["units"].title()))
        opt_grid1.attach_next_to(self.unit_com, unit_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the third grid.
        opt_grid3 = Gtk.Grid()
        opt_grid3.set_column_spacing(10)
        opt_grid3.set_row_spacing(5)
        opt_grid3_lbl = Gtk.Label("Interface")
        
        # Create the Restore window size checkbox.
        self.win_chk = Gtk.CheckButton("Restore window size")
        self.win_chk.set_tooltip_text("Automatically restore window size on application start to the size when previously closed.")
        self.win_chk.set_active(config["restore"])
        opt_grid3.attach(self.win_chk, 0, 0, 2, 1)
        
        # Create the Show dates in title checkbox.
        self.date_chk = Gtk.CheckButton("Show dates in title")
        self.date_chk.set_tooltip_text("Show starting and ending dates of the dataset in the title bar.")
        self.date_chk.set_active(config["show_dates"])
        opt_grid3.attach(self.date_chk, 0, 1, 2, 1)
        
        # Create the Show units in list checkbox.
        self.unit_chk = Gtk.CheckButton("Show units in list")
        self.unit_chk.set_tooltip_text("Show measurement units in the data list headers.")
        self.unit_chk.set_active(config["show_units"])
        opt_grid3.attach(self.unit_chk, 0, 2, 2, 1)
        
        # Create the show pre-fill dialog checkbox.
        self.pdl_chk = Gtk.CheckButton("Show data filling window")
        self.pdl_chk.set_tooltip_text("Show a window when data fields have been automatically filled.")
        self.pdl_chk.set_active(config["show_pre-fill"])
        opt_grid3.attach(self.pdl_chk, 0, 3, 2, 1)
        
        # Create the confirm exit checkbox.
        self.cex_chk = Gtk.CheckButton("Confirm application close")
        self.cex_chk.set_tooltip_text("Show a confirmation window when closing the application.")
        self.cex_chk.set_active(config["confirm_exit"])
        opt_grid3.attach(self.cex_chk, 0, 4, 2, 1)
        
        # Create the graph color selector.
        graph_color_lbl = Gtk.Label("Graph color: ")
        graph_color_lbl.set_alignment(0, 0.5)
        graph_color_lbl.set_tooltip_text("Select the color used for the graphs.")
        opt_grid3.attach(graph_color_lbl, 0, 5, 1, 1)
        self.graph_color_btn = Gtk.ColorButton()
        color_rgba = convert.hex_to_rgba(config["graph_color"])
        default_color = Gdk.RGBA(red = color_rgba[0], green = color_rgba[1], blue = color_rgba[2])
        self.graph_color_btn.set_rgba(default_color)
        opt_grid3.attach(self.graph_color_btn, 1, 5, 1, 1) #112233
        
        # Add the notebook.
        opt_box.add(notebook)
        
        # Add the tabs to the notebook.
        notebook.append_page(opt_grid1, opt_grid1_lbl)
        notebook.append_page(opt_grid3, opt_grid3_lbl)
        
        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id = Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
    
    
    def filter_numbers(self, event):
        """Filters non-numbers out of the entry."""
        
        text = self.loc_ent.get_text()
        self.loc_ent.set_text("".join([i for i in text if i in "0123456789"]))
