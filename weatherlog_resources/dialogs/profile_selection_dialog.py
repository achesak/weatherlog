# -*- coding: utf-8 -*-


# This file defines the generic dialog for selecting a profile.


# Import GTK for the dialog.
from gi.repository import Gtk


class ProfileSelectionDialog(Gtk.Dialog):
    """Shows the profile selection dialog."""
    def __init__(self, parent, title, profiles, select_mode = "single"):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        # Don't allow the user to resize the window.
        #self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        sel_box = self.get_content_area()
        sel_grid = Gtk.Grid()
        sel_box.add(sel_grid)
        
        # Create the label.
        sel_lbl = Gtk.Label("Choose profile:")
        sel_lbl.set_alignment(0, 0.5)
        sel_grid.add(sel_lbl)
        
        # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str, str)
        # Add the profiles.
        for i in profiles:
            self.liststore.append(i)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        
        # Create the Profile column.
        pro_text = Gtk.CellRendererText()
        self.pro_col = Gtk.TreeViewColumn("Profile", pro_text, text = 0)
        self.treeview.append_column(self.pro_col)
        
        # Create the Last Modified column.
        mod_text = Gtk.CellRendererText()
        self.mod_col = Gtk.TreeViewColumn("Last Modified", mod_text, text = 1)
        self.treeview.append_column(self.mod_col)
        
        # Allow for multiple items to be selected, if appropriate.
        if select_mode == "multiple":
            self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        
        # Create the ScrolledWindow for displaying the list with a scrollbar.
        scrolled_win = Gtk.ScrolledWindow()
        
        # The container should scroll vertically and horizontally.
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        
        # Display the TreeView.
        scrolled_win.add(self.treeview)
        sel_grid.attach_next_to(scrolled_win, sel_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
