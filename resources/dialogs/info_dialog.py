# -*- coding: utf-8 -*-


# This file defines the Info dialog.


# Import GTK for the dialog.
from gi.repository import Gtk
# Import the functions for various tasks.
from .. import utility_functions
# Import the functions for getting the data.
from .. import info_functions


class InfoDialog(Gtk.Dialog):
    """Shows the "Info" dialog."""
    def __init__(self, parent, data):
        """Create the dialog."""
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Info", parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        
        # Add the button.
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str, str)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        # Create the Category column.
        cate_text = Gtk.CellRendererText()
        cate_col = Gtk.TreeViewColumn("Category", cate_text, text = 0)
        self.treeview.append_column(cate_col)
        # Create the Value column.
        valu_text = Gtk.CellRendererText()
        valu_col = Gtk.TreeViewColumn("Value", valu_text, text = 1)
        self.treeview.append_column(valu_col)
        
        # Create the ScrolledWindow for displaying the list with a scrollbar.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        # Display the TreeView.
        scrolled_win.add(self.treeview)
        self.get_content_area().add(scrolled_win)
        
        # Add the data.
        ####### ADD THE STUFF TO CALCULATE THIS!
        self.liststore.append(["First day", "5/13/13"])
        self.liststore.append(["Last day", "5/14/13"])
        self.liststore.append(["Number of days", "1"])
        self.liststore.append(["Average temperature", "40 °C"])
        self.liststore.append(["Lowest temperature", "30 °C"])
        self.liststore.append(["Highest temperature", "50 °C"])
        self.liststore.append(["Average precipitation", "3.45 cm"])
        self.liststore.append(["Total precipitation", "56.42 cm"])
        self.liststore.append(["Average wind speed", "45 kph"])
        self.liststore.append(["Lowest wind speed", "0 kph"])
        self.liststore.append(["Highest wind speed", "99861 kph"])
        self.liststore.append(["Average humidity", "45%"])
        self.liststore.append(["Lowest humidity", "1%"])
        self.liststore.append(["Highest humidity", "99.8%"])
        self.liststore.append(["Average air pressure", "45 mbar"])
        self.liststore.append(["Lowest air pressure", "2 mbar"])
        self.liststore.append(["Highest air pressure", "100 mbar"])
        
        # Show the dialog. There's no need to get the response.
        self.show_all()