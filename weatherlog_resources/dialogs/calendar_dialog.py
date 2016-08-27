# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/calendar_dialog.py
# This dialog enters a date or a range of dates using calendars.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk


class CalendarDialog(Gtk.Dialog):
    """Shows the calendar dialog."""
    
    def __init__(self, parent, title, label, day = None, month = None, year = None):
        """Create the dialog."""
        
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid and widgets.
        info_box = self.get_content_area()
        info_grid = Gtk.Grid()
        info_box.add(info_grid)
        info_lbl = Gtk.Label(label)
        info_lbl.set_alignment(0, 0.5)
        info_grid.add(info_lbl)
        self.info_cal = Gtk.Calendar()
        info_grid.attach_next_to(self.info_cal, info_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Set the default date.
        if day != None:
            self.info_cal.select_month(month, year)
            self.info_cal.select_day(day)
        
        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id = Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()


class CalendarRangeDialog(Gtk.Dialog):
    """Shows the calendar dialog for selection of a range of dates."""
    
    def __init__(self, parent, title, day_start = [], day_end = []):
        """Create the dialog."""
        
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid and frames.
        cal_box = self.get_content_area()
        cal_grid = Gtk.Grid()
        cal_grid.set_column_spacing(5)
        cal_box.add(cal_grid)
        cal_start_frame = Gtk.Frame()
        cal_start_frame.set_label("Starting date")
        cal_end_frame = Gtk.Frame()
        cal_end_frame.set_label("Ending date")
        cal_grid.add(cal_start_frame)
        cal_grid.attach_next_to(cal_end_frame, cal_start_frame, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the calendars.
        self.start_cal = Gtk.Calendar()
        self.end_cal = Gtk.Calendar()
        cal_start_frame.add(self.start_cal)
        cal_end_frame.add(self.end_cal)
        
        # Set the default dates.
        if len(day_start) != 0:
            self.start_cal.select_month(day_start[1], day_start[2])
            self.start_cal.select_day(day_start[0])
        if len(day_end) != 0:
            self.end_cal.select_month(day_end[1], day_end[2])
            self.end_cal.select_day(day_end[0])
        
        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id = Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
