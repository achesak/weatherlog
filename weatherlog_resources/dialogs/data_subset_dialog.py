# -*- coding: utf-8 -*-


# This file defines the data subset dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class DataSubsetDialog(Gtk.Dialog):
    """Shows the data subset dialog."""
    def __init__(self, parent, title, data, show_units, units):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(800, 300)
        
        # Add the buttons.
        self.add_button("Export", 9)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the ListStore for storing the data. ListStore has 8 columns, all strings.
        self.liststore = Gtk.ListStore(str, str, str, str, str, str, str, str)
        
        # Add the data.
        for i in data:
            self.liststore.append(i)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        
        # Create the Date column.
        date_text = Gtk.CellRendererText()
        self.date_col = Gtk.TreeViewColumn("Date", date_text, text = 0)
        self.treeview.append_column(self.date_col)
        
        # Create the Temperature column.
        temp_text = Gtk.CellRendererText()
        self.temp_col = Gtk.TreeViewColumn("Temperature (%s)" % units["temp"], temp_text, text = 1)
        self.treeview.append_column(self.temp_col)
        
        # Create the Precipation column.
        prec_text = Gtk.CellRendererText()
        self.prec_col = Gtk.TreeViewColumn("Precipitation (%s)" % units["prec"], prec_text, text = 2)
        self.treeview.append_column(self.prec_col)
        
        # Create the Wind column.
        wind_text = Gtk.CellRendererText()
        self.wind_col = Gtk.TreeViewColumn("Wind (%s)" % units["wind"], wind_text, text = 3)
        self.treeview.append_column(self.wind_col)
        
        # Create the Humidity column.
        humi_text = Gtk.CellRendererText()
        self.humi_col = Gtk.TreeViewColumn("Humidity (%)", humi_text, text = 4)
        self.treeview.append_column(self.humi_col)
        
        # Create the Air Pressure column.
        airp_text = Gtk.CellRendererText()
        self.airp_col = Gtk.TreeViewColumn("Air Pressure (%s)" % units["airp"], airp_text, text = 5)
        self.treeview.append_column(self.airp_col)
        
        # Create the Cloud Cover column.
        clou_text = Gtk.CellRendererText()
        self.clou_col = Gtk.TreeViewColumn("Cloud Cover", clou_text, text = 6)
        self.treeview.append_column(self.clou_col)
        
        # Create the Notes column.
        note_text = Gtk.CellRendererText()
        self.note_col = Gtk.TreeViewColumn("Notes", note_text, text = 7)
        self.treeview.append_column(self.note_col)
        
        # Create the ScrolledWindow for displaying the list with a scrollbar.
        scrolled_win = Gtk.ScrolledWindow()
        
        # The container should scroll both horizontally and vertically.
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        
        # Display the TreeView.
        scrolled_win.add(self.treeview)
        self.get_content_area().add(scrolled_win)
        
        # Change the titles, if the user doesn't want units to be displayed.
        if not show_units:
            self.temp_col.set_title("Temperature")
            self.prec_col.set_title("Precipitation")
            self.wind_col.set_title("Wind")
            self.humi_col.set_title("Humidity")
            self.airp_col.set_title("Air Pressure")
        
        # Show the dialog. There's no need to get the response.
        self.show_all()
