# -*- coding: utf-8 -*-


# This file defines the chart dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class GenericChartDialog(Gtk.Dialog):
    """Shows the chart dialog."""
    
    def __init__(self, parent, title, data):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(1000, 500)
        self.add_button("Export", 9)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the tab notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        chart_box = self.get_content_area()
        
        # Tab 1: Temperature chart.
        chart_box1 = Gtk.Box()
        chart_box1_lbl = Gtk.Label("Temperature")
        self.liststore1 = Gtk.ListStore(str, str, str, str, str, str)
        self.treeview1 = Gtk.TreeView(model = self.liststore1)
        day_text1 = Gtk.CellRendererText()
        day_col1 = Gtk.TreeViewColumn("Day", day_text1, text = 0)
        self.treeview1.append_column(day_col1)
        valu_text1 = Gtk.CellRendererText()
        valu_col1 = Gtk.TreeViewColumn("Value", valu_text1, text = 1)
        self.treeview1.append_column(valu_col1)
        avg_text1 = Gtk.CellRendererText()
        avg_col1 = Gtk.TreeViewColumn("Average Difference", valu_text1, text = 2)
        self.treeview1.append_column(avg_col1)
        low_text1 = Gtk.CellRendererText()
        low_col1 = Gtk.TreeViewColumn("Low Difference", low_text1, text = 3)
        self.treeview1.append_column(low_col1)
        high_text1 = Gtk.CellRendererText()
        high_col1 = Gtk.TreeViewColumn("High Difference", high_text1, text = 4)
        self.treeview1.append_column(high_col1)
        med_text1 = Gtk.CellRendererText()
        med_col1 = Gtk.TreeViewColumn("Median Difference", med_text1, text = 5)
        self.treeview1.append_column(med_col1)
        chart_box1.pack_start(self.treeview1, fill = True, expand = True, padding = 0)
        
        # Tab 2: Wind Chill chart.
        chart_box6 = Gtk.Box()
        chart_box6_lbl = Gtk.Label("Wind Chill")
        self.liststore6 = Gtk.ListStore(str, str, str, str, str, str)
        self.treeview6 = Gtk.TreeView(model = self.liststore6)
        day_text6 = Gtk.CellRendererText()
        day_col6 = Gtk.TreeViewColumn("Day", day_text6, text = 0)
        self.treeview6.append_column(day_col6)
        valu_text6 = Gtk.CellRendererText()
        valu_col6 = Gtk.TreeViewColumn("Value", valu_text6, text = 1)
        self.treeview6.append_column(valu_col6)
        avg_text6 = Gtk.CellRendererText()
        avg_col6 = Gtk.TreeViewColumn("Average Difference", valu_text6, text = 2)
        self.treeview6.append_column(avg_col6)
        low_text6 = Gtk.CellRendererText()
        low_col6 = Gtk.TreeViewColumn("Low Difference", low_text6, text = 3)
        self.treeview6.append_column(low_col6)
        high_text6 = Gtk.CellRendererText()
        high_col6 = Gtk.TreeViewColumn("High Difference", high_text6, text = 4)
        self.treeview6.append_column(high_col6)
        med_text6 = Gtk.CellRendererText()
        med_col6 = Gtk.TreeViewColumn("Median Difference", med_text6, text = 5)
        self.treeview6.append_column(med_col6)
        chart_box6.pack_start(self.treeview6, fill = True, expand = True, padding = 0)
        
        # Tab 3: Precipitation chart.
        chart_box2 = Gtk.Box()
        chart_box2_lbl = Gtk.Label("Precipitation")
        self.liststore2 = Gtk.ListStore(str, str, str, str, str, str)
        self.treeview2 = Gtk.TreeView(model = self.liststore2)
        day_text2 = Gtk.CellRendererText()
        day_col2 = Gtk.TreeViewColumn("Day", day_text2, text = 0)
        self.treeview2.append_column(day_col2)
        valu_text2 = Gtk.CellRendererText()
        valu_col2 = Gtk.TreeViewColumn("Value", valu_text2, text = 1)
        self.treeview2.append_column(valu_col2)
        avg_text2 = Gtk.CellRendererText()
        avg_col2 = Gtk.TreeViewColumn("Average Difference", valu_text2, text = 2)
        self.treeview2.append_column(avg_col2)
        low_text2 = Gtk.CellRendererText()
        low_col2 = Gtk.TreeViewColumn("Low Difference", low_text2, text = 3)
        self.treeview2.append_column(low_col2)
        high_text2 = Gtk.CellRendererText()
        high_col2 = Gtk.TreeViewColumn("High Difference", high_text2, text = 4)
        self.treeview2.append_column(high_col2)
        med_text2 = Gtk.CellRendererText()
        med_col2 = Gtk.TreeViewColumn("Median Difference", med_text2, text = 5)
        self.treeview2.append_column(med_col2)
        chart_box2.pack_start(self.treeview2, fill = True, expand = True, padding = 0)
        
        # Tab 4: Wind chart.
        chart_box3 = Gtk.Box()
        chart_box3_lbl = Gtk.Label("Wind")
        self.liststore3 = Gtk.ListStore(str, str, str, str, str, str)
        self.treeview3 = Gtk.TreeView(model = self.liststore3)
        day_text3 = Gtk.CellRendererText()
        day_col3 = Gtk.TreeViewColumn("Day", day_text3, text = 0)
        self.treeview3.append_column(day_col3)
        valu_text3 = Gtk.CellRendererText()
        valu_col3 = Gtk.TreeViewColumn("Value", valu_text3, text = 1)
        self.treeview3.append_column(valu_col3)
        avg_text3 = Gtk.CellRendererText()
        avg_col3 = Gtk.TreeViewColumn("Average Difference", valu_text3, text = 2)
        self.treeview3.append_column(avg_col3)
        low_text3 = Gtk.CellRendererText()
        low_col3 = Gtk.TreeViewColumn("Low Difference", low_text3, text = 3)
        self.treeview3.append_column(low_col3)
        high_text3 = Gtk.CellRendererText()
        high_col3 = Gtk.TreeViewColumn("High Difference", high_text3, text = 4)
        self.treeview3.append_column(high_col3)
        med_text3 = Gtk.CellRendererText()
        med_col3 = Gtk.TreeViewColumn("Median Difference", med_text3, text = 5)
        self.treeview3.append_column(med_col3)
        chart_box3.pack_start(self.treeview3, fill = True, expand = True, padding = 0)
        
        # Tab 5: Humidity chart.
        chart_box4 = Gtk.Box()
        chart_box4_lbl = Gtk.Label("Humidity")
        self.liststore4 = Gtk.ListStore(str, str, str, str, str, str)
        self.treeview4 = Gtk.TreeView(model = self.liststore4)
        day_text4 = Gtk.CellRendererText()
        day_col4 = Gtk.TreeViewColumn("Day", day_text4, text = 0)
        self.treeview4.append_column(day_col4)
        valu_text4 = Gtk.CellRendererText()
        valu_col4 = Gtk.TreeViewColumn("Value", valu_text4, text = 1)
        self.treeview4.append_column(valu_col4)
        avg_text4 = Gtk.CellRendererText()
        avg_col4 = Gtk.TreeViewColumn("Average Difference", valu_text4, text = 2)
        self.treeview4.append_column(avg_col4)
        low_text4 = Gtk.CellRendererText()
        low_col4 = Gtk.TreeViewColumn("Low Difference", low_text4, text = 3)
        self.treeview4.append_column(low_col4)
        high_text4 = Gtk.CellRendererText()
        high_col4 = Gtk.TreeViewColumn("High Difference", high_text4, text = 4)
        self.treeview4.append_column(high_col4)
        med_text4 = Gtk.CellRendererText()
        med_col4 = Gtk.TreeViewColumn("Median Difference", med_text4, text = 5)
        self.treeview4.append_column(med_col4)
        chart_box4.pack_start(self.treeview4, fill = True, expand = True, padding = 0)
        
        # Tab 6: Air Pressure chart.
        chart_box5 = Gtk.Box()
        chart_box5_lbl = Gtk.Label("Air Pressure")
        self.liststore5 = Gtk.ListStore(str, str, str, str, str, str)
        self.treeview5 = Gtk.TreeView(model = self.liststore5)
        day_text5 = Gtk.CellRendererText()
        day_col5 = Gtk.TreeViewColumn("Day", day_text5, text = 0)
        self.treeview5.append_column(day_col5)
        valu_text5 = Gtk.CellRendererText()
        valu_col5 = Gtk.TreeViewColumn("Value", valu_text5, text = 1)
        self.treeview5.append_column(valu_col5)
        avg_text5 = Gtk.CellRendererText()
        avg_col5 = Gtk.TreeViewColumn("Average Difference", valu_text5, text = 2)
        self.treeview5.append_column(avg_col5)
        low_text5 = Gtk.CellRendererText()
        low_col5 = Gtk.TreeViewColumn("Low Difference", low_text5, text = 3)
        self.treeview5.append_column(low_col5)
        high_text5 = Gtk.CellRendererText()
        high_col5 = Gtk.TreeViewColumn("High Difference", high_text5, text = 4)
        self.treeview5.append_column(high_col5)
        med_text5 = Gtk.CellRendererText()
        med_col5 = Gtk.TreeViewColumn("Median Difference", med_text5, text = 5)
        self.treeview5.append_column(med_col5)
        chart_box5.pack_start(self.treeview5, fill = True, expand = True, padding = 0)
        
        # Tab 7: Visibility chart.
        chart_box7 = Gtk.Box()
        chart_box7_lbl = Gtk.Label("Visibility")
        self.liststore7 = Gtk.ListStore(str, str, str, str, str, str)
        self.treeview7 = Gtk.TreeView(model = self.liststore7)
        day_text7 = Gtk.CellRendererText()
        day_col7 = Gtk.TreeViewColumn("Day", day_text7, text = 0)
        self.treeview7.append_column(day_col7)
        valu_text7 = Gtk.CellRendererText()
        valu_col7 = Gtk.TreeViewColumn("Value", valu_text7, text = 1)
        self.treeview7.append_column(valu_col7)
        avg_text7 = Gtk.CellRendererText()
        avg_col7 = Gtk.TreeViewColumn("Average Difference", valu_text7, text = 2)
        self.treeview7.append_column(avg_col7)
        low_text7 = Gtk.CellRendererText()
        low_col7 = Gtk.TreeViewColumn("Low Difference", low_text7, text = 3)
        self.treeview7.append_column(low_col7)
        high_text7 = Gtk.CellRendererText()
        high_col7 = Gtk.TreeViewColumn("High Difference", high_text7, text = 4)
        self.treeview7.append_column(high_col7)
        med_text7 = Gtk.CellRendererText()
        med_col7 = Gtk.TreeViewColumn("Median Difference", med_text7, text = 5)
        self.treeview7.append_column(med_col7)
        chart_box7.pack_start(self.treeview7, fill = True, expand = True, padding = 0)
        
        # Create the ScrolledWindow for displaying the lists with scrollbars.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        scrolled_win.add(notebook)
        chart_box.add(scrolled_win)
        
        # Add the tabs to the notebook.
        notebook.append_page(chart_box1, chart_box1_lbl)
        notebook.append_page(chart_box6, chart_box6_lbl)
        notebook.append_page(chart_box2, chart_box2_lbl)
        notebook.append_page(chart_box3, chart_box3_lbl)
        notebook.append_page(chart_box4, chart_box4_lbl)
        notebook.append_page(chart_box5, chart_box5_lbl)
        notebook.append_page(chart_box7, chart_box7_lbl)
        
        # Add the data.
        for i in data[0]:
            self.liststore1.append(i)
        for i in data[1]:
            self.liststore6.append(i)
        for i in data[2]:
            self.liststore2.append(i)
        for i in data[3]:
            self.liststore3.append(i)
        for i in data[4]:
            self.liststore4.append(i)
        for i in data[5]:
            self.liststore5.append(i)
        for i in data[6]:
            self.liststore7.append(i)
        
        # Show the dialog.
        self.show_all()
