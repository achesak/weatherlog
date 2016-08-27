# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/export_pastebin_dialog.py
# This dialog exports data to pastebin.com
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk


class ExportPastebinDialog(Gtk.Dialog):
    """Shows the "Export to Pastebin" dialog."""
    
    def __init__(self, parent, title, config):
        """Create the dialog."""
        
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_size_request(500, 0)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        nam_box = self.get_content_area()
        nam_grid = Gtk.Grid()
        nam_grid.set_column_spacing(3)
        nam_grid.set_row_spacing(3)
        nam_box.add(nam_grid)
        
        # Create the labels and entries.
        nam_lbl = Gtk.Label("Name: ")
        nam_lbl.set_alignment(0, 0.5)
        nam_grid.add(nam_lbl)
        self.nam_ent = Gtk.Entry()
        self.nam_ent.set_hexpand(True)
        nam_grid.attach_next_to(self.nam_ent, nam_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        for_lbl = Gtk.Label("Format: ")
        for_lbl.set_alignment(0, 0.5)
        nam_grid.attach_next_to(for_lbl, nam_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.for_com = Gtk.ComboBoxText()
        for i in ["JSON", "HTML", "CSV"]:
            self.for_com.append_text(i)
        self.for_com.set_active(["JSON", "HTML", "CSV"].index(config["pastebin_format"]))
        self.for_com.set_hexpand(True)
        nam_grid.attach_next_to(self.for_com, for_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        exi_lbl = Gtk.Label("Expiration: ")
        exi_lbl.set_alignment(0, 0.5)
        nam_grid.attach_next_to(exi_lbl, for_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.exi_com = Gtk.ComboBoxText()
        for i in ["Never", "1 Hour", "1 Day", "1 Week", "2 Weeks", "1 Month"]:
            self.exi_com.append_text(i)
        self.exi_com.set_active(["N", "1H", "1D", "1W", "2W", "1M"].index(config["pastebin_expires"]))
        self.exi_com.set_hexpand(True)
        nam_grid.attach_next_to(self.exi_com, exi_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        exo_lbl = Gtk.Label("Exposure: ")
        exo_lbl.set_alignment(0, 0.5)
        nam_grid.attach_next_to(exo_lbl, exi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.exo_com = Gtk.ComboBoxText()
        for i in ["Public", "Unlisted"]:
            self.exo_com.append_text(i)
        self.exo_com.set_active(config["pastebin_exposure"])
        self.exo_com.set_hexpand(True)
        nam_grid.attach_next_to(self.exo_com, exo_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id = Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
