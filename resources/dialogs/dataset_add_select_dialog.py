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
from resources.constants import *
import resources.validate as validate
import resources.io as io
from resources.dialogs.misc_dialogs import *


class DatasetAddSelectionDialog(Gtk.Dialog):
    """Shows the dataset creation/selection dialog."""

    def __init__(self, parent, title, datasets, main_dir, last_dataset):
        """Create the dialog."""

        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL, use_header_bar=True)
        self.set_default_size(500, 300)
        self.add_button("Select Dataset", DialogResponse.USE_SELECTED)

        self.main_dir = main_dir
        self.last_dataset = last_dataset

        # Create the header bar.
        header = self.get_header_bar()
        header.set_title(title)
        header.set_show_close_button(True)

        # Set up the main grid.
        dat_grid = Gtk.Grid()
        self.get_content_area().add(dat_grid)


        # Create the selection frame.
        sel_frame = Gtk.Frame()
        sel_frame.set_label("Select dataset")
        dat_grid.add(sel_frame)

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

        # Create the creation frame.
        add_frame = Gtk.Frame()
        add_frame.set_label("Create new dataset")
        dat_grid.attach_next_to(add_frame, sel_frame, Gtk.PositionType.BOTTOM, 1, 1)

        # Create the creation entry and button.
        add_box = Gtk.Box()
        self.add_ent = Gtk.Entry()
        add_frame.add(add_box)
        self.add_btn = Gtk.Button(label="Create Dataset")
        self.add_btn.set_margin_left(5)
        add_box.pack_start(self.add_ent, True, True, 0)
        add_box.pack_end(self.add_btn, False, False, 0)

        # Add the datasets.
        for i in datasets:
            self.liststore.append(i)

        # Display the UI.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        scrolled_win.add(self.treeview)
        sel_frame.add(scrolled_win)

        # Connect the events.
        self.add_btn.connect("clicked", self.create_dataset)

        # Connect 'Enter' key to the OK button.
        self.add_ent.set_activates_default(True)
        ok_btn = self.get_widget_for_response(response_id=DialogResponse.USE_SELECTED)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()

        # Show the dialog.
        self.show_all()

    def create_dataset(self, event):
        """Creates a new dataset."""

        new_name = self.add_ent.get_text()

        # Validate the name.
        valid = validate.validate_dataset(self.main_dir, new_name)
        if valid != DatasetValidation.VALID:
            show_error_dialog(self, "Copy Data", validate.validate_dataset_name_strings[valid])
            return

        # Create the directory and file.
        io.write_blank_dataset(self.main_dir, new_name)
        io.write_metadata(self.main_dir, new_name, now=True)
        io.write_dataset(main_dir=self.main_dir, name=new_name, data=[])

        # Refresh the dataset list.
        dataset_list = io.get_dataset_list(self.main_dir, self.last_dataset)
        self.liststore.clear()
        for i in dataset_list:
            self.liststore.append(i)
