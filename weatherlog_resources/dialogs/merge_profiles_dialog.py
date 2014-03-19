# -*- coding: utf-8 -*-


# This file defines the Merge Profiles dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class MergeProfilesDialog(Gtk.Dialog):
    """Shows the "Merge Profiles" dialog."""
    def __init__(self, parent, profiles):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Merge Profiles", parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        # Don't allow the user to resize the window.
        #self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        mer_box = self.get_content_area()
        mer_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        mer_box.add(mer_grid)
        
        # Create the label.
        mer_lbl = Gtk.Label("Choose profile:")
        mer_lbl.set_alignment(0, 0.5)
        mer_grid.add(mer_lbl)
        
        # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str, str)
        # Add the profiles.
        for i in profiles:
            self.liststore.append(i)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        
        # Create the Profile column.
        mer_text = Gtk.CellRendererText()
        self.mer_col = Gtk.TreeViewColumn("Profile", mer_text, text = 0)
        self.treeview.append_column(self.mer_col)
        
        # Create the Last Modified column.
        mod_text = Gtk.CellRendererText()
        self.mod_col = Gtk.TreeViewColumn("Last Modified", mod_text, text = 1)
        self.treeview.append_column(self.mod_col)
        
        # Create the ScrolledWindow for displaying the list with a scrollbar.
        scrolled_win = Gtk.ScrolledWindow()
        
        # The container should scroll vertically and horizontally.
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        
        # Display the TreeView.
        scrolled_win.add(self.treeview)
        mer_grid.attach_next_to(scrolled_win, mer_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
