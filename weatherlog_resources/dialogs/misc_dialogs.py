# -*- coding: utf-8 -*-


# This file defines functions for displaying miscellaneous dialogs.


# Import GTK for the dialog.
from gi.repository import Gtk


def show_alert_dialog(self, title, msg):
    """Shows the alert dialog."""
    
    alert_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, title)
    alert_dlg.format_secondary_text(msg)
    alert_dlg.run()
    alert_dlg.destroy()


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
    
    # Create the dialog.
    import_dlg = Gtk.FileChooserDialog(title, self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    
    # Get the response and filename then close the dialog.
    response = import_dlg.run()
    filename = import_dlg.get_filename()
    import_dlg.destroy()
    return [response, filename]
    

def show_save_dialog(self, title):
    """Shows the file chooser (save) dialog."""
    
    # Create the dialog.
    export_dlg = Gtk.FileChooserDialog(title, self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Export to CSV", 98, "Export to HTML", 99, "Export", Gtk.ResponseType.OK))
    export_dlg.set_do_overwrite_confirmation(True)
    
    # Get the response and filename then close the dialog.
    response = export_dlg.run()
    filename = export_dlg.get_filename()
    export_dlg.destroy()
    return [response, filename]
