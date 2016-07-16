# -*- coding: utf-8 -*-


# This file defines the graph dialog.


# Import GTK for the dialog.
from gi.repository import Gtk
# Import datetime for sorting by dates.
import datetime
# Import matplotlib for graphing.
try:
    from matplotlib.figure import Figure
    from matplotlib.dates import date2num
    from matplotlib.ticker import MaxNLocator
    from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
except:
    pass


class GenericGraphDialog(Gtk.Dialog):
    """Shows the graph dialog."""
    
    def __init__(self, parent, title, data, last_profile, units, config):
        """Create the dialog."""
        
        # Dicts for getting the style from config:
        lines = {"Solid": "-", "Dashes": "--", "Dots": ":", "Dashes and dots": "-."}
        hatches = {"Solid": "", "Large upward stripes": "/", "Small upward stripes": "//", "Large downward stripes": "\\", \
                   "Small downward stripes": "\\\\", "Horizontal stripes": "-", "Crosshatch": "+", "Diagonal crosshatch": "x", \
                   "Stars": "*", "Dots": ".", "Small circles": "o", "Large circles": "O"}
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent)
        self.set_default_size(1000, 600)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the tab notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        info_box = self.get_content_area()
        
        # Temperature graph.
        temp_box = Gtk.Box()
        temp_box_lbl = Gtk.Label("Temperature")
        temp_figure = Figure(figsize = (12, 6))
        temp_figure.subplots_adjust(bottom = 0.2)
        temp_graph = temp_figure.add_subplot(1,1,1)
        temp_graph.plot(data["date_ticks"], data["temp_data"], color = config["graph_color"], linewidth = config["line_width"], linestyle = lines[config["line_style"]])
        temp_graph.set_title("Temperature - %s" % last_profile)
        temp_graph.set_xlabel("Date")
        temp_graph.set_ylabel("Temperature")
        temp_graph.set_xticks(data["date_ticks"])
        temp_graph.set_xticklabels(data["date_labels"], rotation = "vertical")
        temp_canvas = FigureCanvas(temp_figure)
        temp_win = Gtk.ScrolledWindow()
        temp_win.set_hexpand(True)
        temp_win.set_vexpand(True)
        temp_win.add(temp_canvas)
        
        # Wind Chill graph.
        chil_box = Gtk.Box()
        chil_box_lbl = Gtk.Label("Wind Chill")
        chil_figure = Figure(figsize = (12, 6))
        chil_figure.subplots_adjust(bottom = 0.2)
        chil_graph = chil_figure.add_subplot(1,1,1)
        chil_graph.plot(data["date_ticks"], data["chil_data"], color = config["graph_color"], linewidth = config["line_width"], linestyle = lines[config["line_style"]])
        chil_graph.set_title("Wind Chill - %s" % last_profile)
        chil_graph.set_xlabel("Date")
        chil_graph.set_ylabel("Wind Chill")
        chil_graph.set_xticks(data["date_ticks"])
        chil_graph.set_xticklabels(data["date_labels"], rotation = "vertical")
        chil_canvas = FigureCanvas(chil_figure)
        chil_win = Gtk.ScrolledWindow()
        chil_win.set_hexpand(True)
        chil_win.set_vexpand(True)
        chil_win.add(chil_canvas)
        
        # Precipitation graph.
        prec_box = Gtk.Box()
        prec_box_lbl = Gtk.Label("Precipitation")
        prec_figure = Figure(figsize = (12, 6))
        prec_figure.subplots_adjust(bottom = 0.2)
        prec_graph = prec_figure.add_subplot(1,1,1)
        prec_graph.plot(data["date_ticks"], data["prec_data"], color = config["graph_color"], linewidth = config["line_width"], linestyle = lines[config["line_style"]])
        prec_graph.set_title("Precipitation - %s" % last_profile)
        prec_graph.set_xlabel("Date")
        prec_graph.set_ylabel("Precipitation")
        prec_graph.set_xticks(data["date_ticks"])
        prec_graph.set_xticklabels(data["date_labels"], rotation = "vertical")
        prec_canvas = FigureCanvas(prec_figure)
        prec_win = Gtk.ScrolledWindow()
        prec_win.set_hexpand(True)
        prec_win.set_vexpand(True)
        prec_win.add(prec_canvas)
        
        # Precipitation amount bar graph
        pramt_box = Gtk.Box()
        pramt_box_lbl = Gtk.Label("Precipitation (Amount)")
        pramt_figure = Figure(figsize = (12, 6))
        pramt_figure.gca().yaxis.set_major_locator(MaxNLocator(integer = True))
        pramt_graph = pramt_figure.add_subplot(1,1,1)
        pramt_graph.bar([0, 1, 2, 3], data["prec_amount"], width = 0.5, color = config["graph_color"], hatch = hatches[config["hatch_style"]])
        pramt_graph.set_xlabel("Precipitation Type")
        pramt_graph.set_ylabel("Total Amount")
        pramt_graph.set_title("Precipitation (Amount) - %s" % last_profile)
        pramt_graph.set_xticks([0.25, 1.25, 2.25, 3.25])
        pramt_graph.set_xticklabels(["Rain", "Snow", "Hail", "Sleet"])
        pramt_canvas = FigureCanvas(pramt_figure)
        pramt_win = Gtk.ScrolledWindow()
        pramt_win.set_hexpand(True)
        pramt_win.set_vexpand(True)
        pramt_win.add(pramt_canvas)
        
        # Precipitation days bar graph
        prday_box = Gtk.Box()
        prday_box_lbl = Gtk.Label("Precipitation (Days)")
        prday_figure = Figure(figsize = (12, 6))
        prday_figure.gca().yaxis.set_major_locator(MaxNLocator(integer = True))
        prday_graph = prday_figure.add_subplot(1,1,1)
        prday_graph.bar([0, 1, 2, 3, 4], data["prec_days"], width = 0.5, color = config["graph_color"], hatch = hatches[config["hatch_style"]])
        prday_graph.set_xlabel("Precipitation Type")
        prday_graph.set_ylabel("Number of Days")
        prday_graph.set_title("Precipitation (Days) - %s" % last_profile)
        prday_graph.set_xticks([0.25, 1.25, 2.25, 3.25, 4.25])
        prday_graph.set_xticklabels(["None", "Rain", "Snow", "Hail", "Sleet"])
        prday_canvas = FigureCanvas(prday_figure)
        prday_win = Gtk.ScrolledWindow()
        prday_win.set_hexpand(True)
        prday_win.set_vexpand(True)
        prday_win.add(prday_canvas)
        
        # Wind Speed graph.
        wind_box = Gtk.Box()
        wind_box_lbl = Gtk.Label("Wind Speed")
        wind_figure = Figure(figsize = (12, 6))
        wind_figure.subplots_adjust(bottom = 0.2)
        wind_graph = wind_figure.add_subplot(1,1,1)
        wind_graph.plot(data["date_ticks"], data["wind_data"], color = config["graph_color"], linewidth = config["line_width"], linestyle = lines[config["line_style"]])
        wind_graph.set_title("Wind Speed - %s" % last_profile)
        wind_graph.set_xlabel("Date")
        wind_graph.set_ylabel("Wind Speed")
        wind_graph.set_xticks(data["date_ticks"])
        wind_graph.set_xticklabels(data["date_labels"], rotation = "vertical")
        wind_canvas = FigureCanvas(wind_figure)
        wind_win = Gtk.ScrolledWindow()
        wind_win.set_hexpand(True)
        wind_win.set_vexpand(True)
        wind_win.add(wind_canvas)
        
        # Humidity graph.
        humi_box = Gtk.Box()
        humi_box_lbl = Gtk.Label("Humidity")
        humi_figure = Figure(figsize = (12, 6))
        humi_figure.subplots_adjust(bottom = 0.2)
        humi_graph = humi_figure.add_subplot(1,1,1)
        humi_graph.plot(data["date_ticks"], data["humi_data"], color = config["graph_color"], linewidth = config["line_width"], linestyle = lines[config["line_style"]])
        humi_graph.set_title("Humidity - %s" % last_profile)
        humi_graph.set_xlabel("Date")
        humi_graph.set_ylabel("Humidity")
        humi_graph.set_xticks(data["date_ticks"])
        humi_graph.set_xticklabels(data["date_labels"], rotation = "vertical")
        humi_canvas = FigureCanvas(humi_figure)
        humi_win = Gtk.ScrolledWindow()
        humi_win.set_hexpand(True)
        humi_win.set_vexpand(True)
        humi_win.add(humi_canvas)
        
        # Air Pressure graph.
        airp_box = Gtk.Box()
        airp_box_lbl = Gtk.Label("Air Pressure")
        airp_figure = Figure(figsize = (12, 6))
        airp_figure.subplots_adjust(bottom = 0.2)
        airp_graph = airp_figure.add_subplot(1,1,1)
        airp_graph.plot(data["date_ticks"], data["airp_data"], color = config["graph_color"], linewidth = config["line_width"], linestyle = lines[config["line_style"]])
        airp_graph.set_title("Air Pressure - %s" % last_profile)
        airp_graph.set_xlabel("Date")
        airp_graph.set_ylabel("Air Pressure")
        airp_graph.set_xticks(data["date_ticks"])
        airp_graph.set_xticklabels(data["date_labels"], rotation = "vertical")
        airp_canvas = FigureCanvas(airp_figure)
        airp_win = Gtk.ScrolledWindow()
        airp_win.set_hexpand(True)
        airp_win.set_vexpand(True)
        airp_win.add(airp_canvas)
        
        # Air Pressure change bar graph
        airc_box = Gtk.Box()
        airc_box_lbl = Gtk.Label("Air Pressure (Change)")
        airc_figure = Figure(figsize = (12, 6))
        airc_figure.gca().yaxis.set_major_locator(MaxNLocator(integer = True))
        airc_graph = airc_figure.add_subplot(1,1,1)
        airc_graph.bar([0, 1, 2], data["airp_change"], width = 0.5, color = config["graph_color"], hatch = hatches[config["hatch_style"]])
        airc_graph.set_xlabel("Air Pressure Change")
        airc_graph.set_ylabel("Number of Days")
        airc_graph.set_title("Air Pressure (Change) - %s" % last_profile)
        airc_graph.set_xticks([0.25, 1.25, 2.25])
        airc_graph.set_xticklabels(["Steady", "Rising", "Falling"])
        airc_canvas = FigureCanvas(airc_figure)
        airc_win = Gtk.ScrolledWindow()
        airc_win.set_hexpand(True)
        airc_win.set_vexpand(True)
        airc_win.add(airc_canvas)
        
        # Visibility graph
        visi_box = Gtk.Box()
        visi_box_lbl = Gtk.Label("Visibility")
        visi_figure = Figure(figsize = (12, 6))
        visi_figure.subplots_adjust(bottom = 0.2)
        visi_graph = visi_figure.add_subplot(1,1,1)
        visi_graph.plot(data["date_ticks"], data["visi_data"], color = config["graph_color"], linewidth = config["line_width"], linestyle = lines[config["line_style"]])
        visi_graph.set_title("Visibility - %s" % last_profile)
        visi_graph.set_xlabel("Date")
        visi_graph.set_ylabel("Visibility")
        visi_graph.set_xticks(data["date_ticks"])
        visi_graph.set_xticklabels(data["date_labels"], rotation = "vertical")
        visi_canvas = FigureCanvas(visi_figure)
        visi_win = Gtk.ScrolledWindow()
        visi_win.set_hexpand(True)
        visi_win.set_vexpand(True)
        visi_win.add(visi_canvas)
        
        # Cloud Cover bar graph
        clou_box = Gtk.Box()
        clou_box_lbl = Gtk.Label("Cloud Cover")
        clou_figure = Figure(figsize = (12, 6))
        clou_figure.gca().yaxis.set_major_locator(MaxNLocator(integer = True))
        clou_graph = clou_figure.add_subplot(1,1,1)
        clou_graph.bar([0, 1, 2, 3, 4], data["clou_days"], width = 0.5, color = config["graph_color"], hatch = hatches[config["hatch_style"]])
        clou_graph.set_xlabel("Cloud Cover")
        clou_graph.set_ylabel("Number of Days")
        clou_graph.set_title("Cloud Cover - %s" % last_profile)
        clou_graph.set_xticks([0.25, 1.25, 2.25, 3.25, 4.25])
        clou_graph.set_xticklabels(["Sunny", "Mostly Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy"])
        clou_canvas = FigureCanvas(clou_figure)
        clou_win = Gtk.ScrolledWindow()
        clou_win.set_hexpand(True)
        clou_win.set_vexpand(True)
        clou_win.add(clou_canvas)
        
        # Cloud Type bar graph
        ctyp_box = Gtk.Box()
        ctyp_box_lbl = Gtk.Label("Cloud Type")
        ctyp_figure = Figure(figsize = (12, 6))
        ctyp_figure.gca().yaxis.set_major_locator(MaxNLocator(integer = True))
        ctyp_figure.subplots_adjust(bottom = 0.25)
        ctyp_graph = ctyp_figure.add_subplot(1,1,1)
        ctyp_graph.bar([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], data["clou_types"], width = 0.5, color = config["graph_color"], hatch = hatches[config["hatch_style"]])
        ctyp_graph.set_xlabel("Cloud Type")
        ctyp_graph.set_ylabel("Number of Days")
        ctyp_graph.set_title("Cloud Type - %s" % last_profile)
        ctyp_graph.set_xticks([0.25, 1.25, 2.25, 3.25, 4.25, 5.25, 6.25, 7.25, 8.25, 9.25, 10.25])
        ctyp_graph.set_xticklabels(["None", "Unknown", "Cirrus", "Cirrocumulus", "Cirrostratus", "Cumulonimbus",
                            "Altocumulus", "Altostratus", "Stratus", "Cumulus", "Stratocumulus"], rotation="vertical")
        ctyp_canvas = FigureCanvas(ctyp_figure)
        ctyp_win = Gtk.ScrolledWindow()
        ctyp_win.set_hexpand(True)
        ctyp_win.set_vexpand(True)
        ctyp_win.add(ctyp_canvas)
        
        # Add the tabs to the notebook.
        notebook.append_page(temp_win, temp_box_lbl)
        notebook.append_page(chil_win, chil_box_lbl)
        notebook.append_page(prec_win, prec_box_lbl)
        notebook.append_page(pramt_win, pramt_box_lbl)
        notebook.append_page(prday_win, prday_box_lbl)
        notebook.append_page(wind_win, wind_box_lbl)
        notebook.append_page(humi_win, humi_box_lbl)
        notebook.append_page(airp_win, airp_box_lbl)
        notebook.append_page(airc_win, airc_box_lbl)
        notebook.append_page(visi_win, visi_box_lbl)
        notebook.append_page(clou_win, clou_box_lbl)
        notebook.append_page(ctyp_win, ctyp_box_lbl)
        info_box.add(notebook)
        
        # Show the dialog.
        self.show_all()
