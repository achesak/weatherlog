# -*- coding: utf-8 -*-


# This file defines the generic info dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class CurrentWeatherDialog(Gtk.Dialog):
    """Shows the current weather dialog."""
    def __init__(self, parent, title, data):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(400, 350)
        
        # Create the tab notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        info_box = self.get_content_area()
        
        # Add the buttons.
        self.add_button("Export", 9)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Tab 1: Weather info.
        info_box1 = Gtk.Box()
        info_box1_lbl = Gtk.Label("Weather")
        self.liststore1 = Gtk.ListStore(str, str)
        self.treeview1 = Gtk.TreeView(model = self.liststore1)
        cate_text1 = Gtk.CellRendererText()
        cate_col1 = Gtk.TreeViewColumn("Field", cate_text1, text = 0)
        self.treeview1.append_column(cate_col1)
        valu_text1 = Gtk.CellRendererText()
        valu_col1 = Gtk.TreeViewColumn("Value", valu_text1, text = 1)
        self.treeview1.append_column(valu_col1)
        info_box1.pack_start(self.treeview1, fill = True, expand = True, padding = 0)
        scrolled_win1 = Gtk.ScrolledWindow()
        scrolled_win1.set_hexpand(True)
        scrolled_win1.set_vexpand(True)
        scrolled_win1.add(info_box1)
        
        # Tab 2: Location info.
        info_box2 = Gtk.Box()
        info_box2_lbl = Gtk.Label("Location")
        self.liststore2 = Gtk.ListStore(str, str)
        self.treeview2 = Gtk.TreeView(model = self.liststore2)
        cate_text2 = Gtk.CellRendererText()
        cate_col2 = Gtk.TreeViewColumn("Field", cate_text2, text = 0)
        self.treeview2.append_column(cate_col2)
        valu_text2 = Gtk.CellRendererText()
        valu_col2 = Gtk.TreeViewColumn("Value", valu_text2, text = 1)
        self.treeview2.append_column(valu_col2)
        info_box2.pack_start(self.treeview2, fill = True, expand = True, padding = 0)
        scrolled_win2 = Gtk.ScrolledWindow()
        scrolled_win2.set_hexpand(True)
        scrolled_win2.set_vexpand(True)
        scrolled_win2.add(info_box2)
        
        # Tab 3: Forecast info.
        info_box3 = Gtk.Box()
        info_box3_lbl = Gtk.Label("Forecast")
        self.liststore3 = Gtk.ListStore(str, str)
        self.treeview3 = Gtk.TreeView(model = self.liststore3)
        cate_text3 = Gtk.CellRendererText()
        cate_col3 = Gtk.TreeViewColumn("Field", cate_text3, text = 0)
        self.treeview3.append_column(cate_col3)
        valu_text3 = Gtk.CellRendererText()
        valu_col3 = Gtk.TreeViewColumn("Value", valu_text3, text = 1)
        self.treeview3.append_column(valu_col3)
        info_box3.pack_start(self.treeview3, fill = True, expand = True, padding = 0)
        scrolled_win3 = Gtk.ScrolledWindow()
        scrolled_win3.set_hexpand(True)
        scrolled_win3.set_vexpand(True)
        scrolled_win3.add(info_box3)
        
        
        # Add the tabs to the notebook.
        notebook.append_page(scrolled_win1, info_box1_lbl)
        notebook.append_page(scrolled_win2, info_box2_lbl)
        notebook.append_page(scrolled_win3, info_box3_lbl)
        info_box.add(notebook)
        
        # Add the data.
        for i in data[0]:
            self.liststore1.append(i)
        for i in data[1]:
            self.liststore2.append(i)
        for i in data[2]:
            self.liststore3.append(i)
        
        # Show the dialog. There's no need to get the response.
        self.show_all()
