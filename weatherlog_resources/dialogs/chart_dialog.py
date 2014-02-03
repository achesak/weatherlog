# -*- coding: utf-8 -*-


# This file defines the generic chart dialog.


# Import GTK for the dialog.
from gi.repository import Gtk
# Import the functions for various tasks.
from .. import utility_functions
# Import the functions for getting the data.
from .. import info_functions


class GenericChartDialog(Gtk.Dialog):
    """Shows the chart dialog."""
    def __init__(self, parent, title, data):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        
        # Add the buttons.
        self.add_button("Export", 9)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str, str)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        # Create the Day column.
        day_text = Gtk.CellRendererText()
        day_col = Gtk.TreeViewColumn("Day", day_text, text = 0)
        self.treeview.append_column(day_col)
        # Create the Value column.
        valu_text = Gtk.CellRendererText()
        valu_col = Gtk.TreeViewColumn("Value", valu_text, text = 1)
        self.treeview.append_column(valu_col)
        # Create the Average Diff. column.
        avg_text = Gtk.CellRendererText()
        avg_col = Gtk.TreeViewColumn("Average Diff.", valu_text, text = 2)
        self.treeview.append_column(avg_col)
        # Create the Low Diff. column.
        low_text = Gtk.CellRendererText()
        low_col = Gtk.TreeViewColumn("Low Diff.", low_text, text = 3)
        self.treeview.append_column(low_col)
        # Create the High Diff. column.
        high_text = Gtk.CellRendererText()
        high_col = Gtk.TreeViewColumn("High Diff.", high_text, text = 4)
        self.treeview.append_column(high_col)
        # Create the Median Diff. column.
        med_text = Gtk.CellRendererText()
        med_col = Gtk.TreeViewColumn("Median Diff.", med_text, text = 5)
        self.treeview.append_column(med_col)
        
        # Create the ScrolledWindow for displaying the list with a scrollbar.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        # Display the TreeView.
        scrolled_win.add(self.treeview)
        self.get_content_area().add(scrolled_win)
        
        # Add the data.
        for i in data:
            self.liststore.append(i)
        
        # Show the dialog. There's no need to get the response.
        self.show_all()

