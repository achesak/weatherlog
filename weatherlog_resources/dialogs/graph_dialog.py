# -*- coding: utf-8 -*-


# This file defines the graph dialog.


# Import GTK for the dialog.
from gi.repository import Gtk
# Import datetime for sorting by dates.
import datetime
# Import matplotlib for graphing.
from matplotlib.figure import Figure
from matplotlib.dates import date2num
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas


class GenericGraphDialog(Gtk.Dialog):
    """Shows the graph dialog."""
    def __init__(self, parent, title, data, last_profile):
        """Create the dialog."""
        
        data = [(datetime.datetime.strptime('5/1/2014', "%d/%m/%Y"), 23),
                (datetime.datetime.strptime('12/1/2014', "%d/%m/%Y"), 12),
                (datetime.datetime.strptime('5/2/2014', "%d/%m/%Y"), 14),
                (datetime.datetime.strptime('19/2/2014', "%d/%m/%Y"), 16),
                (datetime.datetime.strptime('5/4/2014', "%d/%m/%Y"), 13),
                (datetime.datetime.strptime('5/5/2014', "%d/%m/%Y"), 9),
                (datetime.datetime.strptime('19/5/2014', "%d/%m/%Y"), 27),
                (datetime.datetime.strptime('19/6/2014', "%d/%m/%Y"), 15),
                (datetime.datetime.strptime('5/7/2014', "%d/%m/%Y"), 16),
                (datetime.datetime.strptime('5/10/2014', "%d/%m/%Y"), 14),
                (datetime.datetime.strptime('19/10/2014', "%d/%m/%Y"), 11),
                (datetime.datetime.strptime('19/11/2014', "%d/%m/%Y"), 19)
                ]
        
        x = [date2num(date) for (date, value) in data]
        y = [value for (date, value) in data]
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(1000, 600)
        
        # Create the tab notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        info_box = self.get_content_area()
        
        # Add the buttons.
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Tab 1: Temperature graph.
        info_box1 = Gtk.Box()
        info_box1_lbl = Gtk.Label("Temperature")
        f1 = Figure(figsize = (12, 6))
        f1.subplots_adjust(bottom = 0.2)
        a1 = f1.add_subplot(1,1,1)
        a1.plot(x, y)
        a1.set_title("Temperature - %s" % last_profile)
        a1.set_xlabel("Date")
        a1.set_ylabel("Temperature")
        a1.set_xticks(x)
        a1.set_xticklabels(
                [date.strftime("%d/%m/%Y") for (date, value) in data], rotation = "vertical"
        )
        canvas1 = FigureCanvas(f1)
        scrolled_win1 = Gtk.ScrolledWindow()
        scrolled_win1.set_hexpand(True)
        scrolled_win1.set_vexpand(True)
        scrolled_win1.add(canvas1)
        
        # Tab 2: Precipitation graph.
        info_box2 = Gtk.Box()
        info_box2_lbl = Gtk.Label("Precipitation")
        f2 = Figure(figsize = (12, 6))
        f2.subplots_adjust(bottom = 0.2)
        a2 = f2.add_subplot(1,1,1)
        a2.plot(x, y)
        a2.set_title("Precipitation - %s" % last_profile)
        a2.set_xlabel("Date")
        a2.set_ylabel("Precipitation")
        a2.set_xticks(x)
        a2.set_xticklabels(
                [date.strftime("%d/%m/%Y") for (date, value) in data], rotation = "vertical"
        )
        canvas2 = FigureCanvas(f2)
        scrolled_win2 = Gtk.ScrolledWindow()
        scrolled_win2.set_hexpand(True)
        scrolled_win2.set_vexpand(True)
        scrolled_win2.add(canvas2)
        
        # Tab 3: Wind graph.
        info_box3 = Gtk.Box()
        info_box3_lbl = Gtk.Label("Wind")
        f3 = Figure(figsize = (12, 6))
        f3.subplots_adjust(bottom = 0.2)
        a3 = f3.add_subplot(1,1,1)
        a3.plot(x, y)
        a3.set_title("Wind Speed - %s" % last_profile)
        a3.set_xlabel("Date")
        a3.set_ylabel("Wind Speed")
        a3.set_xticks(x)
        a3.set_xticklabels(
                [date.strftime("%d/%m/%Y") for (date, value) in data], rotation = "vertical"
        )
        canvas3 = FigureCanvas(f3)
        scrolled_win3 = Gtk.ScrolledWindow()
        scrolled_win3.set_hexpand(True)
        scrolled_win3.set_vexpand(True)
        scrolled_win3.add(canvas3)
        
        # Tab 4: Humidity graph.
        info_box4 = Gtk.Box()
        info_box4_lbl = Gtk.Label("Humidity")
        f4 = Figure(figsize = (12, 6))
        f4.subplots_adjust(bottom = 0.2)
        a4 = f4.add_subplot(1,1,1)
        a4.plot(x, y)
        a4.set_title("Humidity - %s" % last_profile)
        a4.set_xlabel("Date")
        a4.set_ylabel("Humidity")
        a4.set_xticks(x)
        a4.set_xticklabels(
                [date.strftime("%d/%m/%Y") for (date, value) in data], rotation = "vertical"
        )
        canvas4 = FigureCanvas(f4)
        scrolled_win4 = Gtk.ScrolledWindow()
        scrolled_win4.set_hexpand(True)
        scrolled_win4.set_vexpand(True)
        scrolled_win4.add(canvas4)
        
        # Tab 5: Air Pressure graph.
        info_box5 = Gtk.Box()
        info_box5_lbl = Gtk.Label("Air Pressure")
        f5 = Figure(figsize = (12, 6))
        f5.subplots_adjust(bottom = 0.2)
        a5 = f5.add_subplot(1,1,1)
        a5.plot(x, y)
        a5.set_title("Air Pressure - %s" % last_profile)
        a5.set_xlabel("Date")
        a5.set_ylabel("Air Pressure")
        a5.set_xticks(x)
        a5.set_xticklabels(
                [date.strftime("%d/%m/%Y") for (date, value) in data], rotation = "vertical"
        )
        canvas5 = FigureCanvas(f5)
        scrolled_win5 = Gtk.ScrolledWindow()
        scrolled_win5.set_hexpand(True)
        scrolled_win5.set_vexpand(True)
        scrolled_win5.add(canvas5)
        
        # Add the tabs to the notebook.
        notebook.append_page(scrolled_win1, info_box1_lbl)
        notebook.append_page(scrolled_win2, info_box2_lbl)
        notebook.append_page(scrolled_win3, info_box3_lbl)
        notebook.append_page(scrolled_win4, info_box4_lbl)
        notebook.append_page(scrolled_win5, info_box5_lbl)
        info_box.add(notebook)
        
        # Show the dialog. There's no need to get the response.
        self.show_all()
