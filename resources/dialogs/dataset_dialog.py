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
from resources.dialogs.entry_dialog import GenericEntryDialog

# Import shutil for file management.
import shutil
import os
import datetime


class DatasetDialog(Gtk.Dialog):
    """Shows the dataset creation/selection dialog."""

    def __init__(self, parent, main_dir, last_dataset, config):
        """Create the dialog."""

        Gtk.Dialog.__init__(self, "Datasets", parent, Gtk.DialogFlags.MODAL, use_header_bar=True)
        self.set_default_size(500, 600)

        self.main_dir = main_dir
        self.last_dataset = last_dataset
        self.config = config
        self.switch_name = None

        # Create the header bar.
        header = self.get_header_bar()
        header.set_title("Datasets")

        # Set up the main grid.
        dat_grid = Gtk.Grid()
        dat_grid.set_border_width(5)
        dat_grid.set_column_spacing(5)
        dat_grid.set_row_spacing(5)
        self.get_content_area().add(dat_grid)

        # Create the creation frame.
        add_frame = Gtk.Frame()
        add_frame.set_label("Create new dataset")
        dat_grid.add(add_frame)

        # Create the creation entry and button.
        add_grid = Gtk.Grid()
        add_grid.set_border_width(5)
        add_grid.set_column_spacing(5)
        add_grid.set_row_spacing(5)
        self.add_ent = Gtk.Entry()
        self.add_ent.set_hexpand(True)
        add_frame.add(add_grid)
        self.add_btn = Gtk.Button(label="Create")
        add_grid.add(self.add_ent)
        add_grid.attach_next_to(self.add_btn, self.add_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Create the selection frame and grid.
        sel_frame = Gtk.Frame()
        sel_frame.set_label("Select dataset")
        dat_grid.attach_next_to(sel_frame, add_frame, Gtk.PositionType.BOTTOM, 1, 1)
        sel_grid = Gtk.Grid()
        sel_grid.set_border_width(5)
        sel_grid.set_column_spacing(5)
        sel_grid.set_row_spacing(5)
        sel_frame.add(sel_grid)

        # Create the Dataset, Creation Date, and Last Modified Date columns.
        self.liststore = Gtk.ListStore(str, str, str)
        self.treeview = Gtk.TreeView(model=self.liststore)
        self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        pro_text = Gtk.CellRendererText()
        self.pro_col = Gtk.TreeViewColumn("Dataset", pro_text, text=0)
        self.pro_col.set_expand(True)
        self.treeview.append_column(self.pro_col)
        cre_text = Gtk.CellRendererText()
        self.cre_col = Gtk.TreeViewColumn("Created", cre_text, text=1)
        self.cre_col.set_expand(True)
        self.treeview.append_column(self.cre_col)
        mod_text = Gtk.CellRendererText()
        self.mod_col = Gtk.TreeViewColumn("Last Modified", mod_text, text=2)
        self.mod_col.set_expand(True)
        self.treeview.append_column(self.mod_col)

        # Create the scrolling frame.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        scrolled_win.add(self.treeview)
        sel_grid.attach(scrolled_win, 0, 0, 3, 1)

        # Create the management buttons.
        rename_btn = Gtk.Button("Rename")
        sel_grid.attach(rename_btn, 0, 1, 1, 1)
        remove_btn = Gtk.Button("Remove")
        sel_grid.attach(remove_btn, 1, 1, 1, 1)
        switch_btn = Gtk.Button("Switch")
        sel_grid.attach(switch_btn, 2, 1, 1, 1)

        self.update_list()

        # Connect the events.
        self.add_btn.connect("clicked", lambda x: self.create_dataset())
        self.add_ent.connect("activate", lambda x: self.create_dataset())
        remove_btn.connect("clicked", lambda x: self.remove_datasets())
        rename_btn.connect("clicked", lambda x: self.rename_dataset())
        switch_btn.connect("clicked", lambda x: self.switch_dataset())
        self.treeview.connect("row-activated", lambda x, y, z: self.switch_dataset())

        # Show the dialog.
        self.show_all()

    def update_list(self):
        """Updates the dataset list."""

        self.liststore.clear()

        datasets = io.get_dataset_list(self.main_dir, self.last_dataset)

        # Add the datasets.
        for i in datasets:
            self.liststore.append(i)

    def create_dataset(self):
        """Creates a new dataset."""

        new_name = self.add_ent.get_text()

        # Validate the name.
        valid = validate.validate_dataset(self.main_dir, new_name)
        if valid != DatasetValidation.VALID:
            show_error_dialog(self, "Datasets", validate.validate_dataset_name_strings[valid])
            return

        # If the name is already in use, ask the user is they want to delete the old dataset.
        elif valid == DatasetValidation.IN_USE:
            del_old = show_question_dialog(self.window, "Datasets",
                                           "%s\n\nWould you like to delete the existing dataset?" %
                                           validate.validate_dataset_name_strings[valid])
            if del_old != Gtk.ResponseType.OK:
                return

            shutil.rmtree("%s/datasets/%s" % (self.main_dir, new_name))

        # Create the directory and file.
        io.write_blank_dataset(self.main_dir, new_name)
        io.write_metadata(self.main_dir, new_name, now=True)
        io.write_dataset(main_dir=self.main_dir, name=new_name, data=[])

        # Refresh the dataset list.
        self.update_list()
        self.add_ent.set_text("")

    def remove_datasets(self):
        """Removes datasets."""

        model, treeiter = self.treeview.get_selection().get_selected_rows()

        if treeiter is None:
            return

        # Get the datasets.
        datasets_list = []
        for i in treeiter:
            datasets_list.append(model[i][0])

        datasets_list_string = "\n\nSelected dataset%s:" % ("" if len(datasets_list) == 1 else "s")
        for dataset in datasets_list:
            datasets_list_string += "\n" + dataset

        if self.config["confirm_del"]:
            response = show_question_dialog(self, "Datasets",
                                            "Are you sure you want to remove the dataset%s? This action cannot be undone.%s" % (
                                            "" if len(datasets_list) == 1 else "s", datasets_list_string))
            if response != Gtk.ResponseType.OK:
                return

        # Delete the selected datasets.
        for name in datasets_list:
            if name == self.last_dataset:
                continue
            shutil.rmtree("%s/datasets/%s" % (self.main_dir, name))

        # Refresh the dataset list.
        self.update_list()

    def rename_dataset(self):
        """Rename a dataset."""

        model, treeiter = self.treeview.get_selection().get_selected_rows()

        if treeiter is None:
            return

        # Get the dataset name,
        old_name = None
        for i in treeiter:
            old_name = model[i][0]
            break

        # Get the dataset name.
        if old_name is None or old_name == self.last_dataset:
            return

        # Get the new dataset name.
        ren_dlg = GenericEntryDialog(self, title="Datasets",
                                     message="Enter new name for \"%s\"" % old_name)
        response = ren_dlg.run()
        new_name = ren_dlg.nam_ent.get_text().lstrip().rstrip()
        ren_dlg.destroy()

        if response != Gtk.ResponseType.OK:
            return

        if new_name == old_name:
            show_error_dialog(self, "Datasets", "The new name is the same as the old name.")
            return

        # Validate the name. If the name isn't valid, don't continue.
        valid = validate.validate_dataset(self.main_dir, new_name)
        if valid != DatasetValidation.VALID and valid != DatasetValidation.IN_USE:
            show_error_dialog(self, "Datasets", validate.validate_dataset_name_strings[valid])
            return

        # If the name is already in use, ask the user is they want to delete the old dataset.
        elif valid == DatasetValidation.IN_USE:
            del_old = show_question_dialog(self, "Datasets",
                                           "%s\n\nWould you like to delete the existing dataset?" %
                                           validate.validate_dataset_name_strings[valid])
            if del_old != Gtk.ResponseType.OK:
                return

            shutil.rmtree("%s/datasets/%s" % (self.main_dir, new_name))

        # Rename the directory.
        os.rename("%s/datasets/%s" % (self.main_dir, old_name), "%s/datasets/%s" % (self.main_dir, new_name))
        now = datetime.datetime.now()
        modified = "%d/%d/%d" % (now.day, now.month, now.year)
        creation, modified2 = io.get_metadata(self.main_dir, new_name)
        io.write_metadata(self.main_dir, new_name, creation, modified)

        # Refresh the dataset list.
        self.update_list()

    def switch_dataset(self):
        """Switches to a different dataset."""

        model, treeiter = self.treeview.get_selection().get_selected_rows()

        if treeiter is None:
            return

        # Get the dataset name,
        name = None
        for i in treeiter:
            name = model[i][0]
            break

        # Get the dataset name.
        if name is None or name == self.last_dataset:
            return

        # Set the field and return to the main window.
        self.switch_name = name
        self.response(Gtk.ResponseType.OK)
