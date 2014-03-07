# -*- coding: utf-8 -*-


# This file defines the Info for Selected Dates dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class InfoSelectedDialog(Gtk.Dialog):
    """Shows the info for selected dates dialog."""
    def __init__(self, parent, info, profile, dates):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "%s Info for Selected Dates - %s" % (info, profile), parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        # Don't allow the user to resize the window.
        #self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        info_box = self.get_content_area()
        info_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        info_box.add(info_grid)
        
        # Create the label.
        info_lbl = Gtk.Label("Select the dates:")
        info_lbl.set_alignment(0, 0.5)
        info_grid.add(info_lbl)
        
        # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str)
        # Add the dates.
        for i in dates:
            self.liststore.append(i)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        
        # Create the Date column.
        date_text = Gtk.CellRendererText()
        self.date_col = Gtk.TreeViewColumn("Date", date_text, text = 0)
        self.treeview.append_column(self.date_col)
        
        # Allow for multiple items to be selected.
        self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        
        # Create the ScrolledWindow for displaying the list with a scrollbar.
        scrolled_win = Gtk.ScrolledWindow()
        
        # The container should scroll vertically and horizontally.
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        
        # Display the TreeView.
        scrolled_win.add(self.treeview)
        info_grid.attach_next_to(scrolled_win, info_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Show the dialog.
        self.show_all()
