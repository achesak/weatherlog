# -*- coding: utf-8 -*-


# This file defines the function for showing the no data dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


def show_no_data_dialog(master, title):
    """Show the dialog to tell the user there is no info."""
    
    err_miss_dlg = Gtk.MessageDialog(master, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, title)
    err_miss_dlg.format_secondary_text("There is no data to display.")
    err_miss_dlg.run()
    err_miss_dlg.destroy()
