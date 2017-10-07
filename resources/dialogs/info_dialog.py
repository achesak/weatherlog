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
from resources.constants import *

# Import matplotlib for graphing.
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas


class InfoDialog(Gtk.Dialog):
    """Shows the info dialog."""

    def __init__(self, parent, title, subtitle, info_data, table_data, graph_data, config, graph_meta):
        """Create the dialog."""

        Gtk.Dialog.__init__(self, title, parent, use_header_bar=True)
        self.set_default_size(1200, 700)
        self.add_button("Export", DialogResponse.EXPORT)

        # Create the header bar.
        header = self.get_header_bar()
        header.set_title(title)
        header.set_subtitle(subtitle)
        header.set_show_close_button(True)

        # Create the displays.
        self.build_info()
        self.build_tables()
        self.build_graphs(graph_data, config, graph_meta)

        # Add the info data.
        for i in info_data[0]:
            self.info_gen_list.append(i)
        for i in info_data[1]:
            self.info_temp_list.append(i)
        for i in info_data[2]:
            self.info_chil_list.append(i)
        for i in info_data[3]:
            self.info_prec_list.append(i)
        for i in info_data[4]:
            self.info_wind_list.append(i)
        for i in info_data[5]:
            self.info_humi_list.append(i)
        for i in info_data[6]:
            self.info_airp_list.append(i)
        for i in info_data[7]:
            self.info_visi_list.append(i)
        for i in info_data[8]:
            self.info_clou_list.append(i)
        for i in info_data[9]:
            self.info_note_list.append(i)

        # Add the table data.
        for i in table_data[0]:
            self.table_temp_list.append(i)
        for i in table_data[1]:
            self.table_chil_list.append(i)
        for i in table_data[2]:
            self.table_prec_list.append(i)
        for i in table_data[3]:
            self.table_wind_list.append(i)
        for i in table_data[4]:
            self.table_humi_list.append(i)
        for i in table_data[5]:
            self.table_airp_list.append(i)
        for i in table_data[6]:
            self.table_visi_list.append(i)

        # Create the stack.
        stack = Gtk.Stack()
        stack.set_hexpand(True)
        stack.set_vexpand(True)
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        header.set_custom_title(stack_switcher)
        self.get_content_area().add(stack)

        # Build the stack.
        stack.add_titled(self.info_notebook, "info", "Info")
        stack.add_titled(self.table_notebook, "tables", "Tables")
        stack.add_titled(self.graph_notebook, "graphs", "Graphs")

        # Show the dialog.
        self.show_all()

    def build_info(self):
        """Builds the info display."""

        # Create the tab notebook.
        info_notebook = Gtk.Notebook()
        info_notebook.set_tab_pos(Gtk.PositionType.LEFT)
        self.info_notebook = info_notebook

        # Tab 1: General info.
        gen_box = Gtk.Box()
        gen_box_lbl = Gtk.Label("General")
        self.info_gen_list = Gtk.ListStore(str, str)
        self.info_gen_tree = Gtk.TreeView(model=self.info_gen_list)
        gen_cate_text = Gtk.CellRendererText()
        gen_cate_col = Gtk.TreeViewColumn("Field", gen_cate_text, text=0)
        gen_cate_col.set_min_width(400)
        self.info_gen_tree.append_column(gen_cate_col)
        gen_value_text = Gtk.CellRendererText()
        gen_value_col = Gtk.TreeViewColumn("Value", gen_value_text, text=1)
        self.info_gen_tree.append_column(gen_value_col)
        gen_box.pack_start(self.info_gen_tree, fill=True, expand=True, padding=0)
        gen_win = Gtk.ScrolledWindow()
        gen_win.set_hexpand(True)
        gen_win.set_vexpand(True)
        gen_win.add(gen_box)

        # Tab 2: Temperature info.
        temp_box = Gtk.Box()
        temp_box_lbl = Gtk.Label("Temperature")
        self.info_temp_list = Gtk.ListStore(str, str)
        self.info_temp_tree = Gtk.TreeView(model=self.info_temp_list)
        temp_cate_text = Gtk.CellRendererText()
        temp_cate_col = Gtk.TreeViewColumn("Field", temp_cate_text, text=0)
        temp_cate_col.set_min_width(400)
        self.info_temp_tree.append_column(temp_cate_col)
        temp_value_text = Gtk.CellRendererText()
        temp_value_col = Gtk.TreeViewColumn("Value", temp_value_text, text=1)
        self.info_temp_tree.append_column(temp_value_col)
        temp_box.pack_start(self.info_temp_tree, fill=True, expand=True, padding=0)
        temp_win = Gtk.ScrolledWindow()
        temp_win.set_hexpand(True)
        temp_win.set_vexpand(True)
        temp_win.add(temp_box)

        # Tab 3: Wind Chill info.
        chil_box = Gtk.Box()
        chil_box_lbl = Gtk.Label("Wind Chill")
        self.info_chil_list = Gtk.ListStore(str, str)
        self.info_chil_tree = Gtk.TreeView(model=self.info_chil_list)
        chil_cate_text = Gtk.CellRendererText()
        chil_cate_col = Gtk.TreeViewColumn("Field", chil_cate_text, text=0)
        chil_cate_col.set_min_width(400)
        self.info_chil_tree.append_column(chil_cate_col)
        chil_value_text = Gtk.CellRendererText()
        chil_value_col = Gtk.TreeViewColumn("Value", chil_value_text, text=1)
        self.info_chil_tree.append_column(chil_value_col)
        chil_box.pack_start(self.info_chil_tree, fill=True, expand=True, padding=0)
        chil_win = Gtk.ScrolledWindow()
        chil_win.set_hexpand(True)
        chil_win.set_vexpand(True)
        chil_win.add(chil_box)

        # Tab 4: Precipitation info.
        prec_box = Gtk.Box()
        prec_box_lbl = Gtk.Label("Precipitation")
        self.info_prec_list = Gtk.ListStore(str, str)
        self.info_prec_tree = Gtk.TreeView(model=self.info_prec_list)
        prec_cate_text = Gtk.CellRendererText()
        prec_cate_col = Gtk.TreeViewColumn("Field", prec_cate_text, text=0)
        prec_cate_col.set_min_width(400)
        self.info_prec_tree.append_column(prec_cate_col)
        prec_value_text = Gtk.CellRendererText()
        prec_value_col = Gtk.TreeViewColumn("Value", prec_value_text, text=1)
        self.info_prec_tree.append_column(prec_value_col)
        prec_box.pack_start(self.info_prec_tree, fill=True, expand=True, padding=0)
        prec_win = Gtk.ScrolledWindow()
        prec_win.set_hexpand(True)
        prec_win.set_vexpand(True)
        prec_win.add(prec_box)

        # Tab 5: Wind info.
        wind_box = Gtk.Box()
        wind_box_lbl = Gtk.Label("Wind")
        self.info_wind_list = Gtk.ListStore(str, str)
        self.info_wind_tree = Gtk.TreeView(model=self.info_wind_list)
        wind_cate_text = Gtk.CellRendererText()
        wind_cate_col = Gtk.TreeViewColumn("Field", wind_cate_text, text=0)
        wind_cate_col.set_min_width(400)
        self.info_wind_tree.append_column(wind_cate_col)
        wind_value_text = Gtk.CellRendererText()
        wind_value_col = Gtk.TreeViewColumn("Value", wind_value_text, text=1)
        self.info_wind_tree.append_column(wind_value_col)
        wind_box.pack_start(self.info_wind_tree, fill=True, expand=True, padding=0)
        wind_win = Gtk.ScrolledWindow()
        wind_win.set_hexpand(True)
        wind_win.set_vexpand(True)
        wind_win.add(wind_box)

        # Tab 6: Humidity info.
        humi_box = Gtk.Box()
        humi_box_lbl = Gtk.Label("Humidity")
        self.info_humi_list = Gtk.ListStore(str, str)
        self.info_humi_tree = Gtk.TreeView(model=self.info_humi_list)
        humi_cate_text = Gtk.CellRendererText()
        humi_cate_col = Gtk.TreeViewColumn("Field", humi_cate_text, text=0)
        humi_cate_col.set_min_width(400)
        self.info_humi_tree.append_column(humi_cate_col)
        humi_value_text = Gtk.CellRendererText()
        humi_value_col = Gtk.TreeViewColumn("Value", humi_value_text, text=1)
        self.info_humi_tree.append_column(humi_value_col)
        humi_box.pack_start(self.info_humi_tree, fill=True, expand=True, padding=0)
        humi_win = Gtk.ScrolledWindow()
        humi_win.set_hexpand(True)
        humi_win.set_vexpand(True)
        humi_win.add(humi_box)

        # Tab 7: Air Pressure info.
        airp_box = Gtk.Box()
        airp_box_lbl = Gtk.Label("Air Pressure")
        self.info_airp_list = Gtk.ListStore(str, str)
        self.info_airp_tree = Gtk.TreeView(model=self.info_airp_list)
        airp_cate_text = Gtk.CellRendererText()
        airp_cate_col = Gtk.TreeViewColumn("Field", airp_cate_text, text=0)
        airp_cate_col.set_min_width(400)
        self.info_airp_tree.append_column(airp_cate_col)
        airp_value_text = Gtk.CellRendererText()
        airp_value_col = Gtk.TreeViewColumn("Value", airp_value_text, text=1)
        self.info_airp_tree.append_column(airp_value_col)
        airp_box.pack_start(self.info_airp_tree, fill=True, expand=True, padding=0)
        airp_win = Gtk.ScrolledWindow()
        airp_win.set_hexpand(True)
        airp_win.set_vexpand(True)
        airp_win.add(airp_box)

        # Tab 8: Visibility info.
        visi_box = Gtk.Box()
        visi_box_lbl = Gtk.Label("Visibility")
        self.info_visi_list = Gtk.ListStore(str, str)
        self.info_visi_tree = Gtk.TreeView(model=self.info_visi_list)
        visi_cate_text = Gtk.CellRendererText()
        visi_cate_col = Gtk.TreeViewColumn("Field", visi_cate_text, text=0)
        visi_cate_col.set_min_width(400)
        self.info_visi_tree.append_column(visi_cate_col)
        visi_value_text = Gtk.CellRendererText()
        visi_value_col = Gtk.TreeViewColumn("Value", visi_value_text, text=1)
        self.info_visi_tree.append_column(visi_value_col)
        visi_box.pack_start(self.info_visi_tree, fill=True, expand=True, padding=0)
        visi_win = Gtk.ScrolledWindow()
        visi_win.set_hexpand(True)
        visi_win.set_vexpand(True)
        visi_win.add(visi_box)

        # Tab 9: Cloud Cover info.
        clou_box = Gtk.Box()
        clou_box_lbl = Gtk.Label("Cloud Cover")
        self.info_clou_list = Gtk.ListStore(str, str)
        self.info_clou_tree = Gtk.TreeView(model=self.info_clou_list)
        clou_cate_text = Gtk.CellRendererText()
        clou_cate_col = Gtk.TreeViewColumn("Field", clou_cate_text, text=0)
        clou_cate_col.set_min_width(400)
        self.info_clou_tree.append_column(clou_cate_col)
        clou_value_text = Gtk.CellRendererText()
        clou_value_col = Gtk.TreeViewColumn("Value", clou_value_text, text=1)
        self.info_clou_tree.append_column(clou_value_col)
        clou_box.pack_start(self.info_clou_tree, fill=True, expand=True, padding=0)
        clou_win = Gtk.ScrolledWindow()
        clou_win.set_hexpand(True)
        clou_win.set_vexpand(True)
        clou_win.add(clou_box)

        # Tab 10: Notes info.
        note_box = Gtk.Box()
        note_box_lbl = Gtk.Label("Notes")
        self.info_note_list = Gtk.ListStore(str, str)
        self.info_note_tree = Gtk.TreeView(model=self.info_note_list)
        note_cate_text = Gtk.CellRendererText()
        note_cate_col = Gtk.TreeViewColumn("Field", note_cate_text, text=0)
        note_cate_col.set_min_width(400)
        self.info_note_tree.append_column(note_cate_col)
        note_value_text = Gtk.CellRendererText()
        note_value_col = Gtk.TreeViewColumn("Value", note_value_text, text=1)
        self.info_note_tree.append_column(note_value_col)
        note_box.pack_start(self.info_note_tree, fill=True, expand=True, padding=0)
        note_win = Gtk.ScrolledWindow()
        note_win.set_hexpand(True)
        note_win.set_vexpand(True)
        note_win.add(note_box)

        # Add the tabs to the notebook.
        info_notebook.append_page(gen_win, gen_box_lbl)
        info_notebook.append_page(temp_win, temp_box_lbl)
        info_notebook.append_page(chil_win, chil_box_lbl)
        info_notebook.append_page(prec_win, prec_box_lbl)
        info_notebook.append_page(wind_win, wind_box_lbl)
        info_notebook.append_page(humi_win, humi_box_lbl)
        info_notebook.append_page(airp_win, airp_box_lbl)
        info_notebook.append_page(visi_win, visi_box_lbl)
        info_notebook.append_page(clou_win, clou_box_lbl)
        info_notebook.append_page(note_win, note_box_lbl)

    def build_tables(self):
        """Builds the table display."""

        # Create the tab notebook.
        table_notebook = Gtk.Notebook()
        table_notebook.set_tab_pos(Gtk.PositionType.LEFT)

        # Tab 1: Temperature table.
        temp_box = Gtk.Box()
        temp_box.set_hexpand(True)
        temp_box.set_vexpand(True)
        temp_box_lbl = Gtk.Label("Temperature")
        self.table_temp_list = Gtk.ListStore(str, str, str, str, str, str)
        self.table_temp_tree = Gtk.TreeView(model=self.table_temp_list)
        temp_day_text = Gtk.CellRendererText()
        temp_day_col = Gtk.TreeViewColumn("Day", temp_day_text, text=0)
        temp_day_col.set_min_width(150)
        temp_day_col.set_expand(True)
        self.table_temp_tree.append_column(temp_day_col)
        temp_value_text = Gtk.CellRendererText()
        temp_value_col = Gtk.TreeViewColumn("Value", temp_value_text, text=1)
        temp_value_col.set_min_width(100)
        temp_value_col.set_expand(True)
        self.table_temp_tree.append_column(temp_value_col)
        temp_avg_text = Gtk.CellRendererText()
        temp_avg_col = Gtk.TreeViewColumn("Average Difference", temp_avg_text, text=2)
        temp_avg_col.set_expand(True)
        self.table_temp_tree.append_column(temp_avg_col)
        temp_low_text = Gtk.CellRendererText()
        temp_low_col = Gtk.TreeViewColumn("Low Difference", temp_low_text, text=3)
        temp_low_col.set_expand(True)
        self.table_temp_tree.append_column(temp_low_col)
        temp_high_text = Gtk.CellRendererText()
        temp_high_col = Gtk.TreeViewColumn("High Difference", temp_high_text, text=4)
        temp_high_col.set_expand(True)
        self.table_temp_tree.append_column(temp_high_col)
        temp_med_text = Gtk.CellRendererText()
        temp_med_col = Gtk.TreeViewColumn("Median Difference", temp_med_text, text=5)
        temp_med_col.set_expand(True)
        self.table_temp_tree.append_column(temp_med_col)
        temp_box.pack_start(self.table_temp_tree, fill=True, expand=True, padding=0)

        # Tab 2: Wind Chill table.
        chil_box = Gtk.Box()
        chil_box_lbl = Gtk.Label("Wind Chill")
        self.table_chil_list = Gtk.ListStore(str, str, str, str, str, str)
        self.table_chil_tree = Gtk.TreeView(model=self.table_chil_list)
        chil_day_text = Gtk.CellRendererText()
        chil_day_col = Gtk.TreeViewColumn("Day", chil_day_text, text=0)
        chil_day_col.set_min_width(150)
        chil_day_col.set_expand(True)
        self.table_chil_tree.append_column(chil_day_col)
        chil_value_text = Gtk.CellRendererText()
        chil_value_col = Gtk.TreeViewColumn("Value", chil_value_text, text=1)
        chil_value_col.set_min_width(100)
        chil_value_col.set_expand(True)
        self.table_chil_tree.append_column(chil_value_col)
        chil_avg_text = Gtk.CellRendererText()
        chil_avg_col = Gtk.TreeViewColumn("Average Difference", chil_avg_text, text=2)
        chil_avg_col.set_expand(True)
        self.table_chil_tree.append_column(chil_avg_col)
        chil_low_text = Gtk.CellRendererText()
        chil_low_col = Gtk.TreeViewColumn("Low Difference", chil_low_text, text=3)
        chil_low_col.set_expand(True)
        self.table_chil_tree.append_column(chil_low_col)
        chil_high_text = Gtk.CellRendererText()
        chil_high_col = Gtk.TreeViewColumn("High Difference", chil_high_text, text=4)
        chil_high_col.set_expand(True)
        self.table_chil_tree.append_column(chil_high_col)
        chil_med_text = Gtk.CellRendererText()
        chil_med_col = Gtk.TreeViewColumn("Median Difference", chil_med_text, text=5)
        chil_med_col.set_expand(True)
        self.table_chil_tree.append_column(chil_med_col)
        chil_box.pack_start(self.table_chil_tree, fill=True, expand=True, padding=0)

        # Tab 3: Precipitation table.
        prec_box = Gtk.Box()
        prec_box_lbl = Gtk.Label("Precipitation")
        self.table_prec_list = Gtk.ListStore(str, str, str, str, str, str)
        self.table_prec_tree = Gtk.TreeView(model=self.table_prec_list)
        prec_day_text = Gtk.CellRendererText()
        prec_day_col = Gtk.TreeViewColumn("Day", prec_day_text, text=0)
        prec_day_col.set_min_width(150)
        prec_day_col.set_expand(True)
        self.table_prec_tree.append_column(prec_day_col)
        prec_value_text = Gtk.CellRendererText()
        prec_value_col = Gtk.TreeViewColumn("Value", prec_value_text, text=1)
        prec_value_col.set_min_width(100)
        prec_value_col.set_expand(True)
        self.table_prec_tree.append_column(prec_value_col)
        prec_avg_text = Gtk.CellRendererText()
        prec_avg_col = Gtk.TreeViewColumn("Average Difference", prec_avg_text, text=2)
        prec_avg_col.set_expand(True)
        self.table_prec_tree.append_column(prec_avg_col)
        prec_low_text = Gtk.CellRendererText()
        prec_low_col = Gtk.TreeViewColumn("Low Difference", prec_low_text, text=3)
        prec_low_col.set_expand(True)
        self.table_prec_tree.append_column(prec_low_col)
        prec_high_text = Gtk.CellRendererText()
        prec_high_col = Gtk.TreeViewColumn("High Difference", prec_high_text, text=4)
        prec_high_col.set_expand(True)
        self.table_prec_tree.append_column(prec_high_col)
        prec_med_text = Gtk.CellRendererText()
        prec_med_col = Gtk.TreeViewColumn("Median Difference", prec_med_text, text=5)
        prec_med_col.set_expand(True)
        self.table_prec_tree.append_column(prec_med_col)
        prec_box.pack_start(self.table_prec_tree, fill=True, expand=True, padding=0)

        # Tab 4: Wind table.
        wind_box = Gtk.Box()
        wind_box_lbl = Gtk.Label("Wind")
        self.table_wind_list = Gtk.ListStore(str, str, str, str, str, str)
        self.table_wind_tree = Gtk.TreeView(model=self.table_wind_list)
        wind_day_text = Gtk.CellRendererText()
        wind_day_col = Gtk.TreeViewColumn("Day", wind_day_text, text=0)
        wind_day_col.set_min_width(150)
        wind_day_col.set_expand(True)
        self.table_wind_tree.append_column(wind_day_col)
        wind_value_text = Gtk.CellRendererText()
        wind_value_col = Gtk.TreeViewColumn("Value", wind_value_text, text=1)
        wind_value_col.set_min_width(100)
        wind_value_col.set_expand(True)
        self.table_wind_tree.append_column(wind_value_col)
        wind_avg_text = Gtk.CellRendererText()
        wind_avg_col = Gtk.TreeViewColumn("Average Difference", wind_avg_text, text=2)
        wind_avg_col.set_expand(True)
        self.table_wind_tree.append_column(wind_avg_col)
        wind_low_text = Gtk.CellRendererText()
        wind_low_col = Gtk.TreeViewColumn("Low Difference", wind_low_text, text=3)
        wind_low_col.set_expand(True)
        self.table_wind_tree.append_column(wind_low_col)
        wind_high_text = Gtk.CellRendererText()
        wind_high_col = Gtk.TreeViewColumn("High Difference", wind_high_text, text=4)
        wind_high_col.set_expand(True)
        self.table_wind_tree.append_column(wind_high_col)
        wind_med_text = Gtk.CellRendererText()
        wind_med_col = Gtk.TreeViewColumn("Median Difference", wind_med_text, text=5)
        wind_med_col.set_expand(True)
        self.table_wind_tree.append_column(wind_med_col)
        wind_box.pack_start(self.table_wind_tree, fill=True, expand=True, padding=0)

        # Tab 5: Humidity table.
        humi_box = Gtk.Box()
        humi_box_lbl = Gtk.Label("Humidity")
        self.table_humi_list = Gtk.ListStore(str, str, str, str, str, str)
        self.table_humi_tree = Gtk.TreeView(model=self.table_humi_list)
        humi_day_text = Gtk.CellRendererText()
        humi_day_col = Gtk.TreeViewColumn("Day", humi_day_text, text=0)
        humi_day_col.set_min_width(150)
        humi_day_col.set_expand(True)
        self.table_humi_tree.append_column(humi_day_col)
        humi_value_text = Gtk.CellRendererText()
        humi_value_col = Gtk.TreeViewColumn("Value", humi_value_text, text=1)
        humi_value_col.set_min_width(100)
        humi_value_col.set_expand(True)
        self.table_humi_tree.append_column(humi_value_col)
        humi_avg_text = Gtk.CellRendererText()
        humi_avg_col = Gtk.TreeViewColumn("Average Difference", humi_avg_text, text=2)
        humi_avg_col.set_expand(True)
        self.table_humi_tree.append_column(humi_avg_col)
        humi_low_text = Gtk.CellRendererText()
        humi_low_col = Gtk.TreeViewColumn("Low Difference", humi_low_text, text=3)
        humi_low_col.set_expand(True)
        self.table_humi_tree.append_column(humi_low_col)
        humi_high_text = Gtk.CellRendererText()
        humi_high_col = Gtk.TreeViewColumn("High Difference", humi_high_text, text=4)
        humi_high_col.set_expand(True)
        self.table_humi_tree.append_column(humi_high_col)
        humi_med_text = Gtk.CellRendererText()
        humi_med_col = Gtk.TreeViewColumn("Median Difference", humi_med_text, text=5)
        humi_med_col.set_expand(True)
        self.table_humi_tree.append_column(humi_med_col)
        humi_box.pack_start(self.table_humi_tree, fill=True, expand=True, padding=0)

        # Tab 6: Air Pressure table.
        airp_box = Gtk.Box()
        airp_box_lbl = Gtk.Label("Air Pressure")
        self.table_airp_list = Gtk.ListStore(str, str, str, str, str, str)
        self.table_airp_tree = Gtk.TreeView(model=self.table_airp_list)
        airp_day_text = Gtk.CellRendererText()
        airp_day_col = Gtk.TreeViewColumn("Day", airp_day_text, text=0)
        airp_day_col.set_min_width(150)
        airp_day_col.set_expand(True)
        self.table_airp_tree.append_column(airp_day_col)
        airp_value_text = Gtk.CellRendererText()
        airp_value_col = Gtk.TreeViewColumn("Value", airp_value_text, text=1)
        airp_value_col.set_min_width(100)
        airp_value_col.set_expand(True)
        self.table_airp_tree.append_column(airp_value_col)
        airp_avg_text = Gtk.CellRendererText()
        airp_avg_col = Gtk.TreeViewColumn("Average Difference", airp_avg_text, text=2)
        airp_avg_col.set_expand(True)
        self.table_airp_tree.append_column(airp_avg_col)
        airp_low_text = Gtk.CellRendererText()
        airp_low_col = Gtk.TreeViewColumn("Low Difference", airp_low_text, text=3)
        airp_low_col.set_expand(True)
        self.table_airp_tree.append_column(airp_low_col)
        high_text5 = Gtk.CellRendererText()
        airp_high_col = Gtk.TreeViewColumn("High Difference", high_text5, text=4)
        airp_high_col.set_expand(True)
        self.table_airp_tree.append_column(airp_high_col)
        airp_med_text = Gtk.CellRendererText()
        airp_med_col = Gtk.TreeViewColumn("Median Difference", airp_med_text, text=5)
        airp_med_col.set_expand(True)
        self.table_airp_tree.append_column(airp_med_col)
        airp_box.pack_start(self.table_airp_tree, fill=True, expand=True, padding=0)

        # Tab 7: Visibility table.
        visi_box = Gtk.Box()
        visi_box_lbl = Gtk.Label("Visibility")
        self.table_visi_list = Gtk.ListStore(str, str, str, str, str, str)
        self.table_visi_tree = Gtk.TreeView(model=self.table_visi_list)
        visi_day_text = Gtk.CellRendererText()
        visi_day_col = Gtk.TreeViewColumn("Day", visi_day_text, text=0)
        visi_day_col.set_min_width(150)
        visi_day_col.set_expand(True)
        self.table_visi_tree.append_column(visi_day_col)
        visi_value_text = Gtk.CellRendererText()
        visi_value_col = Gtk.TreeViewColumn("Value", visi_value_text, text=1)
        visi_value_col.set_min_width(100)
        visi_value_col.set_expand(True)
        self.table_visi_tree.append_column(visi_value_col)
        visi_avg_text = Gtk.CellRendererText()
        visi_avg_col = Gtk.TreeViewColumn("Average Difference", visi_avg_text, text=2)
        visi_avg_col.set_expand(True)
        self.table_visi_tree.append_column(visi_avg_col)
        visi_low_text = Gtk.CellRendererText()
        visi_low_col = Gtk.TreeViewColumn("Low Difference", visi_low_text, text=3)
        visi_low_col.set_expand(True)
        self.table_visi_tree.append_column(visi_low_col)
        visi_high_text = Gtk.CellRendererText()
        visi_high_col = Gtk.TreeViewColumn("High Difference", visi_high_text, text=4)
        visi_high_col.set_expand(True)
        self.table_visi_tree.append_column(visi_high_col)
        visi_med_text = Gtk.CellRendererText()
        visi_med_col = Gtk.TreeViewColumn("Median Difference", visi_med_text, text=5)
        visi_med_col.set_expand(True)
        self.table_visi_tree.append_column(visi_med_col)
        visi_box.pack_start(self.table_visi_tree, fill=True, expand=True, padding=0)

        # Create the ScrolledWindow for displaying the lists with scrollbars.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        scrolled_win.add(table_notebook)
        self.table_notebook = scrolled_win

        # Add the tabs to the notebook.
        table_notebook.append_page(temp_box, temp_box_lbl)
        table_notebook.append_page(chil_box, chil_box_lbl)
        table_notebook.append_page(prec_box, prec_box_lbl)
        table_notebook.append_page(wind_box, wind_box_lbl)
        table_notebook.append_page(humi_box, humi_box_lbl)
        table_notebook.append_page(airp_box, airp_box_lbl)
        table_notebook.append_page(visi_box, visi_box_lbl)

    def build_graphs(self, data, config, graph_data):
        """Builds the graph display."""

        lines = graph_data["lines"]
        hatches = graph_data["hatches"]

        # Create the tab notebook.
        graph_notebook = Gtk.Notebook()
        graph_notebook.set_tab_pos(Gtk.PositionType.LEFT)
        self.graph_notebook = graph_notebook

        # Temperature graph.
        temp_box_lbl = Gtk.Label("Temperature")
        temp_figure = Figure(figsize=(12, 6))
        temp_figure.subplots_adjust(bottom=0.2)
        temp_graph = temp_figure.add_subplot(1, 1, 1)
        temp_graph.plot(data["date_ticks"], data["temp_data"], color=config["graph_color"],
                        linewidth=config["line_width"], linestyle=lines[config["line_style"]])
        temp_graph.set_title("Temperature")
        temp_graph.set_xlabel("Date")
        temp_graph.set_ylabel("Temperature")
        temp_graph.set_xticks(data["date_ticks"])
        temp_graph.set_xticklabels(data["date_labels"], rotation="vertical")
        temp_canvas = FigureCanvas(temp_figure)
        temp_win = Gtk.ScrolledWindow()
        temp_win.set_hexpand(True)
        temp_win.set_vexpand(True)
        temp_win.add(temp_canvas)

        # Wind Chill graph.
        chil_box_lbl = Gtk.Label("Wind Chill")
        chil_figure = Figure(figsize=(12, 6))
        chil_figure.subplots_adjust(bottom=0.2)
        chil_graph = chil_figure.add_subplot(1, 1, 1)
        chil_graph.plot(data["date_ticks"], data["chil_data"], color=config["graph_color"],
                        linewidth=config["line_width"], linestyle=lines[config["line_style"]])
        chil_graph.set_title("Wind Chill")
        chil_graph.set_xlabel("Date")
        chil_graph.set_ylabel("Wind Chill")
        chil_graph.set_xticks(data["date_ticks"])
        chil_graph.set_xticklabels(data["date_labels"], rotation="vertical")
        chil_canvas = FigureCanvas(chil_figure)
        chil_win = Gtk.ScrolledWindow()
        chil_win.set_hexpand(True)
        chil_win.set_vexpand(True)
        chil_win.add(chil_canvas)

        # Precipitation graph.
        prec_box_lbl = Gtk.Label("Precipitation")
        prec_figure = Figure(figsize=(12, 6))
        prec_figure.subplots_adjust(bottom=0.2)
        prec_graph = prec_figure.add_subplot(1, 1, 1)
        prec_graph.plot(data["date_ticks"], data["prec_data"], color=config["graph_color"],
                        linewidth=config["line_width"], linestyle=lines[config["line_style"]])
        prec_graph.set_title("Precipitation")
        prec_graph.set_xlabel("Date")
        prec_graph.set_ylabel("Precipitation")
        prec_graph.set_xticks(data["date_ticks"])
        prec_graph.set_xticklabels(data["date_labels"], rotation="vertical")
        prec_canvas = FigureCanvas(prec_figure)
        prec_win = Gtk.ScrolledWindow()
        prec_win.set_hexpand(True)
        prec_win.set_vexpand(True)
        prec_win.add(prec_canvas)

        # Precipitation amount bar graph
        pramt_box_lbl = Gtk.Label("Precipitation (Amount)")
        pramt_figure = Figure(figsize=(12, 6))
        pramt_figure.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        pramt_graph = pramt_figure.add_subplot(1, 1, 1)
        pramt_graph.bar([0, 1, 2, 3], data["prec_amount"], width=0.5, color=config["graph_color"],
                        hatch=hatches[config["hatch_style"]])
        pramt_graph.set_xlabel("Precipitation Type")
        pramt_graph.set_ylabel("Total Amount")
        pramt_graph.set_title("Precipitation (Amount)")
        pramt_graph.set_xticks([0.25, 1.25, 2.25, 3.25])
        pramt_graph.set_xticklabels(["Rain", "Snow", "Hail", "Sleet"])
        pramt_canvas = FigureCanvas(pramt_figure)
        pramt_win = Gtk.ScrolledWindow()
        pramt_win.set_hexpand(True)
        pramt_win.set_vexpand(True)
        pramt_win.add(pramt_canvas)

        # Precipitation days bar graph
        prday_box_lbl = Gtk.Label("Precipitation (Days)")
        prday_figure = Figure(figsize=(12, 6))
        prday_figure.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        prday_graph = prday_figure.add_subplot(1, 1, 1)
        prday_graph.bar([0, 1, 2, 3, 4], data["prec_days"], width=0.5, color=config["graph_color"],
                        hatch=hatches[config["hatch_style"]])
        prday_graph.set_xlabel("Precipitation Type")
        prday_graph.set_ylabel("Number of Days")
        prday_graph.set_title("Precipitation (Days)")
        prday_graph.set_xticks([0.25, 1.25, 2.25, 3.25, 4.25])
        prday_graph.set_xticklabels(["None", "Rain", "Snow", "Hail", "Sleet"])
        prday_canvas = FigureCanvas(prday_figure)
        prday_win = Gtk.ScrolledWindow()
        prday_win.set_hexpand(True)
        prday_win.set_vexpand(True)
        prday_win.add(prday_canvas)

        # Wind Speed graph.
        wind_box_lbl = Gtk.Label("Wind Speed")
        wind_figure = Figure(figsize=(12, 6))
        wind_figure.subplots_adjust(bottom=0.2)
        wind_graph = wind_figure.add_subplot(1, 1, 1)
        wind_graph.plot(data["date_ticks"], data["wind_data"], color=config["graph_color"],
                        linewidth=config["line_width"], linestyle=lines[config["line_style"]])
        wind_graph.set_title("Wind Speed")
        wind_graph.set_xlabel("Date")
        wind_graph.set_ylabel("Wind Speed")
        wind_graph.set_xticks(data["date_ticks"])
        wind_graph.set_xticklabels(data["date_labels"], rotation="vertical")
        wind_canvas = FigureCanvas(wind_figure)
        wind_win = Gtk.ScrolledWindow()
        wind_win.set_hexpand(True)
        wind_win.set_vexpand(True)
        wind_win.add(wind_canvas)

        # Humidity graph.
        humi_box_lbl = Gtk.Label("Humidity")
        humi_figure = Figure(figsize=(12, 6))
        humi_figure.subplots_adjust(bottom=0.2)
        humi_graph = humi_figure.add_subplot(1, 1, 1)
        humi_graph.plot(data["date_ticks"], data["humi_data"], color=config["graph_color"],
                        linewidth=config["line_width"], linestyle=lines[config["line_style"]])
        humi_graph.set_title("Humidity")
        humi_graph.set_xlabel("Date")
        humi_graph.set_ylabel("Humidity")
        humi_graph.set_xticks(data["date_ticks"])
        humi_graph.set_xticklabels(data["date_labels"], rotation="vertical")
        humi_canvas = FigureCanvas(humi_figure)
        humi_win = Gtk.ScrolledWindow()
        humi_win.set_hexpand(True)
        humi_win.set_vexpand(True)
        humi_win.add(humi_canvas)

        # Air Pressure graph.
        airp_box_lbl = Gtk.Label("Air Pressure")
        airp_figure = Figure(figsize=(12, 6))
        airp_figure.subplots_adjust(bottom=0.2)
        airp_graph = airp_figure.add_subplot(1, 1, 1)
        airp_graph.plot(data["date_ticks"], data["airp_data"], color=config["graph_color"],
                        linewidth=config["line_width"], linestyle=lines[config["line_style"]])
        airp_graph.set_title("Air Pressure")
        airp_graph.set_xlabel("Date")
        airp_graph.set_ylabel("Air Pressure")
        airp_graph.set_xticks(data["date_ticks"])
        airp_graph.set_xticklabels(data["date_labels"], rotation="vertical")
        airp_canvas = FigureCanvas(airp_figure)
        airp_win = Gtk.ScrolledWindow()
        airp_win.set_hexpand(True)
        airp_win.set_vexpand(True)
        airp_win.add(airp_canvas)

        # Air Pressure change bar graph
        airc_box_lbl = Gtk.Label("Air Pressure (Change)")
        airc_figure = Figure(figsize=(12, 6))
        airc_figure.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        airc_graph = airc_figure.add_subplot(1, 1, 1)
        airc_graph.bar([0, 1, 2], data["airp_change"], width=0.5, color=config["graph_color"],
                       hatch=hatches[config["hatch_style"]])
        airc_graph.set_xlabel("Air Pressure Change")
        airc_graph.set_ylabel("Number of Days")
        airc_graph.set_title("Air Pressure (Change)")
        airc_graph.set_xticks([0.25, 1.25, 2.25])
        airc_graph.set_xticklabels(["Steady", "Rising", "Falling"])
        airc_canvas = FigureCanvas(airc_figure)
        airc_win = Gtk.ScrolledWindow()
        airc_win.set_hexpand(True)
        airc_win.set_vexpand(True)
        airc_win.add(airc_canvas)

        # Visibility graph
        visi_box_lbl = Gtk.Label("Visibility")
        visi_figure = Figure(figsize=(12, 6))
        visi_figure.subplots_adjust(bottom=0.2)
        visi_graph = visi_figure.add_subplot(1, 1, 1)
        visi_graph.plot(data["date_ticks"], data["visi_data"], color=config["graph_color"],
                        linewidth=config["line_width"], linestyle=lines[config["line_style"]])
        visi_graph.set_title("Visibility")
        visi_graph.set_xlabel("Date")
        visi_graph.set_ylabel("Visibility")
        visi_graph.set_xticks(data["date_ticks"])
        visi_graph.set_xticklabels(data["date_labels"], rotation="vertical")
        visi_canvas = FigureCanvas(visi_figure)
        visi_win = Gtk.ScrolledWindow()
        visi_win.set_hexpand(True)
        visi_win.set_vexpand(True)
        visi_win.add(visi_canvas)

        # Cloud Cover bar graph
        clou_box_lbl = Gtk.Label("Cloud Cover")
        clou_figure = Figure(figsize=(12, 6))
        clou_figure.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        clou_graph = clou_figure.add_subplot(1, 1, 1)
        clou_graph.bar([0, 1, 2, 3, 4], data["clou_days"], width=0.5, color=config["graph_color"],
                       hatch=hatches[config["hatch_style"]])
        clou_graph.set_xlabel("Cloud Cover")
        clou_graph.set_ylabel("Number of Days")
        clou_graph.set_title("Cloud Cover")
        clou_graph.set_xticks([0.25, 1.25, 2.25, 3.25, 4.25])
        clou_graph.set_xticklabels(["Sunny", "Mostly Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy"])
        clou_canvas = FigureCanvas(clou_figure)
        clou_win = Gtk.ScrolledWindow()
        clou_win.set_hexpand(True)
        clou_win.set_vexpand(True)
        clou_win.add(clou_canvas)

        # Cloud Type bar graph
        ctyp_box_lbl = Gtk.Label("Cloud Type")
        ctyp_figure = Figure(figsize=(12, 6))
        ctyp_figure.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        ctyp_figure.subplots_adjust(bottom=0.25)
        ctyp_graph = ctyp_figure.add_subplot(1, 1, 1)
        ctyp_graph.bar([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], data["clou_types"], width=0.5, color=config["graph_color"],
                       hatch=hatches[config["hatch_style"]])
        ctyp_graph.set_xlabel("Cloud Type")
        ctyp_graph.set_ylabel("Number of Days")
        ctyp_graph.set_title("Cloud Type")
        ctyp_graph.set_xticks([0.25, 1.25, 2.25, 3.25, 4.25, 5.25, 6.25, 7.25, 8.25, 9.25, 10.25])
        ctyp_graph.set_xticklabels(["None", "Unknown", "Cirrus", "Cirrocumulus", "Cirrostratus", "Cumulonimbus",
                                    "Altocumulus", "Altostratus", "Stratus", "Cumulus", "Stratocumulus"],
                                   rotation="vertical")
        ctyp_canvas = FigureCanvas(ctyp_figure)
        ctyp_win = Gtk.ScrolledWindow()
        ctyp_win.set_hexpand(True)
        ctyp_win.set_vexpand(True)
        ctyp_win.add(ctyp_canvas)

        # Add the tabs to the notebook.
        graph_notebook.append_page(temp_win, temp_box_lbl)
        graph_notebook.append_page(chil_win, chil_box_lbl)
        graph_notebook.append_page(prec_win, prec_box_lbl)
        graph_notebook.append_page(pramt_win, pramt_box_lbl)
        graph_notebook.append_page(prday_win, prday_box_lbl)
        graph_notebook.append_page(wind_win, wind_box_lbl)
        graph_notebook.append_page(humi_win, humi_box_lbl)
        graph_notebook.append_page(airp_win, airp_box_lbl)
        graph_notebook.append_page(airc_win, airc_box_lbl)
        graph_notebook.append_page(visi_win, visi_box_lbl)
        graph_notebook.append_page(clou_win, clou_box_lbl)
        graph_notebook.append_page(ctyp_win, ctyp_box_lbl)
