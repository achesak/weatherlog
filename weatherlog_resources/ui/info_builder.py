# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: ui/info_builder.py
# This module implements the function for building the Info tab.
#
################################################################################


# Import Gtk and Gdk for the interface.
from gi.repository import Gtk


def info_builder(self):
    """Builds the Info tab on the main interface."""

    # Create the info frame.
    self.info_frame = Gtk.Box()
    self.info_notebook = Gtk.Notebook()
    self.info_notebook.set_tab_pos(Gtk.PositionType.LEFT)
    self.info_frame.add(self.info_notebook)

    # Tab 1: General info.
    self.info_gen_box = Gtk.Box()
    self.info_gen_box_lbl = Gtk.Label("General")
    self.info_gen_list = Gtk.ListStore(str, str)
    self.info_gen_tree = Gtk.TreeView(model=self.info_gen_list)
    self.info_gen_cate_text = Gtk.CellRendererText()
    self.info_gen_cate_col = Gtk.TreeViewColumn("Field", self.info_gen_cate_text, text=0)
    self.info_gen_tree.append_column(self.info_gen_cate_col)
    self.info_gen_value_text = Gtk.CellRendererText()
    self.info_gen_value_col = Gtk.TreeViewColumn("Value", self.info_gen_value_text, text=1)
    self.info_gen_tree.append_column(self.info_gen_value_col)
    self.info_gen_box.pack_start(self.info_gen_tree, fill=True, expand=True, padding=0)
    self.info_gen_win = Gtk.ScrolledWindow()
    self.info_gen_win.set_hexpand(True)
    self.info_gen_win.set_vexpand(True)
    self.info_gen_win.add(self.info_gen_box)

    # Tab 2: Temperature info.
    self.info_temp_box = Gtk.Box()
    self.info_temp_box_lbl = Gtk.Label("Temperature")
    self.info_temp_list = Gtk.ListStore(str, str)
    self.info_temp_tree = Gtk.TreeView(model=self.info_temp_list)
    self.info_temp_cate_text = Gtk.CellRendererText()
    self.info_temp_cate_col = Gtk.TreeViewColumn("Field", self.info_temp_cate_text, text=0)
    self.info_temp_tree.append_column(self.info_temp_cate_col)
    self.info_temp_value_text = Gtk.CellRendererText()
    self.info_temp_value_col = Gtk.TreeViewColumn("Value", self.info_temp_value_text, text=1)
    self.info_temp_tree.append_column(self.info_temp_value_col)
    self.info_temp_box.pack_start(self.info_temp_tree, fill=True, expand=True, padding=0)
    self.info_temp_win = Gtk.ScrolledWindow()
    self.info_temp_win.set_hexpand(True)
    self.info_temp_win.set_vexpand(True)
    self.info_temp_win.add(self.info_temp_box)

    # Tab 3: Wind Chill info.
    self.info_chil_box = Gtk.Box()
    self.info_chil_box_lbl = Gtk.Label("Wind Chill")
    self.info_chil_list = Gtk.ListStore(str, str)
    self.info_chil_tree = Gtk.TreeView(model=self.info_chil_list)
    self.info_chil_cate_text = Gtk.CellRendererText()
    self.info_chil_cate_col = Gtk.TreeViewColumn("Field", self.info_chil_cate_text, text=0)
    self.info_chil_tree.append_column(self.info_chil_cate_col)
    self.info_chil_value_text = Gtk.CellRendererText()
    self.info_chil_value_col = Gtk.TreeViewColumn("Value", self.info_chil_value_text, text=1)
    self.info_chil_tree.append_column(self.info_chil_value_col)
    self.info_chil_box.pack_start(self.info_chil_tree, fill=True, expand=True, padding=0)
    self.info_chil_win = Gtk.ScrolledWindow()
    self.info_chil_win.set_hexpand(True)
    self.info_chil_win.set_vexpand(True)
    self.info_chil_win.add(self.info_chil_box)

    # Tab 4: Precipitation info.
    self.info_prec_box = Gtk.Box()
    self.info_prec_box_lbl = Gtk.Label("Precipitation")
    self.info_prec_list = Gtk.ListStore(str, str)
    self.info_prec_tree = Gtk.TreeView(model=self.info_prec_list)
    self.info_prec_cate_text = Gtk.CellRendererText()
    self.info_prec_cate_col = Gtk.TreeViewColumn("Field", self.info_prec_cate_text, text=0)
    self.info_prec_tree.append_column(self.info_prec_cate_col)
    self.info_prec_value_text = Gtk.CellRendererText()
    self.info_prec_value_col = Gtk.TreeViewColumn("Value", self.info_prec_value_text, text=1)
    self.info_prec_tree.append_column(self.info_prec_value_col)
    self.info_prec_box.pack_start(self.info_prec_tree, fill=True, expand=True, padding=0)
    self.info_prec_win = Gtk.ScrolledWindow()
    self.info_prec_win.set_hexpand(True)
    self.info_prec_win.set_vexpand(True)
    self.info_prec_win.add(self.info_prec_box)

    # Tab 5: Wind info.
    self.info_wind_box = Gtk.Box()
    self.info_wind_box_lbl = Gtk.Label("Wind")
    self.info_wind_list = Gtk.ListStore(str, str)
    self.info_wind_tree = Gtk.TreeView(model=self.info_wind_list)
    self.info_wind_cate_text = Gtk.CellRendererText()
    self.info_wind_cate_col = Gtk.TreeViewColumn("Field", self.info_wind_cate_text, text=0)
    self.info_wind_tree.append_column(self.info_wind_cate_col)
    self.info_wind_value_text = Gtk.CellRendererText()
    self.info_wind_value_col = Gtk.TreeViewColumn("Value", self.info_wind_value_text, text=1)
    self.info_wind_tree.append_column(self.info_wind_value_col)
    self.info_wind_box.pack_start(self.info_wind_tree, fill=True, expand=True, padding=0)
    self.info_wind_win = Gtk.ScrolledWindow()
    self.info_wind_win.set_hexpand(True)
    self.info_wind_win.set_vexpand(True)
    self.info_wind_win.add(self.info_wind_box)

    # Tab 6: Humidity info.
    self.info_humi_box = Gtk.Box()
    self.info_humi_box_lbl = Gtk.Label("Humidity")
    self.info_humi_list = Gtk.ListStore(str, str)
    self.info_humi_tree = Gtk.TreeView(model=self.info_humi_list)
    self.info_humi_cate_text = Gtk.CellRendererText()
    self.info_humi_cate_col = Gtk.TreeViewColumn("Field", self.info_humi_cate_text, text=0)
    self.info_humi_tree.append_column(self.info_humi_cate_col)
    self.info_humi_value_text = Gtk.CellRendererText()
    self.info_humi_value_col = Gtk.TreeViewColumn("Value", self.info_humi_value_text, text=1)
    self.info_humi_tree.append_column(self.info_humi_value_col)
    self.info_humi_box.pack_start(self.info_humi_tree, fill=True, expand=True, padding=0)
    self.info_humi_win = Gtk.ScrolledWindow()
    self.info_humi_win.set_hexpand(True)
    self.info_humi_win.set_vexpand(True)
    self.info_humi_win.add(self.info_humi_box)

    # Tab 7: Air Pressure info.
    self.info_airp_box = Gtk.Box()
    self.info_airp_box_lbl = Gtk.Label("Air Pressure")
    self.info_airp_list = Gtk.ListStore(str, str)
    self.info_airp_tree = Gtk.TreeView(model=self.info_airp_list)
    self.info_airp_cate_text = Gtk.CellRendererText()
    self.info_airp_cate_col = Gtk.TreeViewColumn("Field", self.info_airp_cate_text, text=0)
    self.info_airp_tree.append_column(self.info_airp_cate_col)
    self.info_airp_value_text = Gtk.CellRendererText()
    self.info_airp_value_col = Gtk.TreeViewColumn("Value", self.info_airp_value_text, text=1)
    self.info_airp_tree.append_column(self.info_airp_value_col)
    self.info_airp_box.pack_start(self.info_airp_tree, fill=True, expand=True, padding=0)
    self.info_airp_win = Gtk.ScrolledWindow()
    self.info_airp_win.set_hexpand(True)
    self.info_airp_win.set_vexpand(True)
    self.info_airp_win.add(self.info_airp_box)

    # Tab 8: Visibility info.
    self.info_visi_box = Gtk.Box()
    self.info_visi_box_lbl = Gtk.Label("Visibility")
    self.info_visi_list = Gtk.ListStore(str, str)
    self.info_visi_tree = Gtk.TreeView(model=self.info_visi_list)
    self.info_visi_cate_text = Gtk.CellRendererText()
    self.info_visi_cate_col = Gtk.TreeViewColumn("Field", self.info_visi_cate_text, text=0)
    self.info_visi_tree.append_column(self.info_visi_cate_col)
    self.info_visi_value_text = Gtk.CellRendererText()
    self.info_visi_value_col = Gtk.TreeViewColumn("Value", self.info_visi_value_text, text=1)
    self.info_visi_tree.append_column(self.info_visi_value_col)
    self.info_visi_box.pack_start(self.info_visi_tree, fill=True, expand=True, padding=0)
    self.info_visi_win = Gtk.ScrolledWindow()
    self.info_visi_win.set_hexpand(True)
    self.info_visi_win.set_vexpand(True)
    self.info_visi_win.add(self.info_visi_box)

    # Tab 9: Cloud Cover info.
    self.info_clou_box = Gtk.Box()
    self.info_clou_box_lbl = Gtk.Label("Cloud Cover")
    self.info_clou_list = Gtk.ListStore(str, str)
    self.info_clou_tree = Gtk.TreeView(model=self.info_clou_list)
    self.info_clou_cate_text = Gtk.CellRendererText()
    self.info_clou_cate_col = Gtk.TreeViewColumn("Field", self.info_clou_cate_text, text=0)
    self.info_clou_tree.append_column(self.info_clou_cate_col)
    self.info_clou_value_text = Gtk.CellRendererText()
    self.info_clou_value_col = Gtk.TreeViewColumn("Value", self.info_clou_value_text, text=1)
    self.info_clou_tree.append_column(self.info_clou_value_col)
    self.info_clou_box.pack_start(self.info_clou_tree, fill=True, expand=True, padding=0)
    self.info_clou_win = Gtk.ScrolledWindow()
    self.info_clou_win.set_hexpand(True)
    self.info_clou_win.set_vexpand(True)
    self.info_clou_win.add(self.info_clou_box)

    # Tab 10: Notes info.
    self.info_note_box = Gtk.Box()
    self.info_note_box_lbl = Gtk.Label("Notes")
    self.info_note_list = Gtk.ListStore(str, str)
    self.info_note_tree = Gtk.TreeView(model=self.info_note_list)
    self.info_note_cate_text = Gtk.CellRendererText()
    self.info_note_cate_col = Gtk.TreeViewColumn("Field", self.info_note_cate_text, text=0)
    self.info_note_tree.append_column(self.info_note_cate_col)
    self.info_note_value_text = Gtk.CellRendererText()
    self.info_note_value_col = Gtk.TreeViewColumn("Value", self.info_note_value_text, text=1)
    self.info_note_tree.append_column(self.info_note_value_col)
    self.info_note_box.pack_start(self.info_note_tree, fill=True, expand=True, padding=0)
    self.info_note_win = Gtk.ScrolledWindow()
    self.info_note_win.set_hexpand(True)
    self.info_note_win.set_vexpand(True)
    self.info_note_win.add(self.info_note_box)

    # Add the tabs.
    self.info_notebook.append_page(self.info_gen_win, self.info_gen_box_lbl)
    self.info_notebook.append_page(self.info_temp_win, self.info_temp_box_lbl)
    self.info_notebook.append_page(self.info_chil_win, self.info_chil_box_lbl)
    self.info_notebook.append_page(self.info_prec_win, self.info_prec_box_lbl)
    self.info_notebook.append_page(self.info_wind_win, self.info_wind_box_lbl)
    self.info_notebook.append_page(self.info_humi_win, self.info_humi_box_lbl)
    self.info_notebook.append_page(self.info_airp_win, self.info_airp_box_lbl)
    self.info_notebook.append_page(self.info_visi_win, self.info_visi_box_lbl)
    self.info_notebook.append_page(self.info_clou_win, self.info_clou_box_lbl)
    self.info_notebook.append_page(self.info_note_win, self.info_note_box_lbl)
