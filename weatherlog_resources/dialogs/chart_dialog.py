# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/chart_dialog.py
# This dialog shows the dataset charts.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk


class ChartDialog(Gtk.Dialog):
    """Shows the chart dialog."""
    
    def __init__(self, parent, title, data):
        """Create the dialog."""
        
        Gtk.Dialog.__init__(self, title, parent)
        self.set_default_size(1000, 500)
        self.add_button("Export", 9)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the tab notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        chart_box = self.get_content_area()
        
        # Tab 1: Temperature chart.
        temp_box = Gtk.Box()
        temp_box.set_hexpand(True)
        temp_box.set_vexpand(True)
        temp_box_lbl = Gtk.Label("Temperature")
        self.temp_list = Gtk.ListStore(str, str, str, str, str, str)
        self.temp_tree = Gtk.TreeView(model = self.temp_list)
        temp_day_text = Gtk.CellRendererText()
        temp_day_col = Gtk.TreeViewColumn("Day", temp_day_text, text = 0)
        temp_day_col.set_min_width(150)
        self.temp_tree.append_column(temp_day_col)
        temp_value_text = Gtk.CellRendererText()
        temp_value_col = Gtk.TreeViewColumn("Value", temp_value_text, text = 1)
        temp_value_col.set_min_width(100)
        self.temp_tree.append_column(temp_value_col)
        temp_avg_text = Gtk.CellRendererText()
        temp_avg_col = Gtk.TreeViewColumn("Average Difference", temp_value_text, text = 2)
        self.temp_tree.append_column(temp_avg_col)
        temp_low_text = Gtk.CellRendererText()
        temp_low_col = Gtk.TreeViewColumn("Low Difference", temp_low_text, text = 3)
        self.temp_tree.append_column(temp_low_col)
        temp_high_text = Gtk.CellRendererText()
        temp_high_col = Gtk.TreeViewColumn("High Difference", temp_high_text, text = 4)
        self.temp_tree.append_column(temp_high_col)
        temp_med_text = Gtk.CellRendererText()
        temp_med_col = Gtk.TreeViewColumn("Median Difference", temp_med_text, text = 5)
        self.temp_tree.append_column(temp_med_col)
        temp_box.pack_start(self.temp_tree, fill = True, expand = True, padding = 0)
        
        # Tab 2: Wind Chill chart.
        chil_box = Gtk.Box()
        chil_box_lbl = Gtk.Label("Wind Chill")
        self.chil_list = Gtk.ListStore(str, str, str, str, str, str)
        self.chil_tree = Gtk.TreeView(model = self.chil_list)
        chil_day_text = Gtk.CellRendererText()
        chil_day_col = Gtk.TreeViewColumn("Day", chil_day_text, text = 0)
        chil_day_col.set_min_width(150)
        self.chil_tree.append_column(chil_day_col)
        chil_value_text = Gtk.CellRendererText()
        chil_value_col = Gtk.TreeViewColumn("Value", chil_value_text, text = 1)
        chil_value_col.set_min_width(100)
        self.chil_tree.append_column(chil_value_col)
        chil_avg_text = Gtk.CellRendererText()
        chil_avg_col = Gtk.TreeViewColumn("Average Difference", chil_value_text, text = 2)
        self.chil_tree.append_column(chil_avg_col)
        chil_low_text = Gtk.CellRendererText()
        chil_low_col = Gtk.TreeViewColumn("Low Difference", chil_low_text, text = 3)
        self.chil_tree.append_column(chil_low_col)
        chil_high_text = Gtk.CellRendererText()
        chil_high_col = Gtk.TreeViewColumn("High Difference", chil_high_text, text = 4)
        self.chil_tree.append_column(chil_high_col)
        chil_med_text = Gtk.CellRendererText()
        chil_med_col = Gtk.TreeViewColumn("Median Difference", chil_med_text, text = 5)
        self.chil_tree.append_column(chil_med_col)
        chil_box.pack_start(self.chil_tree, fill = True, expand = True, padding = 0)
        
        # Tab 3: Precipitation chart.
        prec_box = Gtk.Box()
        prec_box_lbl = Gtk.Label("Precipitation")
        self.prec_list = Gtk.ListStore(str, str, str, str, str, str)
        self.prec_tree = Gtk.TreeView(model = self.prec_list)
        prec_day_text = Gtk.CellRendererText()
        prec_day_col = Gtk.TreeViewColumn("Day", prec_day_text, text = 0)
        prec_day_col.set_min_width(150)
        self.prec_tree.append_column(prec_day_col)
        prec_value_text = Gtk.CellRendererText()
        prec_value_col = Gtk.TreeViewColumn("Value", prec_value_text, text = 1)
        prec_value_col.set_min_width(100)
        self.prec_tree.append_column(prec_value_col)
        prec_avg_text = Gtk.CellRendererText()
        prec_avg_col = Gtk.TreeViewColumn("Average Difference", prec_value_text, text = 2)
        self.prec_tree.append_column(prec_avg_col)
        prec_low_text = Gtk.CellRendererText()
        prec_low_col = Gtk.TreeViewColumn("Low Difference", prec_low_text, text = 3)
        self.prec_tree.append_column(prec_low_col)
        prec_high_text = Gtk.CellRendererText()
        prec_high_col = Gtk.TreeViewColumn("High Difference", prec_high_text, text = 4)
        self.prec_tree.append_column(prec_high_col)
        prec_med_text = Gtk.CellRendererText()
        prec_med_col = Gtk.TreeViewColumn("Median Difference", prec_med_text, text = 5)
        self.prec_tree.append_column(prec_med_col)
        prec_box.pack_start(self.prec_tree, fill = True, expand = True, padding = 0)
        
        # Tab 4: Wind chart.
        wind_box = Gtk.Box()
        wind_box_lbl = Gtk.Label("Wind")
        self.wind_list = Gtk.ListStore(str, str, str, str, str, str)
        self.wind_tree = Gtk.TreeView(model = self.wind_list)
        wind_day_text = Gtk.CellRendererText()
        wind_day_col = Gtk.TreeViewColumn("Day", wind_day_text, text = 0)
        wind_day_col.set_min_width(150)
        self.wind_tree.append_column(wind_day_col)
        wind_value_text = Gtk.CellRendererText()
        wind_value_col = Gtk.TreeViewColumn("Value", wind_value_text, text = 1)
        wind_value_col.set_min_width(100)
        self.wind_tree.append_column(wind_value_col)
        wind_avg_text = Gtk.CellRendererText()
        wind_avg_col = Gtk.TreeViewColumn("Average Difference", wind_value_text, text = 2)
        self.wind_tree.append_column(wind_avg_col)
        wind_low_text = Gtk.CellRendererText()
        wind_low_col = Gtk.TreeViewColumn("Low Difference", wind_low_text, text = 3)
        self.wind_tree.append_column(wind_low_col)
        wind_high_text = Gtk.CellRendererText()
        wind_high_col = Gtk.TreeViewColumn("High Difference", wind_high_text, text = 4)
        self.wind_tree.append_column(wind_high_col)
        wind_med_text = Gtk.CellRendererText()
        wind_med_col = Gtk.TreeViewColumn("Median Difference", wind_med_text, text = 5)
        self.wind_tree.append_column(wind_med_col)
        wind_box.pack_start(self.wind_tree, fill = True, expand = True, padding = 0)
        
        # Tab 5: Humidity chart.
        humi_box = Gtk.Box()
        humi_box_lbl = Gtk.Label("Humidity")
        self.humi_list = Gtk.ListStore(str, str, str, str, str, str)
        self.humi_tree = Gtk.TreeView(model = self.humi_list)
        humi_day_text = Gtk.CellRendererText()
        humi_day_col = Gtk.TreeViewColumn("Day", humi_day_text, text = 0)
        humi_day_col.set_min_width(150)
        self.humi_tree.append_column(humi_day_col)
        humi_value_text = Gtk.CellRendererText()
        humi_value_col = Gtk.TreeViewColumn("Value", humi_value_text, text = 1)
        humi_value_col.set_min_width(100)
        self.humi_tree.append_column(humi_value_col)
        humi_avg_text = Gtk.CellRendererText()
        humi_avg_col = Gtk.TreeViewColumn("Average Difference", humi_value_text, text = 2)
        self.humi_tree.append_column(humi_avg_col)
        humi_low_text = Gtk.CellRendererText()
        humi_low_col = Gtk.TreeViewColumn("Low Difference", humi_low_text, text = 3)
        self.humi_tree.append_column(humi_low_col)
        humi_high_text = Gtk.CellRendererText()
        humi_high_col = Gtk.TreeViewColumn("High Difference", humi_high_text, text = 4)
        self.humi_tree.append_column(humi_high_col)
        humi_med_text = Gtk.CellRendererText()
        humi_med_col = Gtk.TreeViewColumn("Median Difference", humi_med_text, text = 5)
        self.humi_tree.append_column(humi_med_col)
        humi_box.pack_start(self.humi_tree, fill = True, expand = True, padding = 0)
        
        # Tab 6: Air Pressure chart.
        airp_box = Gtk.Box()
        airp_box_lbl = Gtk.Label("Air Pressure")
        self.airp_list = Gtk.ListStore(str, str, str, str, str, str)
        self.airp_tree = Gtk.TreeView(model = self.airp_list)
        airp_day_text = Gtk.CellRendererText()
        airp_day_col = Gtk.TreeViewColumn("Day", airp_day_text, text = 0)
        airp_day_col.set_min_width(150)
        self.airp_tree.append_column(airp_day_col)
        airp_value_text = Gtk.CellRendererText()
        airp_value_col = Gtk.TreeViewColumn("Value", airp_value_text, text = 1)
        airp_value_col.set_min_width(100)
        self.airp_tree.append_column(airp_value_col)
        airp_avg_text = Gtk.CellRendererText()
        airp_avg_col = Gtk.TreeViewColumn("Average Difference", airp_value_text, text = 2)
        self.airp_tree.append_column(airp_avg_col)
        airp_low_text = Gtk.CellRendererText()
        airp_low_col = Gtk.TreeViewColumn("Low Difference", airp_low_text, text = 3)
        self.airp_tree.append_column(airp_low_col)
        high_text5 = Gtk.CellRendererText()
        airp_high_col = Gtk.TreeViewColumn("High Difference", high_text5, text = 4)
        self.airp_tree.append_column(airp_high_col)
        airp_med_text = Gtk.CellRendererText()
        airp_med_col = Gtk.TreeViewColumn("Median Difference", airp_med_text, text = 5)
        self.airp_tree.append_column(airp_med_col)
        airp_box.pack_start(self.airp_tree, fill = True, expand = True, padding = 0)
        
        # Tab 7: Visibility chart.
        visi_box = Gtk.Box()
        visi_box_lbl = Gtk.Label("Visibility")
        self.visi_list = Gtk.ListStore(str, str, str, str, str, str)
        self.visi_tree = Gtk.TreeView(model = self.visi_list)
        visi_day_text = Gtk.CellRendererText()
        visi_day_col = Gtk.TreeViewColumn("Day", visi_day_text, text = 0)
        visi_day_col.set_min_width(150)
        self.visi_tree.append_column(visi_day_col)
        visi_value_text = Gtk.CellRendererText()
        visi_value_col = Gtk.TreeViewColumn("Value", visi_value_text, text = 1)
        visi_value_col.set_min_width(100)
        self.visi_tree.append_column(visi_value_col)
        visi_avg_text = Gtk.CellRendererText()
        visi_avg_col = Gtk.TreeViewColumn("Average Difference", visi_value_text, text = 2)
        self.visi_tree.append_column(visi_avg_col)
        visi_low_text = Gtk.CellRendererText()
        visi_low_col = Gtk.TreeViewColumn("Low Difference", visi_low_text, text = 3)
        self.visi_tree.append_column(visi_low_col)
        visi_high_text = Gtk.CellRendererText()
        visi_high_col = Gtk.TreeViewColumn("High Difference", visi_high_text, text = 4)
        self.visi_tree.append_column(visi_high_col)
        visi_med_text = Gtk.CellRendererText()
        visi_med_col = Gtk.TreeViewColumn("Median Difference", visi_med_text, text = 5)
        self.visi_tree.append_column(visi_med_col)
        visi_box.pack_start(self.visi_tree, fill = True, expand = True, padding = 0)
        
        # Create the ScrolledWindow for displaying the lists with scrollbars.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        scrolled_win.add(notebook)
        chart_box.add(scrolled_win)
        
        # Add the tabs to the notebook.
        notebook.append_page(temp_box, temp_box_lbl)
        notebook.append_page(chil_box, chil_box_lbl)
        notebook.append_page(prec_box, prec_box_lbl)
        notebook.append_page(wind_box, wind_box_lbl)
        notebook.append_page(humi_box, humi_box_lbl)
        notebook.append_page(airp_box, airp_box_lbl)
        notebook.append_page(visi_box, visi_box_lbl)
        
        # Add the data.
        for i in data[0]:
            self.temp_list.append(i)
        for i in data[1]:
            self.chil_list.append(i)
        for i in data[2]:
            self.prec_list.append(i)
        for i in data[3]:
            self.wind_list.append(i)
        for i in data[4]:
            self.humi_list.append(i)
        for i in data[5]:
            self.airp_list.append(i)
        for i in data[6]:
            self.visi_list.append(i)
        
        # Show the dialog.
        self.show_all()
