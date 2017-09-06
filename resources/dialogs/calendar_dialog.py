# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/calendar_dialog.py
# This dialog enters a date using calendars.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk


class CalendarDialog(Gtk.Dialog):
    """Shows the calendar dialog."""

    def __init__(self, parent, title, label, day=None, month=None, year=None):
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
        if day is not None:
            self.info_cal.select_month(month, year)
            self.info_cal.select_day(day)

        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()

        # Show the dialog.
        self.show_all()
