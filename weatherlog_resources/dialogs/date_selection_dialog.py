# -*- coding: utf-8 -*-


# This file defines the dialog for selecting dates.


# Import GTK for the dialog.
from gi.repository import Gtk


class DateSelectionDialog(Gtk.Dialog):
    """Shows the date selection dialog."""
    
    def __init__(self, parent, title, dates, buttons = [["Cancel", Gtk.ResponseType.CANCEL], ["OK", Gtk.ResponseType.OK]], show_conflicts = False):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        for i in buttons:
            self.add_button(i[0], i[1])
        
        # Create the frame.
        sel_frame = Gtk.Frame()
        sel_frame.set_label("Select dates:")
        self.get_content_area().add(sel_frame)
        
        # Create the Date selection.
        self.liststore = Gtk.ListStore(str)
        self.treeview = Gtk.TreeView(model = self.liststore)
        self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        date_text = Gtk.CellRendererText()
        self.date_col = Gtk.TreeViewColumn("Date", date_text, text = 0)
        self.treeview.append_column(self.date_col)
        
        # Display the UI.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        scrolled_win.add(self.treeview)
        sel_frame.add(scrolled_win)
        
        # Add the dates.
        for i in dates:
            self.liststore.append(i)
        
        # Show the dialog.
        self.show_all()
