# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/info_dialog.py
# This dialog shows the dataset info.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk

# Import application modules.
from weatherlog_resources.constants import *


class InfoDialog(Gtk.Dialog):
    """Shows the info dialog."""

    def __init__(self, parent, title, data):
        """Create the dialog."""

        Gtk.Dialog.__init__(self, title, parent)
        self.set_default_size(1000, 400)
        self.add_button("Export", DialogResponse.EXPORT)
        self.add_button("Close", Gtk.ResponseType.CLOSE)

        # Create the tab notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        info_box = self.get_content_area()

        # Tab 1: General info.
        gen_box = Gtk.Box()
        gen_box_lbl = Gtk.Label("General")
        self.gen_list = Gtk.ListStore(str, str)
        self.gen_tree = Gtk.TreeView(model=self.gen_list)
        gen_cate_text = Gtk.CellRendererText()
        gen_cate_col = Gtk.TreeViewColumn("Field", gen_cate_text, text=0)
        gen_cate_col.set_min_width(400)
        self.gen_tree.append_column(gen_cate_col)
        gen_value_text = Gtk.CellRendererText()
        gen_value_col = Gtk.TreeViewColumn("Value", gen_value_text, text=1)
        self.gen_tree.append_column(gen_value_col)
        gen_box.pack_start(self.gen_tree, fill=True, expand=True, padding=0)
        gen_win = Gtk.ScrolledWindow()
        gen_win.set_hexpand(True)
        gen_win.set_vexpand(True)
        gen_win.add(gen_box)

        # Tab 2: Temperature info.
        temp_box = Gtk.Box()
        temp_box_lbl = Gtk.Label("Temperature")
        self.temp_list = Gtk.ListStore(str, str)
        self.temp_tree = Gtk.TreeView(model=self.temp_list)
        temp_cate_text = Gtk.CellRendererText()
        temp_cate_col = Gtk.TreeViewColumn("Field", temp_cate_text, text=0)
        self.temp_tree.append_column(temp_cate_col)
        temp_value_text = Gtk.CellRendererText()
        temp_value_col = Gtk.TreeViewColumn("Value", temp_value_text, text=1)
        self.temp_tree.append_column(temp_value_col)
        temp_box.pack_start(self.temp_tree, fill=True, expand=True, padding=0)
        temp_win = Gtk.ScrolledWindow()
        temp_win.set_hexpand(True)
        temp_win.set_vexpand(True)
        temp_win.add(temp_box)

        # Tab 3: Wind Chill info.
        chil_box = Gtk.Box()
        chil_box_lbl = Gtk.Label("Wind Chill")
        self.chil_list = Gtk.ListStore(str, str)
        self.chil_tree = Gtk.TreeView(model=self.chil_list)
        chil_cate_text = Gtk.CellRendererText()
        chil_cate_col = Gtk.TreeViewColumn("Field", chil_cate_text, text=0)
        self.chil_tree.append_column(chil_cate_col)
        chil_value_text = Gtk.CellRendererText()
        chil_value_col = Gtk.TreeViewColumn("Value", chil_value_text, text=1)
        self.chil_tree.append_column(chil_value_col)
        chil_box.pack_start(self.chil_tree, fill=True, expand=True, padding=0)
        chil_win = Gtk.ScrolledWindow()
        chil_win.set_hexpand(True)
        chil_win.set_vexpand(True)
        chil_win.add(chil_box)

        # Tab 4: Precipitation info.
        prec_box = Gtk.Box()
        prec_box_lbl = Gtk.Label("Precipitation")
        self.prec_list = Gtk.ListStore(str, str)
        self.prec_tree = Gtk.TreeView(model=self.prec_list)
        prec_cate_text = Gtk.CellRendererText()
        prec_cate_col = Gtk.TreeViewColumn("Field", prec_cate_text, text=0)
        self.prec_tree.append_column(prec_cate_col)
        prec_value_text = Gtk.CellRendererText()
        prec_value_col = Gtk.TreeViewColumn("Value", prec_value_text, text=1)
        self.prec_tree.append_column(prec_value_col)
        prec_box.pack_start(self.prec_tree, fill=True, expand=True, padding=0)
        prec_win = Gtk.ScrolledWindow()
        prec_win.set_hexpand(True)
        prec_win.set_vexpand(True)
        prec_win.add(prec_box)

        # Tab 5: Wind info.
        wind_box = Gtk.Box()
        wind_box_lbl = Gtk.Label("Wind")
        self.wind_list = Gtk.ListStore(str, str)
        self.wind_tree = Gtk.TreeView(model=self.wind_list)
        wind_cate_text = Gtk.CellRendererText()
        wind_cate_col = Gtk.TreeViewColumn("Field", wind_cate_text, text=0)
        self.wind_tree.append_column(wind_cate_col)
        wind_value_text = Gtk.CellRendererText()
        wind_value_col = Gtk.TreeViewColumn("Value", wind_value_text, text=1)
        self.wind_tree.append_column(wind_value_col)
        wind_box.pack_start(self.wind_tree, fill=True, expand=True, padding=0)
        wind_win = Gtk.ScrolledWindow()
        wind_win.set_hexpand(True)
        wind_win.set_vexpand(True)
        wind_win.add(wind_box)

        # Tab 6: Humidity info.
        humi_box = Gtk.Box()
        humi_box_lbl = Gtk.Label("Humidity")
        self.humi_list = Gtk.ListStore(str, str)
        self.humi_tree = Gtk.TreeView(model=self.humi_list)
        humi_cate_text = Gtk.CellRendererText()
        humi_cate_col = Gtk.TreeViewColumn("Field", humi_cate_text, text=0)
        self.humi_tree.append_column(humi_cate_col)
        humi_value_text = Gtk.CellRendererText()
        humi_value_col = Gtk.TreeViewColumn("Value", humi_value_text, text=1)
        self.humi_tree.append_column(humi_value_col)
        humi_box.pack_start(self.humi_tree, fill=True, expand=True, padding=0)
        humi_win = Gtk.ScrolledWindow()
        humi_win.set_hexpand(True)
        humi_win.set_vexpand(True)
        humi_win.add(humi_box)

        # Tab 7: Air Pressure info.
        airp_box = Gtk.Box()
        airp_box_lbl = Gtk.Label("Air Pressure")
        self.liststore6 = Gtk.ListStore(str, str)
        self.airp_tree = Gtk.TreeView(model=self.liststore6)
        airp_cate_text = Gtk.CellRendererText()
        airp_cate_col = Gtk.TreeViewColumn("Field", airp_cate_text, text=0)
        self.airp_tree.append_column(airp_cate_col)
        airp_value_text = Gtk.CellRendererText()
        airp_value_col = Gtk.TreeViewColumn("Value", airp_value_text, text=1)
        self.airp_tree.append_column(airp_value_col)
        airp_box.pack_start(self.airp_tree, fill=True, expand=True, padding=0)
        airp_win = Gtk.ScrolledWindow()
        airp_win.set_hexpand(True)
        airp_win.set_vexpand(True)
        airp_win.add(airp_box)

        # Tab 8: Visibility info.
        visi_box = Gtk.Box()
        visi_box_lbl = Gtk.Label("Visibility")
        self.visi_list = Gtk.ListStore(str, str)
        self.visi_tree = Gtk.TreeView(model=self.visi_list)
        visi_cate_text = Gtk.CellRendererText()
        visi_cate_col = Gtk.TreeViewColumn("Field", visi_cate_text, text=0)
        self.visi_tree.append_column(visi_cate_col)
        visi_value_text = Gtk.CellRendererText()
        visi_value_col = Gtk.TreeViewColumn("Value", visi_value_text, text=1)
        self.visi_tree.append_column(visi_value_col)
        visi_box.pack_start(self.visi_tree, fill=True, expand=True, padding=0)
        visi_win = Gtk.ScrolledWindow()
        visi_win.set_hexpand(True)
        visi_win.set_vexpand(True)
        visi_win.add(visi_box)

        # Tab 9: Cloud Cover info.
        clou_box = Gtk.Box()
        clou_box_lbl = Gtk.Label("Cloud Cover")
        self.clou_list = Gtk.ListStore(str, str)
        self.clou_tree = Gtk.TreeView(model=self.clou_list)
        clou_cate_text = Gtk.CellRendererText()
        clou_cate_col = Gtk.TreeViewColumn("Field", clou_cate_text, text=0)
        self.clou_tree.append_column(clou_cate_col)
        clou_value_text = Gtk.CellRendererText()
        clou_value_col = Gtk.TreeViewColumn("Value", clou_value_text, text=1)
        self.clou_tree.append_column(clou_value_col)
        clou_box.pack_start(self.clou_tree, fill=True, expand=True, padding=0)
        clou_win = Gtk.ScrolledWindow()
        clou_win.set_hexpand(True)
        clou_win.set_vexpand(True)
        clou_win.add(clou_box)

        # Tab 10: Notes info.
        note_box = Gtk.Box()
        note_box_lbl = Gtk.Label("Notes")
        self.note_list = Gtk.ListStore(str, str)
        self.note_tree = Gtk.TreeView(model=self.note_list)
        note_cate_text = Gtk.CellRendererText()
        note_cate_col = Gtk.TreeViewColumn("Field", note_cate_text, text=0)
        self.note_tree.append_column(note_cate_col)
        note_value_text = Gtk.CellRendererText()
        note_value_col = Gtk.TreeViewColumn("Value", note_value_text, text=1)
        self.note_tree.append_column(note_value_col)
        note_box.pack_start(self.note_tree, fill=True, expand=True, padding=0)
        note_win = Gtk.ScrolledWindow()
        note_win.set_hexpand(True)
        note_win.set_vexpand(True)
        note_win.add(note_box)

        # Add the tabs to the notebook.
        notebook.append_page(gen_win, gen_box_lbl)
        notebook.append_page(temp_win, temp_box_lbl)
        notebook.append_page(chil_win, chil_box_lbl)
        notebook.append_page(prec_win, prec_box_lbl)
        notebook.append_page(wind_win, wind_box_lbl)
        notebook.append_page(humi_win, humi_box_lbl)
        notebook.append_page(airp_win, airp_box_lbl)
        notebook.append_page(visi_win, visi_box_lbl)
        notebook.append_page(clou_win, clou_box_lbl)
        notebook.append_page(note_win, note_box_lbl)
        info_box.add(notebook)

        # Add the data.
        for i in data[0]:
            self.gen_list.append(i)
        for i in data[1]:
            self.temp_list.append(i)
        for i in data[2]:
            self.chil_list.append(i)
        for i in data[3]:
            self.prec_list.append(i)
        for i in data[4]:
            self.wind_list.append(i)
        for i in data[5]:
            self.humi_list.append(i)
        for i in data[6]:
            self.liststore6.append(i)
        for i in data[7]:
            self.visi_list.append(i)
        for i in data[8]:
            self.clou_list.append(i)
        for i in data[9]:
            self.note_list.append(i)

        # Show the dialog.
        self.show_all()
