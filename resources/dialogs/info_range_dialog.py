# -*- coding: utf-8 -*-


# This file defines the Info Range dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class InfoRangeDialog(Gtk.Dialog):
    """Shows the "Add New" dialog."""
    def __init__(self, parent, profile, info, which, day, month, year):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "%s Info in Range - %s" % (info, profile), parent, Gtk.DialogFlags.MODAL)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        info_box = self.get_content_area()
        info_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        info_box.add(info_grid)
        
        # Create the label.
        info_lbl = Gtk.Label("Select the %s date:" % which)
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
