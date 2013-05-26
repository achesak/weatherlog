# -*- coding: utf-8 -*-


# This file defines any dialogs used, other than the main one.


# Import GTK for the dialogs.
from gi.repository import Gtk


class AddNewDialog(Gtk.Dialog):
    """Shows the "Add New" dialog."""
    def __init__(self, parent):
        """Create the dialog."""
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Add New", parent, Gtk.DialogFlags.MODAL)
        
        # Add the buttons.
        self.add_button("OK", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        
        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        new_box.add(new_grid)
        
        # Create the Date label and entry. Replace with a proper datepicker later?
        date_lbl = Gtk.Label("Date: ")
        date_lbl.set_alignment(0, 0.5)
        new_grid.add(date_lbl)
        self.date_ent = Gtk.Entry()
        new_grid.attach_next_to(self.date_ent, date_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Temperature label and entry.
        temp_lbl = Gtk.Label("Temperature (°C): ")
        temp_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(temp_lbl, date_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.temp_ent = Gtk.Entry()
        new_grid.attach_next_to(self.temp_ent, temp_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Precipitation label, entry, and combobox.
        prec_lbl = Gtk.Label("Precipitation (cm): ")
        prec_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(prec_lbl, temp_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.prec_ent = Gtk.Entry()
        new_grid.attach_next_to(self.prec_ent, prec_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.prec_com = Gtk.ComboBoxText()
        for i in ["Rain", "Snow", "Hail", "Sleet"]:
            self.prec_com.append_text(i)
        new_grid.attach_next_to(self.prec_com, self.prec_ent, Gtk.PositionType.RIGHT, 1, 1)
        # Create the Wind label, entry, and combobox.
        wind_lbl = Gtk.Label("Wind (kph): ")
        wind_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(wind_lbl, prec_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.wind_ent = Gtk.Entry()
        new_grid.attach_next_to(self.wind_ent, wind_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.wind_com = Gtk.ComboBoxText()
        for i in ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]:
            self.wind_com.append_text(i)
        new_grid.attach_next_to(self.wind_com, self.wind_ent, Gtk.PositionType.RIGHT, 1, 1)
        # Create the Humidity label and entry.
        humi_lbl = Gtk.Label("Humidity (%): ")
        humi_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(humi_lbl, wind_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.humi_ent = Gtk.Entry()
        new_grid.attach_next_to(self.humi_ent, humi_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Air Pressure label and entry.
        airp_lbl = Gtk.Label("Air Pressure (mbar): ")
        airp_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(airp_lbl, humi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.airp_ent = Gtk.Entry()
        new_grid.attach_next_to(self.airp_ent, airp_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Cloud Cover label and combobox.
        clou_lbl = Gtk.Label("Cloud Cover: ")
        clou_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(clou_lbl, airp_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.clou_com = Gtk.ComboBoxText()
        for i in ["Sunny", "Mostly Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy"]:
            self.clou_com.append_text(i)
        new_grid.attach_next_to(self.clou_com, clou_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Notes label and entry.
        note_lbl = Gtk.Label("Notes: ")
        note_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(note_lbl, clou_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.note_ent = Gtk.Entry()
        new_grid.attach_next_to(self.note_ent, note_lbl, Gtk.PositionType.RIGHT, 2, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()


class InfoDialog(Gtk.Dialog):
    """Shows the "Info" dialog."""
    def __init__(self, parent):
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