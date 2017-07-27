# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/date_selection_dialog.py
# This dialog selects dates from a list.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk


class DateSelectionDialog(Gtk.Dialog):
    """Shows the date selection dialog."""
    
    def __init__(self, parent, title, dates, buttons = [["Cancel", Gtk.ResponseType.CANCEL], ["OK", Gtk.ResponseType.OK]], default_button = Gtk.ResponseType.OK, show_conflicts = False, multi_select = True):
        """Create the dialog."""
        
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        for i in buttons:
            self.add_button(i[0], i[1])
        
        # Create the frame.
        sel_frame = Gtk.Frame()
        sel_frame.set_label("Select date%s:" % ("s" if multi_select else ""))
        self.get_content_area().add(sel_frame)
        
        # Create the Date selection.
        if show_conflicts:
            self.liststore = Gtk.ListStore(str, str)
        else:
            self.liststore = Gtk.ListStore(str)
        self.treeview = Gtk.TreeView(model = self.liststore)
        if multi_select:
            self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        date_text = Gtk.CellRendererText()
        self.date_col = Gtk.TreeViewColumn("Date", date_text, text = 0)
        self.treeview.append_column(self.date_col)
        
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
            self.liststore.append(i)
        
        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id = default_button)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
