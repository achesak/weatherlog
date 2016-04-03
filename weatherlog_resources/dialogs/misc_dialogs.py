# -*- coding: utf-8 -*-


# This file defines functions for displaying miscellaneous dialogs.


# Import GTK for the dialog.
from gi.repository import Gtk
# Import the application constants.
from weatherlog_resources.constants import *

__all__ = ["show_alert_dialog", "show_error_dialog", "show_question_dialog", "show_file_dialog",
           "show_export_dialog", "show_save_dialog", "show_no_data_dialog", "show_import_dialog"]


def show_alert_dialog(self, title, msg, show_cancel = False):
    """Shows the alert dialog."""
    
    buttons = Gtk.ButtonsType.OK_CANCEL if show_cancel else Gtk.ButtonsType.OK
    alert_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, buttons, title)
    alert_dlg.format_secondary_text(msg)
    response = alert_dlg.run()
    alert_dlg.destroy()
    
    return response


def show_error_dialog(self, title, msg):
    """Shows the error dialog."""
    
    error_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, title)
    error_dlg.format_secondary_text(msg)
    error_dlg.run()
    error_dlg.destroy()


def show_question_dialog(self, title, msg):
    """Shows the question dialog."""
    
    over_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, title)
    over_dlg.format_secondary_text(msg)
    response = over_dlg.run()
    over_dlg.destroy()
    return response


def show_file_dialog(self, title):
    """Shows the file chooser (open) dialog."""
    
    import_dlg = Gtk.FileChooserDialog(title, self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    response = import_dlg.run()
    filename = import_dlg.get_filename()
    import_dlg.destroy()
    return [response, filename]


def show_import_dialog(self, title):
    """Shows the file chooser (open) dialog."""
    
    import_dlg = Gtk.FileChooserDialog(title, self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Import and Overwrite", DialogResponse.IMPORT_OVERWRITE, "Import", Gtk.ResponseType.OK))
    response = import_dlg.run()
    filename = import_dlg.get_filename()
    import_dlg.destroy()
    return [response, filename]


def show_export_dialog(self, title):
    """Shows the file chooser (save) dialog."""
    
    export_dlg = Gtk.FileChooserDialog(title, self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Export", Gtk.ResponseType.OK))
    export_dlg.set_do_overwrite_confirmation(True)
    response = export_dlg.run()
    filename = export_dlg.get_filename()
    export_dlg.destroy()
    return [response, filename]
    

def show_save_dialog(self, title):
    """Shows the file chooser (save) dialog."""
    
    export_dlg = Gtk.FileChooserDialog(title, self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Export to CSV", DialogResponse.EXPORT_CSV, "Export to HTML", DialogResponse.EXPORT_HTML, "Export", Gtk.ResponseType.OK))
    export_dlg.set_do_overwrite_confirmation(True)
    response = export_dlg.run()
    filename = export_dlg.get_filename()
    export_dlg.destroy()
    return [response, filename]


def show_no_data_dialog(master, title, message = "There is no data to display."):
    """Show the dialog to tell the user there is no info."""
    
    err_miss_dlg = Gtk.MessageDialog(master, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, title)
    err_miss_dlg.format_secondary_text(message)
    err_miss_dlg.run()
    err_miss_dlg.destroy()
