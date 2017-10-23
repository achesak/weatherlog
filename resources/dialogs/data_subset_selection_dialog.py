# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/data_subset_selection_dialog.py
# This dialog allows the user to enter a detailed search.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk, Gdk

# Import application modules.
from resources.constants import *
import resources.datasets as datasets
import resources.filter_data as filter_data
import resources.export as export
from resources.dialogs.data_subset_dialog import DataSubsetDialog
from resources.dialogs.misc_dialogs import *


class DataSubsetSelectionDialog(Gtk.Window):
    """Shows the data subset selection dialog."""

    def __init__(self, dataset, data, config, units):
        """Create the dialog."""

        Gtk.Window.__init__(self)
        self.set_title("Data Subset")
        self.set_resizable(True)
        self.set_default_size(600, 300)
        self.conditions = []
        self.last_dataset = dataset
        self.data = data
        self.config = config
        self.units = units

        # Create the header bar.
        header = Gtk.HeaderBar()
        header.set_title("Data Subset")
        header.set_subtitle(dataset)
        header.set_show_close_button(True)
        self.ok_btn = Gtk.Button(label="View")
        self.ok_btn.connect("clicked", self.view_subset)
        header.pack_end(self.ok_btn)
        self.set_titlebar(header)

        # Create the grid.
        sel_grid = Gtk.Grid()
        sel_grid.set_margin_top(5)
        sel_grid.set_margin_bottom(5)
        sel_grid.set_margin_left(5)
        sel_grid.set_margin_right(5)
        sel_grid.set_column_spacing(10)
        input_grid = Gtk.Grid()
        input_grid.set_row_spacing(10)
        view_frame = Gtk.Frame()
        view_frame.set_label("All conditions")
        view_grid = Gtk.Grid()
        view_grid.set_row_spacing(5)
        view_grid.set_column_spacing(5)
        view_grid.set_border_width(5)
        view_frame.add(view_grid)
        sel_grid.add(input_grid)
        sel_grid.attach_next_to(view_frame, input_grid, Gtk.PositionType.RIGHT, 1, 1)
        self.add(sel_grid)

        # Create the mode widgets.
        mode_frame = Gtk.Frame()
        mode_frame.set_label("Selection mode")
        mode_grid = Gtk.Grid()
        mode_grid.set_row_spacing(5)
        mode_grid.set_column_spacing(5)
        mode_grid.set_border_width(5)
        self.mode_btn_all = Gtk.RadioButton.new_with_label_from_widget(None, "Match all")
        self.mode_btn_one = Gtk.RadioButton.new_with_label_from_widget(self.mode_btn_all, "Match at least one")
        self.mode_btn_none = Gtk.RadioButton.new_with_label_from_widget(self.mode_btn_all, "Match none")
        if config["default_selection_mode"] == "Match all":
            self.mode_btn_all.set_active(True)
        elif config["default_selection_mode"] == "Match at least one":
            self.mode_btn_one.set_active(True)
        elif config["default_selection_mode"] == "Match none":
            self.mode_btn_none.set_active(True)
        mode_grid.add(self.mode_btn_all)
        mode_grid.attach_next_to(self.mode_btn_one, self.mode_btn_all, Gtk.PositionType.BOTTOM, 1, 1)
        mode_grid.attach_next_to(self.mode_btn_none, self.mode_btn_one, Gtk.PositionType.BOTTOM, 1, 1)
        mode_frame.add(mode_grid)
        input_grid.add(mode_frame)

        # Create the options.
        opt_frame = Gtk.Frame()
        opt_grid = Gtk.Grid()
        opt_grid.set_row_spacing(5)
        opt_grid.set_column_spacing(5)
        opt_grid.set_border_width(5)
        opt_frame.set_label("Search options")
        self.case_chk = Gtk.CheckButton("Case insensitive")
        self.case_chk.set_tooltip_text("Match search term regardless of case.")
        self.case_chk.set_active(config["default_case_insensitive"])
        self.case_chk.set_margin_top(5)
        opt_grid.add(self.case_chk)
        self.rsearch_chk = Gtk.CheckButton("Reset conditions after search")
        self.rsearch_chk.set_tooltip_text("Reset the conditions after search completion")
        self.rsearch_chk.set_active(config["reset_search"])
        self.rsearch_chk.set_margin_bottom(5)
        opt_grid.attach_next_to(self.rsearch_chk, self.case_chk, Gtk.PositionType.BOTTOM, 1, 1)
        opt_frame.add(opt_grid)
        input_grid.attach_next_to(opt_frame, mode_frame, Gtk.PositionType.BOTTOM, 1, 1)

        # Create the new condition widgets.
        cond_frame = Gtk.Frame()
        cond_frame.set_label("New condition")
        cond_grid = Gtk.Grid()
        cond_grid.set_row_spacing(5)
        cond_grid.set_column_spacing(5)
        cond_grid.set_border_width(5)
        field_lbl = Gtk.Label("Field: ")
        field_lbl.set_alignment(0, 0.5)
        cond_grid.add(field_lbl)
        self.field_com = Gtk.ComboBoxText()
        for i in ["Date", "Temperature", "Wind Chill", "Precipitation Amount", "Precipitation Type", "Wind Speed",
                  "Wind Direction", "Humidity", "Air Pressure", "Air Pressure Change", "Visibility", "Cloud Cover",
                  "Cloud Type", "Notes"]:
            self.field_com.append_text(i)
        self.field_com.set_active(0)
        cond_grid.attach_next_to(self.field_com, field_lbl, Gtk.PositionType.RIGHT, 1, 1)
        cond_lbl = Gtk.Label("Operator: ")
        cond_lbl.set_alignment(0, 0.5)
        cond_grid.attach_next_to(cond_lbl, field_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.cond_com = Gtk.ComboBoxText()
        for i in ["Equal To", "Not Equal To", "Greater Than", "Less Than", "Greater Than or Equal To",
                  "Less Than or Equal To", "Between", "Between (Inclusive)", "Outside", "Outside (Inclusive)",
                  "Starts With", "Does Not Start With", "Ends With", "Does Not End With", "Contains",
                  "Does Not Contain"]:
            self.cond_com.append_text(i)
        self.cond_com.set_active(0)
        cond_grid.attach_next_to(self.cond_com, cond_lbl, Gtk.PositionType.RIGHT, 1, 1)
        value_lbl = Gtk.Label("Value: ")
        value_lbl.set_alignment(0, 0.5)
        cond_grid.attach_next_to(value_lbl, cond_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.value_ent = Gtk.Entry()
        cond_grid.attach_next_to(self.value_ent, value_lbl, Gtk.PositionType.RIGHT, 1, 1)
        cond_btn_grid = Gtk.Grid()
        cond_btn_grid.set_column_spacing(5)
        cond_grid.attach_next_to(cond_btn_grid, value_lbl, Gtk.PositionType.BOTTOM, 2, 1)
        self.clear_btn = Gtk.Button(label="Clear")
        self.clear_btn.set_hexpand(True)
        self.clear_btn.connect("clicked", self.clear_condition)
        cond_btn_grid.attach(self.clear_btn, 0, 0, 1, 1)
        self.add_btn = Gtk.Button(label="Add")
        self.add_btn.set_hexpand(True)
        self.add_btn.connect("clicked", self.add_condition)
        cond_btn_grid.attach(self.add_btn, 1, 0, 1, 1)
        cond_frame.add(cond_grid)
        input_grid.attach_next_to(cond_frame, opt_frame, Gtk.PositionType.BOTTOM, 1, 1)

        # Create the data conditions listbox.
        self.liststore = Gtk.ListStore(str, str, str)
        self.treeview = Gtk.TreeView(model=self.liststore)
        self.treeview.set_headers_visible(False)
        self.treeview.set_size_request(400, 300)
        field_text = Gtk.CellRendererText()
        self.field_col = Gtk.TreeViewColumn("Field", field_text, text=0)
        self.field_col.set_expand(True)
        self.treeview.append_column(self.field_col)
        cond_text = Gtk.CellRendererText()
        self.cond_col = Gtk.TreeViewColumn("Operator", cond_text, text=1)
        self.cond_col.set_expand(True)
        self.treeview.append_column(self.cond_col)
        value_text = Gtk.CellRendererText()
        self.value_col = Gtk.TreeViewColumn("Value", value_text, text=2)
        self.value_col.set_expand(True)
        self.treeview.append_column(self.value_col)
        self.treeview.set_hexpand(True)
        self.treeview.set_vexpand(True)
        self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        view_grid.add(self.treeview)
        self.treeview.connect("key-press-event", self.treeview_keypress)

        # Create the buttons.
        sel_grid = Gtk.Grid()
        sel_grid.set_column_spacing(5)
        self.reset_btn = Gtk.Button(label="Reset")
        self.reset_btn.set_hexpand(True)
        self.reset_btn.connect("clicked", self.reset_conditions)
        sel_grid.attach(self.reset_btn, 0, 0, 1, 1)
        self.remove_btn = Gtk.Button(label="Remove")
        self.remove_btn.set_hexpand(True)
        self.remove_btn.connect("clicked", self.remove_condition)
        sel_grid.attach(self.remove_btn, 1, 0, 1, 1)
        view_grid.attach_next_to(sel_grid, self.treeview, Gtk.PositionType.BOTTOM, 1, 1)

        # Show the window.
        self.show_all()

    def treeview_keypress(self, widget, event):
        """Checks the treeview for keypress events."""

        # On 'Delete', remove selected row(s).
        if event.keyval == Gdk.KEY_Delete:
            self.remove_condition(True)

    def check_operator(self, field, operator):
        """Checks if the selected operator can be used with the selected field."""

        # If the column that is being compared is precipitation type, wind direction, air pressure change,
        # cloud cover, or cloud type, and the comparison is numerical, don't continue.
        disallowed = False
        if field == "Precipitation Type" or field == "Wind Direction" or field == "Air Pressure Change" or \
                        field == "Cloud Cover" or field == "Cloud Type" or field == "Notes":
            if operator != "Equal To" and operator != "Not Equal To" and operator != "Starts With" and \
                            operator != "Does Not Start With" and operator != "Ends With" and operator != "Does Not End With" and \
                            operator != "Contains" and operator != "Does Not Contain":

                disallowed = True
        # If the column that is being compared is a numerical field and the
        # comparison is strictly non-numerical,
        # don't continue.
        else:
            if operator == "Starts With" or operator == "Does Not Start With" or operator == "Ends With" or \
                            operator == "Does Not End With" or operator == "Contains" or operator == "Does Not Contain":
                disallowed = True
        # If the column that is being compared is date, only allow equals and not equal to.
        if field == "Date" and operator != "Equal To" and operator != "Not Equal To":
            disallowed = True

        if disallowed:
            show_error_dialog(self, "Add Condition", "Invalid comparison: %s cannot use the \"%s\" operator." % (field, operator))
        return disallowed

    def check_one(self, operator, value):
        """Checks if there is one value, if the operator requires that."""

        if operator != "Between" and operator != "Between (Inclusive)" and operator != "Outside" and \
                        operator != "Outside (Inclusive)" and operator != "Equal To" and operator != "Not Equal To":
            if value.count(",") != 0:
                show_error_dialog(self, "Add Condition",
                                  "The \"%s\" operator requires only one value to be specified." % operator)
                return True
        return False

    def check_two(self, operator, value):
        """Checks if there are two values, if the operator requires that."""

        if operator == "Between" or operator == "Between (Inclusive)" or operator == "Outside" or \
                        operator == "Outside (Inclusive)":
            if value.count(",") != 1:
                show_error_dialog(self, "Add Condition",
                                  "The \"%s\" operator requires two values to be specified, separated with a comma." % operator)
                return True
        return False

    def check_values(self, field, operator, value):
        """Checks that the values are in the correct format for the field."""

        # Temperature, wind chill, precipitation amount, wind speed, humidity, air pressure, visibility:
        # REQUIREMENT: only numerical
        if field in ["Temperature", "Wind Chill", "Precipitation Amount", "Wind Speed", "Humidity", "Air Pressure",
                     "Visibility"]:
            value = [x.strip() for x in value.split(',')]
            for i in value:
                try:
                    float(i)
                except ValueError:
                    show_error_dialog(self, "Add Condition", "%s cannot be compared to the value \"%s\"." % (field, i))
                    return True
        return False

    def clear_condition(self, widget):
        """Clears the input fields."""

        # Clear the fields.
        self.field_com.set_active(0)
        self.cond_com.set_active(0)
        self.value_ent.set_text("")

    def reset_conditions(self, widget, confirm=True):
        """Resets all fields and clears all conditions."""

        # Ask the user to confirm.
        if confirm and show_question_dialog(self, "Reset",
                                            "Are you sure you want to reset all conditions?") != Gtk.ResponseType.OK:
            return

        # Clear the fields.
        self.mode_btn_all.set_active(1)
        self.mode_btn_one.set_active(0)
        self.mode_btn_none.set_active(0)
        self.field_com.set_active(0)
        self.cond_com.set_active(0)
        self.value_ent.set_text("")
        self.liststore.clear()

        # Clear the data.
        self.conditions = []

    def add_condition(self, widget):
        """Shows the add condition dialog."""

        # Get the entered values
        field = self.field_com.get_active_text()
        condition = self.cond_com.get_active_text()
        value = self.value_ent.get_text()

        # Validate the data, and add if it's acceptable.
        if not self.check_operator(field, condition) and not \
            self.check_two(condition, value) and not self.check_one(condition, value) and \
            value.lstrip().rstrip() != "" and not self.check_values(field, condition, value):
            self.liststore.append([field, condition, value])
            self.conditions.append([field, condition, value])

    def remove_condition(self, widget):
        """Removes the selected condition."""

        # Get the selected conditions.
        model, treeiter = self.treeview.get_selection().get_selected_rows()
        conds = []
        for i in treeiter:
            conds.append(model[i][0])

        # Don't continue if nothing was selected.
        if len(conds) == 0:
            return

        # Remove the conditions and update the UI.
        for i in conds:
            index = datasets.get_column(self.conditions, 0).index(i)
            del self.conditions[index]

        self.liststore.clear()
        for i in self.conditions:
            self.liststore.append(i)

    def view_subset(self, widget):
        """Filters the data and displays the subset."""

        # Get the selection mode and conditions.
        if self.mode_btn_all.get_active():
            sel_mode = SelectionMode.ALL
        elif self.mode_btn_one.get_active():
            sel_mode = SelectionMode.ONE
        elif self.mode_btn_none.get_active():
            sel_mode = SelectionMode.NONE
        opt_insensitive = self.case_chk.get_active()
        conditions = []
        for i in self.liststore:
            if i[2].lstrip().rstrip() == "":
                continue
            conditions.append(i[:])

        # If there are no conditions, don't continue.
        if len(conditions) == 0:
            show_alert_dialog(self, "Data Subset Results", "No conditions entered.")
            return

        # Loop through the conditions and filter the data.
        filtered = []
        first = True
        for i in conditions:

            # Get the filtered list.
            subset = filter_data.filter_data(self.data, i, opt_insensitive)

            # If this is the first condition, add all the data to the filtered list.
            if first:
                filtered += subset
                first = False

            # Otherwise, make sure it is combined correctly.
            # AND combination mode:
            elif sel_mode == SelectionMode.ALL:
                filtered = filter_data.filter_and(filtered, subset)

            # OR combination mode or NOT combination mode:
            elif sel_mode == SelectionMode.ONE or SelectionMode.NONE:
                filtered = filter_data.filter_or(filtered, subset)

        # If the NOT combination mode is used, apply that filter as well.
        if sel_mode == SelectionMode.NONE:
            filtered = filter_data.filter_not(filtered, self.data)

        # If there are no items that match the condition, don't show the main dialog.
        if len(filtered) == 0:
            show_alert_dialog(self, "Data Subset Results",
                              "No data matches the specified condition%s." % ("s" if len(conditions) != 1 else ""))
            return

        # If reset conditions is selected, clear them.
        if self.rsearch_chk.get_active():
            self.reset_conditions(1, confirm=False)

        # Show the subset.
        sub_dlg = DataSubsetDialog(self, "Data Subset Results", self.last_dataset, filtered, self.units,
                                   self.config)
        response = sub_dlg.run()
        sub_dlg.destroy()

        # If the user clicked Export:
        if response == DialogResponse.EXPORT:

            # Get the filename and export the info.
            response2, filename = show_export_dialog(self, "Export Data Subset Results")
            if response2 == Gtk.ResponseType.OK:
                data_list = [["WeatherLog Data Subset Results - %s - %s to %s" % (
                    self.last_dataset, (filtered[0][0] if len(filtered) != 0 else "None"),
                    (filtered[len(filtered) - 1][0] if len(filtered) != 0 else "None")),
                              ["Date", "Temperature (%s)" % self.units["temp"], "Wind Chill (%s)" % self.units["temp"],
                               "Precipitation (%s)" % self.units["prec"], "Wind (%s)" % self.units["wind"],
                               "Humidity (%)", "Air Pressure (%s)" % self.units["airp"],
                               "Visibility (%s)" % self.units["visi"],
                               "Cloud Cover", "Notes"],
                              filtered]]
                export.html_generic(data_list, filename)
