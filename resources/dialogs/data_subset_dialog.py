# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/data_subset_dialog.py
# This dialog displays data subsets.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk

# Import copy for deep copying lsits.
import copy

# Import application modules.
from resources.constants import *


class DataSubsetDialog(Gtk.Dialog):
    """Shows the data subset dialog."""

    def __init__(self, parent, title, subtitle, data, units, config):
        """Create the dialog."""

        Gtk.Dialog.__init__(self, title, parent, use_header_bar=True)
        self.set_default_size(1200, 500)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Export", DialogResponse.EXPORT)

        # Create the header bar.
        header = self.get_header_bar()
        header.set_title(title)
        header.set_subtitle(subtitle)

        # Create the data columns.
        self.liststore = Gtk.ListStore(str, str, str, str, str, str, str, str, str, str)
        self.treeview = Gtk.TreeView(model=self.liststore)
        date_text = Gtk.CellRendererText()
        self.date_col = Gtk.TreeViewColumn("Date", date_text, text=0)
        self.treeview.append_column(self.date_col)
        temp_text = Gtk.CellRendererText()
        self.temp_col = Gtk.TreeViewColumn("Temperature (%s)" % units["temp"], temp_text, text=1)
        self.treeview.append_column(self.temp_col)
        chil_text = Gtk.CellRendererText()
        self.chil_col = Gtk.TreeViewColumn("Wind Chill (%s)" % units["temp"], chil_text, text=2)
        self.treeview.append_column(self.chil_col)
        prec_text = Gtk.CellRendererText()
        self.prec_col = Gtk.TreeViewColumn("Precipitation (%s)" % units["prec"], prec_text, text=3)
        self.treeview.append_column(self.prec_col)
        wind_text = Gtk.CellRendererText()
        self.wind_col = Gtk.TreeViewColumn("Wind (%s)" % units["wind"], wind_text, text=4)
        self.treeview.append_column(self.wind_col)
        humi_text = Gtk.CellRendererText()
        self.humi_col = Gtk.TreeViewColumn("Humidity (%)", humi_text, text=5)
        self.treeview.append_column(self.humi_col)
        airp_text = Gtk.CellRendererText()
        self.airp_col = Gtk.TreeViewColumn("Air Pressure (%s)" % units["airp"], airp_text, text=6)
        self.treeview.append_column(self.airp_col)
        visi_text = Gtk.CellRendererText()
        self.visi_col = Gtk.TreeViewColumn("Visibility (%s)" % units["visi"], visi_text, text=7)
        self.treeview.append_column(self.visi_col)
        clou_text = Gtk.CellRendererText()
        self.clou_col = Gtk.TreeViewColumn("Cloud Cover", clou_text, text=8)
        self.treeview.append_column(self.clou_col)
        note_text = Gtk.CellRendererText()
        self.note_col = Gtk.TreeViewColumn("Notes", note_text, text=9)
        self.treeview.append_column(self.note_col)

        # Display the UI.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        scrolled_win.add(self.treeview)
        self.get_content_area().add(scrolled_win)

        # Change the titles, if the user doesn't want units to be displayed.
        if not config["show_units"]:
            self.temp_col.set_title("Temperature")
            self.prec_col.set_title("Precipitation")
            self.wind_col.set_title("Wind")
            self.humi_col.set_title("Humidity")
            self.airp_col.set_title("Air Pressure")

        # Add the data. Truncate the note fields before the data is added to the interface.
        new_data = copy.deepcopy(data)
        if config["truncate_notes"]:
            for row in new_data:
                note = row[9]
                newline_split = False
                if "\n" in note:
                    note = note.splitlines()[0]
                    newline_split = True
                if len(note) > 46:
                    note = note[0:40] + " [...]"
                elif newline_split:
                    note += " [...]"
                row[9] = note

        self.liststore.clear()
        for i in new_data:
            self.liststore.append(i)

        # Show the dialog.
        self.show_all()
