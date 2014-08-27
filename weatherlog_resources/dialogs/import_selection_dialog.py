# -*- coding: utf-8 -*-


# This file defines the dialog for selecting which dates to import.


# Import GTK for the dialog.
from gi.repository import Gtk


class ImportSelectionDialog(Gtk.Dialog):
    """Shows the import selection dialog."""
    def __init__(self, parent, title, dates):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Import All", 20)
        self.add_button("Import", 21)
        
        # Create the grid.
        sel_box = self.get_content_area()
        sel_grid = Gtk.Grid()
        sel_box.add(sel_grid)
        
        # Create the label.
        sel_lbl = Gtk.Label("Choose dates to import:")
        sel_lbl.set_alignment(0, 0.5)
        sel_grid.add(sel_lbl)
        
        # Create the Profile column.
        self.liststore = Gtk.ListStore(str)
        self.treeview = Gtk.TreeView(model = self.liststore)
        self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        pro_text = Gtk.CellRendererText()
        self.pro_col = Gtk.TreeViewColumn("Dates", pro_text, text = 0)
        self.treeview.append_column(self.pro_col)
        
        # Display the UI.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        scrolled_win.add(self.treeview)
        sel_grid.attach_next_to(scrolled_win, sel_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Add the dates.
        for i in dates:
            self.liststore.append([i])
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
