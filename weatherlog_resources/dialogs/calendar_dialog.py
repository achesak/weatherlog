# -*- coding: utf-8 -*-


# This file defines the generic calendar dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class CalendarDialog(Gtk.Dialog):
    """Shows the calendar dialog."""
    def __init__(self, parent, title, label, day, month, year):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        info_box = self.get_content_area()
        info_grid = Gtk.Grid()
        info_box.add(info_grid)
        
        # Create the label.
        info_lbl = Gtk.Label(label)
        info_lbl.set_alignment(0, 0.5)
        info_grid.add(info_lbl)
        
        # Create the calendar.
        self.info_cal = Gtk.Calendar()
        info_grid.attach_next_to(self.info_cal, info_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Set the default date.
        self.info_cal.select_month(month, year)
        self.info_cal.select_day(day)
        
        # Show the dialog.
        self.show_all()
