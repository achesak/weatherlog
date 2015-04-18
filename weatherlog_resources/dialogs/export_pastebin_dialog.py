# -*- coding: utf-8 -*-


# This file defines the dialog for exporting to Pastebin.


# Import GTK for the dialog.
from gi.repository import Gtk


class ExportPastebinDialog(Gtk.Dialog):
    """Shows the "Export to Pastebin" dialog."""
    def __init__(self, parent, title):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        nam_box = self.get_content_area()
        nam_grid = Gtk.Grid()
        nam_box.add(nam_grid)
        
        # Create the labels and entries.
        nam_lbl = Gtk.Label("Paste name: ")
        nam_lbl.set_alignment(0, 0.5)
        nam_grid.add(nam_lbl)
        self.nam_ent = Gtk.Entry()
        nam_grid.attach_next_to(self.nam_ent, nam_lbl, Gtk.PositionType.RIGHT, 1, 1)
        for_lbl = Gtk.Label("Format: ")
        for_lbl.set_alignment(0, 0.5)
        nam_grid.attach_next_to(for_lbl, nam_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.for_com = Gtk.ComboBoxText()
        for i in ["JSON", "HTML", "CSV"]:
            self.for_com.append_text(i)
        self.for_com.set_active(0)
        nam_grid.attach_next_to(self.for_com, for_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
