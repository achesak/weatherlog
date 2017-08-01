# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/dataset_selection_dialog.py
# This dialog selects datasets from a list.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk

# Import application modules.
from weatherlog_resources.constants import *


class DatasetSelectionDialog(Gtk.Dialog):
    """Shows the dataset selection dialog."""

    def __init__(self, parent, title, datasets, select_mode=DatasetSelectionMode.SINGLE):
        """Create the dialog."""

        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(500, 300)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)

        # Create the frame.
        sel_frame = Gtk.Frame()
        if select_mode == DatasetSelectionMode.SINGLE:
            sel_frame.set_label("Select dataset:")
        else:
            sel_frame.set_label("Select datasets:")
        self.get_content_area().add(sel_frame)

        # Create the Dataset, Creation Date, and Last Modified Date columns.
        self.liststore = Gtk.ListStore(str, str, str)
        self.treeview = Gtk.TreeView(model=self.liststore)
        pro_text = Gtk.CellRendererText()
        self.pro_col = Gtk.TreeViewColumn("Dataset", pro_text, text=0)
        self.pro_col.set_expand(True)
        self.treeview.append_column(self.pro_col)
        cre_text = Gtk.CellRendererText()
        self.cre_col = Gtk.TreeViewColumn("Creation Date", cre_text, text=1)
        self.cre_col.set_expand(True)
        self.treeview.append_column(self.cre_col)
        mod_text = Gtk.CellRendererText()
        self.mod_col = Gtk.TreeViewColumn("Last Modified Date", mod_text, text=2)
        self.mod_col.set_expand(True)
        self.treeview.append_column(self.mod_col)

        # Allow for multiple items to be selected, if appropriate.
        if select_mode == DatasetSelectionMode.MULTIPLE:
            self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)

        # Add the datasets..
        for i in datasets:
            self.liststore.append(i)

        # Display the UI.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        scrolled_win.add(self.treeview)
        sel_frame.add(scrolled_win)

        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()

        # Show the dialog.
        self.show_all()
