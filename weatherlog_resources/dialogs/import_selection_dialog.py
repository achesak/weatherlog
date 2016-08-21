# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/import_selection_dialog.py
# This dialog selects which dates to import.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk

# Import application modules.
from weatherlog_resources.constants import *


class ImportSelectionDialog(Gtk.Dialog):
    """Shows the import selection dialog."""
    
    def __init__(self, parent, title, dates, show_conflicts = False):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Import All", DialogResponse.IMPORT_ALL)
        self.add_button("Import", DialogResponse.IMPORT)
        
        # Create the frame.
        sel_frame = Gtk.Frame()
        sel_frame.set_label("Select dates to import: ")
        self.get_content_area().add(sel_frame)
        
        # Create the Date selection.
        if show_conflicts:
            self.liststore = Gtk.ListStore(str, str)
        else:
            self.liststore = Gtk.ListStore(str)
        self.treeview = Gtk.TreeView(model = self.liststore)
        self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        pro_text = Gtk.CellRendererText()
        self.pro_col = Gtk.TreeViewColumn("Date", pro_text, text = 0)
        self.treeview.append_column(self.pro_col)
        
        # Show the Conflict column, if required.
        if show_conflicts:
            conf_text = Gtk.CellRendererText()
            self.conf_col = Gtk.TreeViewColumn("Conflict", conf_text, text = 1)
            self.treeview.append_column(self.conf_col)
        
        # Display the UI.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        scrolled_win.add(self.treeview)
        sel_frame.add(scrolled_win)
        
        # Add the dates.
        for i in dates:
            if show_conflicts:
                self.liststore.append(i)
            else:
                self.liststore.append([i])
        
        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id = DialogResponse.IMPORT)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
