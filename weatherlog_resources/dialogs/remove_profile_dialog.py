# -*- coding: utf-8 -*-


# This file defines the Remove Profile dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class RemoveProfileDialog(Gtk.Dialog):
    """Shows the "Remove Profile" dialog."""
    def __init__(self, parent, profiles):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Remove Profile", parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        # Don't allow the user to resize the window.
        #self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        rem_box = self.get_content_area()
        rem_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        rem_box.add(rem_grid)
        
        # Create the label.
        rem_lbl = Gtk.Label("Choose profile:")
        rem_lbl.set_alignment(0, 0.5)
        rem_grid.add(rem_lbl)
        
        # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str, str)
        # Add the profiles.
        for i in profiles:
            self.liststore.append(i)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        
        # Create the Profile column.
        rem_text = Gtk.CellRendererText()
        self.rem_col = Gtk.TreeViewColumn("Profile", rem_text, text = 0)
        self.treeview.append_column(self.rem_col)
        
        # Create the Last Modified column.
        mod_text = Gtk.CellRendererText()
        self.mod_col = Gtk.TreeViewColumn("Last Modified", mod_text, text = 1)
        self.treeview.append_column(self.mod_col)
        
        # Allow for multiple items to be selected.
        self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        
        # Create the ScrolledWindow for displaying the list with a scrollbar.
        scrolled_win = Gtk.ScrolledWindow()
        
        # The container should scroll vertically and horizontally.
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        
        # Display the TreeView.
        scrolled_win.add(self.treeview)
        rem_grid.attach_next_to(scrolled_win, rem_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
