# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: ui/graph_builder.py
# This module implements the function for building the Graphs tab.
#
################################################################################


# Import Gtk and Gdk for the interface.
from gi.repository import Gtk

# Import matplotlib for graphing.
try:
    from matplotlib.figure import Figure
    from matplotlib.dates import date2num
    from matplotlib.ticker import MaxNLocator
    from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
except ImportError:
    Figure = None
    date2num = None
    MaxNLocator = None
    FigureCanvas = None


def graph_builder(self):
    """Builds the Graphs tab on the main interface."""

    # Create the graph frame.
    self.graph_frame = Gtk.Box()
    self.graph_notebook = Gtk.Notebook()
    self.graph_notebook.set_tab_pos(Gtk.PositionType.LEFT)
    self.graph_frame.add(self.graph_notebook)

    # Temperature graph.
    self.graph_temp_box = Gtk.Box()
    self.graph_temp_box_lbl = Gtk.Label("Temperature")
    self.graph_temp_figure = Figure(figsize=(12, 6))
    self.graph_temp_figure.subplots_adjust(bottom=0.2)
    self.graph_temp_graph = self.graph_temp_figure.add_subplot(1, 1, 1)
    self.graph_temp_graph.set_title("Temperature")
    self.graph_temp_graph.set_xlabel("Date")
    self.graph_temp_graph.set_ylabel("Temperature")
    self.graph_temp_canvas = FigureCanvas(self.graph_temp_figure)
    self.graph_temp_win = Gtk.ScrolledWindow()
    self.graph_temp_win.set_hexpand(True)
    self.graph_temp_win.set_vexpand(True)
    self.graph_temp_win.add(self.graph_temp_canvas)

    # Wind Chill graph.
    self.graph_chil_box = Gtk.Box()
    self.graph_chil_box_lbl = Gtk.Label("Wind Chill")
    self.graph_chil_figure = Figure(figsize=(12, 6))
    self.graph_chil_figure.subplots_adjust(bottom=0.2)
    self.graph_chil_graph = self.graph_chil_figure.add_subplot(1, 1, 1)
    self.graph_chil_graph.set_title("Wind Chill")
    self.graph_chil_graph.set_xlabel("Date")
    self.graph_chil_graph.set_ylabel("Wind Chill")
    self.graph_chil_canvas = FigureCanvas(self.graph_chil_figure)
    self.graph_chil_win = Gtk.ScrolledWindow()
    self.graph_chil_win.set_hexpand(True)
    self.graph_chil_win.set_vexpand(True)
    self.graph_chil_win.add(self.graph_chil_canvas)

    # Precipitation graph.
    self.graph_prec_box = Gtk.Box()
    self.graph_prec_box_lbl = Gtk.Label("Precipitation")
    self.graph_prec_figure = Figure(figsize=(12, 6))
    self.graph_prec_figure.subplots_adjust(bottom=0.2)
    self.graph_prec_graph = self.graph_prec_figure.add_subplot(1, 1, 1)
    self.graph_prec_graph.set_title("Precipitation")
    self.graph_prec_graph.set_xlabel("Date")
    self.graph_prec_graph.set_ylabel("Precipitation")
    self.graph_prec_canvas = FigureCanvas(self.graph_prec_figure)
    self.graph_prec_win = Gtk.ScrolledWindow()
    self.graph_prec_win.set_hexpand(True)
    self.graph_prec_win.set_vexpand(True)
    self.graph_prec_win.add(self.graph_prec_canvas)

    # Precipitation amount bar graph
    self.graph_pramt_box = Gtk.Box()
    self.graph_pramt_box_lbl = Gtk.Label("Precipitation (Amount)")
    self.graph_pramt_figure = Figure(figsize=(12, 6))
    self.graph_pramt_figure.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    self.graph_pramt_graph = self.graph_pramt_figure.add_subplot(1, 1, 1)
    self.graph_pramt_graph.set_xlabel("Precipitation Type")
    self.graph_pramt_graph.set_ylabel("Total Amount")
    self.graph_pramt_graph.set_title("Precipitation (Amount)")
    self.graph_pramt_graph.set_xticks([0.25, 1.25, 2.25, 3.25])
    self.graph_pramt_graph.set_xticklabels(["Rain", "Snow", "Hail", "Sleet"])
    self.graph_pramt_canvas = FigureCanvas(self.graph_pramt_figure)
    self.graph_pramt_win = Gtk.ScrolledWindow()
    self.graph_pramt_win.set_hexpand(True)
    self.graph_pramt_win.set_vexpand(True)
    self.graph_pramt_win.add(self.graph_pramt_canvas)

    # Precipitation days bar graph
    self.graph_prday_box = Gtk.Box()
    self.graph_prday_box_lbl = Gtk.Label("Precipitation (Days)")
    self.graph_prday_figure = Figure(figsize=(12, 6))
    self.graph_prday_figure.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    self.graph_prday_graph = self.graph_prday_figure.add_subplot(1, 1, 1)
    self.graph_prday_graph.set_xlabel("Precipitation Type")
    self.graph_prday_graph.set_ylabel("Number of Days")
    self.graph_prday_graph.set_title("Precipitation (Days)")
    self.graph_prday_graph.set_xticks([0.25, 1.25, 2.25, 3.25, 4.25])
    self.graph_prday_graph.set_xticklabels(["None", "Rain", "Snow", "Hail", "Sleet"])
    self.graph_prday_canvas = FigureCanvas(self.graph_prday_figure)
    self.graph_prday_win = Gtk.ScrolledWindow()
    self.graph_prday_win.set_hexpand(True)
    self.graph_prday_win.set_vexpand(True)
    self.graph_prday_win.add(self.graph_prday_canvas)

    # Wind Speed graph.
    self.graph_wind_box = Gtk.Box()
    self.graph_wind_box_lbl = Gtk.Label("Wind Speed")
    self.graph_wind_figure = Figure(figsize=(12, 6))
    self.graph_wind_figure.subplots_adjust(bottom=0.2)
    self.graph_wind_graph = self.graph_wind_figure.add_subplot(1, 1, 1)
    self.graph_wind_graph.set_title("Wind Speed")
    self.graph_wind_graph.set_xlabel("Date")
    self.graph_wind_graph.set_ylabel("Wind Speed")
    self.graph_wind_canvas = FigureCanvas(self.graph_wind_figure)
    self.graph_wind_win = Gtk.ScrolledWindow()
    self.graph_wind_win.set_hexpand(True)
    self.graph_wind_win.set_vexpand(True)
    self.graph_wind_win.add(self.graph_wind_canvas)

    # Humidity graph.
    self.graph_humi_box = Gtk.Box()
    self.graph_humi_box_lbl = Gtk.Label("Humidity")
    self.graph_humi_figure = Figure(figsize=(12, 6))
    self.graph_humi_figure.subplots_adjust(bottom=0.2)
    self.graph_humi_graph = self.graph_humi_figure.add_subplot(1, 1, 1)
    self.graph_humi_graph.set_title("Humidity")
    self.graph_humi_graph.set_xlabel("Date")
    self.graph_humi_graph.set_ylabel("Humidity")
    self.graph_humi_canvas = FigureCanvas(self.graph_humi_figure)
    self.graph_humi_win = Gtk.ScrolledWindow()
    self.graph_humi_win.set_hexpand(True)
    self.graph_humi_win.set_vexpand(True)
    self.graph_humi_win.add(self.graph_humi_canvas)

    # Air Pressure graph.
    self.graph_airp_box = Gtk.Box()
    self.graph_airp_box_lbl = Gtk.Label("Air Pressure")
    self.graph_airp_figure = Figure(figsize=(12, 6))
    self.graph_airp_figure.subplots_adjust(bottom=0.2)
    self.graph_airp_graph = self.graph_airp_figure.add_subplot(1, 1, 1)
    self.graph_airp_graph.set_title("Air Pressure")
    self.graph_airp_graph.set_xlabel("Date")
    self.graph_airp_graph.set_ylabel("Air Pressure")
    self.graph_airp_canvas = FigureCanvas(self.graph_airp_figure)
    self.graph_airp_win = Gtk.ScrolledWindow()
    self.graph_airp_win.set_hexpand(True)
    self.graph_airp_win.set_vexpand(True)
    self.graph_airp_win.add(self.graph_airp_canvas)

    # Air Pressure change bar graph
    self.graph_airc_box = Gtk.Box()
    self.graph_airc_box_lbl = Gtk.Label("Air Pressure (Change)")
    self.graph_airc_figure = Figure(figsize=(12, 6))
    self.graph_airc_figure.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    self.graph_airc_graph = self.graph_airc_figure.add_subplot(1, 1, 1)
    self.graph_airc_graph.set_xlabel("Air Pressure Change")
    self.graph_airc_graph.set_ylabel("Number of Days")
    self.graph_airc_graph.set_title("Air Pressure (Change)")
    self.graph_airc_graph.set_xticks([0.25, 1.25, 2.25])
    self.graph_airc_graph.set_xticklabels(["Steady", "Rising", "Falling"])
    self.graph_airc_canvas = FigureCanvas(self.graph_airc_figure)
    self.graph_airc_win = Gtk.ScrolledWindow()
    self.graph_airc_win.set_hexpand(True)
    self.graph_airc_win.set_vexpand(True)
    self.graph_airc_win.add(self.graph_airc_canvas)

    # Visibility graph
    self.graph_visi_box = Gtk.Box()
    self.graph_visi_box_lbl = Gtk.Label("Visibility")
    self.graph_visi_figure = Figure(figsize=(12, 6))
    self.graph_visi_figure.subplots_adjust(bottom=0.2)
    self.graph_visi_graph = self.graph_visi_figure.add_subplot(1, 1, 1)
    self.graph_visi_graph.set_title("Visibility")
    self.graph_visi_graph.set_xlabel("Date")
    self.graph_visi_graph.set_ylabel("Visibility")
    self.graph_visi_canvas = FigureCanvas(self.graph_visi_figure)
    self.graph_visi_win = Gtk.ScrolledWindow()
    self.graph_visi_win.set_hexpand(True)
    self.graph_visi_win.set_vexpand(True)
    self.graph_visi_win.add(self.graph_visi_canvas)

    # Cloud Cover bar graph
    self.graph_clou_box = Gtk.Box()
    self.graph_clou_box_lbl = Gtk.Label("Cloud Cover")
    self.graph_clou_figure = Figure(figsize=(12, 6))
    self.graph_clou_figure.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    self.graph_clou_graph = self.graph_clou_figure.add_subplot(1, 1, 1)
    self.graph_clou_graph.set_xlabel("Cloud Cover")
    self.graph_clou_graph.set_ylabel("Number of Days")
    self.graph_clou_graph.set_title("Cloud Cover")
    self.graph_clou_graph.set_xticks([0.25, 1.25, 2.25, 3.25, 4.25])
    self.graph_clou_graph.set_xticklabels(["Sunny", "Mostly Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy"])
    self.graph_clou_canvas = FigureCanvas(self.graph_clou_figure)
    self.graph_clou_win = Gtk.ScrolledWindow()
    self.graph_clou_win.set_hexpand(True)
    self.graph_clou_win.set_vexpand(True)
    self.graph_clou_win.add(self.graph_clou_canvas)

    # Cloud Type bar graph
    self.graph_ctyp_box = Gtk.Box()
    self.graph_ctyp_box_lbl = Gtk.Label("Cloud Type")
    self.graph_ctyp_figure = Figure(figsize=(12, 6))
    self.graph_ctyp_figure.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    self.graph_ctyp_figure.subplots_adjust(bottom=0.25)
    self.graph_ctyp_graph = self.graph_ctyp_figure.add_subplot(1, 1, 1)
    self.graph_ctyp_graph.set_xlabel("Cloud Type")
    self.graph_ctyp_graph.set_ylabel("Number of Days")
    self.graph_ctyp_graph.set_title("Cloud Type")
    self.graph_ctyp_graph.set_xticks([0.25, 1.25, 2.25, 3.25, 4.25, 5.25, 6.25, 7.25, 8.25, 9.25, 10.25])
    self.graph_ctyp_graph.set_xticklabels(["None", "Unknown", "Cirrus", "Cirrocumulus", "Cirrostratus", "Cumulonimbus",
                                           "Altocumulus", "Altostratus", "Stratus", "Cumulus", "Stratocumulus"],
                                          rotation="vertical")
    self.graph_ctyp_canvas = FigureCanvas(self.graph_ctyp_figure)
    self.graph_ctyp_win = Gtk.ScrolledWindow()
    self.graph_ctyp_win.set_hexpand(True)
    self.graph_ctyp_win.set_vexpand(True)
    self.graph_ctyp_win.add(self.graph_ctyp_canvas)

    # Add the tabs.
    self.graph_notebook.append_page(self.graph_temp_win, self.graph_temp_box_lbl)
    self.graph_notebook.append_page(self.graph_chil_win, self.graph_chil_box_lbl)
    self.graph_notebook.append_page(self.graph_prec_win, self.graph_prec_box_lbl)
    self.graph_notebook.append_page(self.graph_pramt_win, self.graph_pramt_box_lbl)
    self.graph_notebook.append_page(self.graph_prday_win, self.graph_prday_box_lbl)
    self.graph_notebook.append_page(self.graph_wind_win, self.graph_wind_box_lbl)
    self.graph_notebook.append_page(self.graph_humi_win, self.graph_humi_box_lbl)
    self.graph_notebook.append_page(self.graph_airp_win, self.graph_airp_box_lbl)
    self.graph_notebook.append_page(self.graph_airc_win, self.graph_airc_box_lbl)
    self.graph_notebook.append_page(self.graph_visi_win, self.graph_visi_box_lbl)
    self.graph_notebook.append_page(self.graph_clou_win, self.graph_clou_box_lbl)
    self.graph_notebook.append_page(self.graph_ctyp_win, self.graph_ctyp_box_lbl)
