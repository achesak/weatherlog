# -*- coding: utf-8 -*-


# This file defines the info dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class GenericInfoDialog(Gtk.Dialog):
    """Shows the info dialog."""
    
    def __init__(self, parent, title, data):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(700, 400)
        self.add_button("Export", 9)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the tab notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        info_box = self.get_content_area()
        
        # Tab 1: General info.
        info_box1 = Gtk.Box()
        info_box1_lbl = Gtk.Label("General")
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
        
        # Tab 2: Temperature info.
        info_box2 = Gtk.Box()
        info_box2_lbl = Gtk.Label("Temperature")
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
        
        # Tab 9: Wind Chill info.
        info_box9 = Gtk.Box()
        info_box9_lbl = Gtk.Label("Wind Chill")
        self.liststore9 = Gtk.ListStore(str, str)
        self.treeview9 = Gtk.TreeView(model = self.liststore9)
        cate_text9 = Gtk.CellRendererText()
        cate_col9 = Gtk.TreeViewColumn("Field", cate_text9, text = 0)
        self.treeview9.append_column(cate_col9)
        valu_text9 = Gtk.CellRendererText()
        valu_col9 = Gtk.TreeViewColumn("Value", valu_text9, text = 1)
        self.treeview9.append_column(valu_col9)
        info_box9.pack_start(self.treeview9, fill = True, expand = True, padding = 0)
        scrolled_win9 = Gtk.ScrolledWindow()
        scrolled_win9.set_hexpand(True)
        scrolled_win9.set_vexpand(True)
        scrolled_win9.add(info_box9)
        
        # Tab 3: Precipitation info.
        info_box3 = Gtk.Box()
        info_box3_lbl = Gtk.Label("Precipitation")
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
        
        # Tab 4: Wind info.
        info_box4 = Gtk.Box()
        info_box4_lbl = Gtk.Label("Wind")
        self.liststore4 = Gtk.ListStore(str, str)
        self.treeview4 = Gtk.TreeView(model = self.liststore4)
        cate_text4 = Gtk.CellRendererText()
        cate_col4 = Gtk.TreeViewColumn("Field", cate_text4, text = 0)
        self.treeview4.append_column(cate_col4)
        valu_text4 = Gtk.CellRendererText()
        valu_col4 = Gtk.TreeViewColumn("Value", valu_text4, text = 1)
        self.treeview4.append_column(valu_col4)
        info_box4.pack_start(self.treeview4, fill = True, expand = True, padding = 0)
        scrolled_win4 = Gtk.ScrolledWindow()
        scrolled_win4.set_hexpand(True)
        scrolled_win4.set_vexpand(True)
        scrolled_win4.add(info_box4)
        
        # Tab 5: Humidity info.
        info_box5 = Gtk.Box()
        info_box5_lbl = Gtk.Label("Humidity")
        self.liststore5 = Gtk.ListStore(str, str)
        self.treeview5 = Gtk.TreeView(model = self.liststore5)
        cate_text5 = Gtk.CellRendererText()
        cate_col5 = Gtk.TreeViewColumn("Field", cate_text5, text = 0)
        self.treeview5.append_column(cate_col5)
        valu_text5 = Gtk.CellRendererText()
        valu_col5 = Gtk.TreeViewColumn("Value", valu_text5, text = 1)
        self.treeview5.append_column(valu_col5)
        info_box5.pack_start(self.treeview5, fill = True, expand = True, padding = 0)
        scrolled_win5 = Gtk.ScrolledWindow()
        scrolled_win5.set_hexpand(True)
        scrolled_win5.set_vexpand(True)
        scrolled_win5.add(info_box5)
        
        # Tab 6: Air Pressure info.
        info_box6 = Gtk.Box()
        info_box6_lbl = Gtk.Label("Air Pressure")
        self.liststore6 = Gtk.ListStore(str, str)
        self.treeview6 = Gtk.TreeView(model = self.liststore6)
        cate_text6 = Gtk.CellRendererText()
        cate_col6 = Gtk.TreeViewColumn("Field", cate_text6, text = 0)
        self.treeview6.append_column(cate_col6)
        valu_text6 = Gtk.CellRendererText()
        valu_col6 = Gtk.TreeViewColumn("Value", valu_text6, text = 1)
        self.treeview6.append_column(valu_col6)
        info_box6.pack_start(self.treeview6, fill = True, expand = True, padding = 0)
        scrolled_win6 = Gtk.ScrolledWindow()
        scrolled_win6.set_hexpand(True)
        scrolled_win6.set_vexpand(True)
        scrolled_win6.add(info_box6)
        
        # Tab 10: Visibility info.
        info_box10 = Gtk.Box()
        info_box10_lbl = Gtk.Label("Visibility")
        self.liststore10 = Gtk.ListStore(str, str)
        self.treeview10 = Gtk.TreeView(model = self.liststore10)
        cate_text10 = Gtk.CellRendererText()
        cate_col10 = Gtk.TreeViewColumn("Field", cate_text10, text = 0)
        self.treeview10.append_column(cate_col10)
        valu_text10 = Gtk.CellRendererText()
        valu_col10 = Gtk.TreeViewColumn("Value", valu_text10, text = 1)
        self.treeview10.append_column(valu_col10)
        info_box10.pack_start(self.treeview10, fill = True, expand = True, padding = 0)
        scrolled_win10 = Gtk.ScrolledWindow()
        scrolled_win10.set_hexpand(True)
        scrolled_win10.set_vexpand(True)
        scrolled_win10.add(info_box10)
        
        # Tab 7: Cloud Cover info.
        info_box7 = Gtk.Box()
        info_box7_lbl = Gtk.Label("Cloud Cover")
        self.liststore7 = Gtk.ListStore(str, str)
        self.treeview7 = Gtk.TreeView(model = self.liststore7)
        cate_text7 = Gtk.CellRendererText()
        cate_col7 = Gtk.TreeViewColumn("Field", cate_text7, text = 0)
        self.treeview7.append_column(cate_col7)
        valu_text7 = Gtk.CellRendererText()
        valu_col7 = Gtk.TreeViewColumn("Value", valu_text7, text = 1)
        self.treeview7.append_column(valu_col7)
        info_box7.pack_start(self.treeview7, fill = True, expand = True, padding = 0)
        scrolled_win7 = Gtk.ScrolledWindow()
        scrolled_win7.set_hexpand(True)
        scrolled_win7.set_vexpand(True)
        scrolled_win7.add(info_box7)
        
        # Tab 8: Notes info.
        info_box8 = Gtk.Box()
        info_box8_lbl = Gtk.Label("Notes")
        self.liststore8 = Gtk.ListStore(str, str)
        self.treeview8 = Gtk.TreeView(model = self.liststore8)
        cate_text8 = Gtk.CellRendererText()
        cate_col8 = Gtk.TreeViewColumn("Field", cate_text8, text = 0)
        self.treeview8.append_column(cate_col8)
        valu_text8 = Gtk.CellRendererText()
        valu_col8 = Gtk.TreeViewColumn("Value", valu_text8, text = 1)
        self.treeview8.append_column(valu_col8)
        info_box8.pack_start(self.treeview8, fill = True, expand = True, padding = 0)
        scrolled_win8 = Gtk.ScrolledWindow()
        scrolled_win8.set_hexpand(True)
        scrolled_win8.set_vexpand(True)
        scrolled_win8.add(info_box8)
        
        # Add the tabs to the notebook.
        notebook.append_page(scrolled_win1, info_box1_lbl)
        notebook.append_page(scrolled_win2, info_box2_lbl)
        notebook.append_page(scrolled_win9, info_box9_lbl)
        notebook.append_page(scrolled_win3, info_box3_lbl)
        notebook.append_page(scrolled_win4, info_box4_lbl)
        notebook.append_page(scrolled_win5, info_box5_lbl)
        notebook.append_page(scrolled_win6, info_box6_lbl)
        notebook.append_page(scrolled_win10, info_box10_lbl)
        notebook.append_page(scrolled_win7, info_box7_lbl)
        notebook.append_page(scrolled_win8, info_box8_lbl)
        info_box.add(notebook)
        
        # Add the data.
        for i in data[0]:
            self.liststore1.append(i)
        for i in data[1]:
            self.liststore2.append(i)
        for i in data[2]:
            self.liststore9.append(i)
        for i in data[3]:
            self.liststore3.append(i)
        for i in data[4]:
            self.liststore4.append(i)
        for i in data[5]:
            self.liststore5.append(i)
        for i in data[6]:
            self.liststore6.append(i)
        for i in data[7]:
            self.liststore10.append(i)
        for i in data[8]:
            self.liststore7.append(i)
        for i in data[9]:
            self.liststore8.append(i)
        
        # Show the dialog.
        self.show_all()
