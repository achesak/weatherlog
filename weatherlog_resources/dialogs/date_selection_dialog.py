# -*- coding: utf-8 -*-


# This file defines the generic dialog for selecting dates.


# Import GTK for the dialog.
from gi.repository import Gtk


class DateSelectionDialog(Gtk.Dialog):
    """Shows the date selection dialog."""
    def __init__(self, parent, title, dates, buttons = [["Cancel", Gtk.ResponseType.CANCEL], ["OK", Gtk.ResponseType.OK]]):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        
        # Add the buttons.
        for i in buttons:
            self.add_button(i[0], i[1])
        
        # Create the grid.
        info_box = self.get_content_area()
        info_grid = Gtk.Grid()
        info_box.add(info_grid)
        
        # Create the label.
        info_lbl = Gtk.Label("Select the dates:")
        info_lbl.set_alignment(0, 0.5)
        info_grid.add(info_lbl)
        
        # Create the Date column.
        self.liststore = Gtk.ListStore(str)
        self.treeview = Gtk.TreeView(model = self.liststore)
        self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        date_text = Gtk.CellRendererText()
        self.date_col = Gtk.TreeViewColumn("Date", date_text, text = 0)
        self.treeview.append_column(self.date_col)
        
        # Display the UI.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        scrolled_win.add(self.treeview)
        info_grid.attach_next_to(scrolled_win, info_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Add the dates.
        for i in dates:
            self.liststore.append(i)
        
        # Show the dialog.
        self.show_all()
