# -*- coding: utf-8 -*-


# This file defines the Add New dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class OptionsDialog(Gtk.Dialog):
    """Shows the "Options" dialog."""
    def __init__(self, parent, config):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Options", parent, Gtk.DialogFlags.MODAL)
        
        # Create the notebook.
        notebook = Gtk.Notebook()
        # Set tab position to top.
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        
        # Add the buttons.
        self.add_button("OK", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Reset", 3)
        
        # Create the first grid.
        opt_box = self.get_content_area()
        opt_grid1 = Gtk.Grid()
        opt_grid1_lbl = Gtk.Label("General")
        
        # Create the pre-fill data checkbox.
        self.pre_chk = Gtk.CheckButton("Pre-fill data")
        self.pre_chk.set_active(config["pre-fill"])
        opt_grid1.attach(self.pre_chk, 0, 0, 2, 1)
        
        # Create the save automatically checkbox.
        self.sav_chk = Gtk.CheckButton("Save automatically")
        self.sav_chk.set_active(config["auto_save"])
        opt_grid1.attach_next_to(self.sav_chk, self.pre_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the confirm deletions checkbox.
        self.del_chk = Gtk.CheckButton("Confirm deletions")
        self.del_chk.set_active(config["confirm_del"])
        opt_grid1.attach_next_to(self.del_chk, self.sav_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the Location label and entry.
        loc_lbl = Gtk.Label("Location: ")
        loc_lbl.set_alignment(0, 0.5)
        opt_grid1.attach_next_to(loc_lbl, self.del_chk, Gtk.PositionType.BOTTOM, 1, 1)
        self.loc_ent = Gtk.Entry()
        self.loc_ent.set_max_length(5)
        self.loc_ent.connect("changed", self.filter_numbers)
        self.loc_ent.set_text(config["location"])
        opt_grid1.attach_next_to(self.loc_ent, loc_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Units label and combobox.
        unit_lbl = Gtk.Label("Units: ")
        unit_lbl.set_alignment(0, 0.5)
        opt_grid1.attach_next_to(unit_lbl, loc_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.unit_com = Gtk.ComboBoxText()
        for i in ["Metric", "Imperial"]:
            self.unit_com.append_text(i)
        self.unit_com.set_active(["Metric", "Imperial"].index(config["units"].title()))
        opt_grid1.attach_next_to(self.unit_com, unit_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the second grid.
        opt_grid2 = Gtk.Grid()
        opt_grid2_lbl = Gtk.Label("Keys")
        
        # Create the Escape Windowed label and entry.
        escw_lbl = Gtk.Label("Escape windowed: ")
        escw_lbl.set_alignment(0, 0.5)
        opt_grid2.attach(escw_lbl, 0, 0, 1, 1)
        self.escw_com = Gtk.ComboBoxText()
        for i in ["Ignore", "Minimize", "Close"]:
            self.escw_com.append_text(i)
        self.escw_com.set_active(["Ignore", "Minimize", "Close"].index(config["escape_windowed"].title()))
        opt_grid2.attach_next_to(self.escw_com, escw_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Escape Fullscreen label and entry.
        escf_lbl = Gtk.Label("Escape fullscreen: ")
        escf_lbl.set_alignment(0, 0.5)
        opt_grid2.attach_next_to(escf_lbl, escw_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.escf_com = Gtk.ComboBoxText()
        for i in ["Ignore", "Exit Fullscreen", "Close"]:
            self.escf_com.append_text(i)
        self.escf_com.set_active(["Ignore", "Exit Fullscreen", "Close"].index(config["escape_fullscreen"].title()))
        opt_grid2.attach_next_to(self.escf_com, escf_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the third grid.
        opt_grid3 = Gtk.Grid()
        opt_grid3_lbl = Gtk.Label("Interface")
        
        # Create the Restore window size checkbox.
        self.win_chk = Gtk.CheckButton("Restore window size")
        self.win_chk.set_active(config["restore"])
        opt_grid3.attach(self.win_chk, 0, 0, 2, 1)
        
        # Create the Show dates in title checkbox.
        self.date_chk = Gtk.CheckButton("Show dates in title")
        self.date_chk.set_active(config["show_dates"])
        opt_grid3.attach(self.date_chk, 0, 1, 2, 1)
        
        # Create the Show units in list checkbox.
        self.unit_chk = Gtk.CheckButton("Show units in list")
        self.unit_chk.set_active(config["show_units"])
        opt_grid3.attach(self.unit_chk, 0, 2, 2, 1)
        
        # Add the notebook.
        opt_box.add(notebook)
        
        # Add the tabs to the notebook.
        notebook.append_page(opt_grid1, opt_grid1_lbl)
        notebook.append_page(opt_grid2, opt_grid2_lbl)
        notebook.append_page(opt_grid3, opt_grid3_lbl)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
    
    
    def filter_numbers(self, event):
        """Filters non-numbers out of the entry."""
        
        # Get the text.
        text = self.loc_ent.get_text()
        
        # Only allow numbers. Filter out any other characters.
        self.loc_ent.set_text("".join([i for i in text if i in "0123456789"]))
