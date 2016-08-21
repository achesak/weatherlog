# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/dataset_add_select_dialog.py
# This dialog creates or selects datasets.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk

# Import application modules.
from weatherlog_resources.constants import *


class DatasetAddSelectionDialog(Gtk.Dialog):
    """Shows the dataset creation/selection dialog."""
    
    def __init__(self, parent, title, datasets):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(500, 300)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Create Dataset", DialogResponse.USE_NEW)
        self.add_button("Use Selected Dataset", DialogResponse.USE_SELECTED)
        
        # Set up the main grid.
        dat_grid = Gtk.Grid()
        self.get_content_area().add(dat_grid)
        
        # Create the creation frame.
        add_frame = Gtk.Frame()
        add_frame.set_label("Create new dataset: ")
        dat_grid.add(add_frame)
        
        # Create the creation entry.
        self.add_ent = Gtk.Entry()
        add_frame.add(self.add_ent)
        
        # Create the selection frame.
        sel_frame = Gtk.Frame()
        sel_frame.set_label("Select existing dataset: ")
        dat_grid.attach_next_to(sel_frame, add_frame, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Create the Dataset, Creation Date, and Last Modified Date columns.
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
        
        # Add the datasets.
        for i in datasets:
            self.liststore.append(i)
        
        # Display the UI.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        scrolled_win.add(self.treeview)
        sel_frame.add(scrolled_win)
        
        # Connect 'Enter' key to the OK button.
        self.add_ent.set_activates_default(True)
        ok_btn = self.get_widget_for_response(response_id = DialogResponse.USE_SELECTED)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
