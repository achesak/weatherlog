# -*- coding: utf-8 -*-


# This file defines the generic dialog for selecting a dataset.


# Import GTK for the dialog.
from gi.repository import Gtk


class DatasetSelectionDialog(Gtk.Dialog):
    """Shows the dataset selection dialog."""
    
    def __init__(self, parent, title, datasets, select_mode = "single"):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(500, 300)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        sel_box = self.get_content_area()
        sel_grid = Gtk.Grid()
        sel_box.add(sel_grid)
        
        # Create the label.
        sel_lbl = Gtk.Label("Choose dataset:")
        sel_lbl.set_alignment(0, 0.5)
        sel_grid.add(sel_lbl)
        
        # Create the Profile, Creation Date, and Last Modified Date columns.
        self.liststore = Gtk.ListStore(str, str, str)
        self.treeview = Gtk.TreeView(model = self.liststore)
        pro_text = Gtk.CellRendererText()
        self.pro_col = Gtk.TreeViewColumn("Dataset", pro_text, text = 0)
        self.treeview.append_column(self.pro_col)
        cre_text = Gtk.CellRendererText()
        self.cre_text = Gtk.TreeViewColumn("Creation Date", cre_text, text = 1)
        self.treeview.append_column(self.cre_text)
        mod_text = Gtk.CellRendererText()
        self.mod_col = Gtk.TreeViewColumn("Last Modified Date", mod_text, text = 2)
        self.treeview.append_column(self.mod_col)
        
        # Allow for multiple items to be selected, if appropriate.
        if select_mode == "multiple":
            self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        
        # Add the profiles.
        for i in datasets:
            self.liststore.append(i)
        
        # Display the UI.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        scrolled_win.add(self.treeview)
        sel_grid.attach_next_to(scrolled_win, sel_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id = Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
