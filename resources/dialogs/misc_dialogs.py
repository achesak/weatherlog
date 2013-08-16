# -*- coding: utf-8 -*-


# This file defines functions for displaying miscellaneous dialogs.


# Import GTK for the dialog.
from gi.repository import Gtk


def show_alert_dialog(self, title, msg):
    """Shows the alert dialog."""
    
    # Create the dialog.
    alert_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, title)
    alert_dlg.format_secondary_text(msg)
    
    # Run then close the dialog.
    alert_dlg.run()
    alert_dlg.destroy()


def show_error_dialog(self, title, msg):
    """Shows the error dialog."""
    
    # Create the dialog.
    error_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, title)
    error_dlg.format_secondary_text(msg)
    
    # Run then close the dialog.
    error_dlg.run()
    error_dlg.destroy()


def show_question_dialog(self, title, msg):
    """Shows the question dialog."""
    
    # Create the dialog.
    over_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, title)
    over_dlg.format_secondary_text(msg)
    
    # Get the response then close the dialog.
    response = over_dlg.run()
    over_dlg.destroy()
    
    # Return the response.
    return response
