# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: dialogs/search_dialog.py
# This dialog allows the user to enter a basic search.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk


class SearchDialog(Gtk.Dialog):
    """Shows the dialog for a search."""
    
    def __init__(self, parent, last_dataset, config):
        """Create the dialog."""
        
        Gtk.Dialog.__init__(self, "Search", parent, Gtk.DialogFlags.MODAL, use_header_bar=True)
        self.set_size_request(400, 0)
        self.add_button("Search", Gtk.ResponseType.OK)

        # Create the header bar.
        header = self.get_header_bar()
        header.set_show_close_button(True)
        header.set_title("Search")
        header.set_subtitle(last_dataset)
        
        # Create the grid.
        qui_grid = Gtk.Grid()
        qui_grid.set_row_spacing(10)
        self.get_content_area().add(qui_grid)
        
        # Create the main input.
        inp_frame = Gtk.Frame()
        inp_frame.set_label("Search term")
        qui_grid.add(inp_frame)
        self.inp_ent = Gtk.Entry()
        self.inp_ent.set_hexpand(True)
        self.inp_ent.set_margin_top(5)
        self.inp_ent.set_margin_bottom(5)
        inp_frame.add(self.inp_ent)
        
        # Create the options.
        opt_frame = Gtk.Frame()
        opt_frame.set_label("Search options")
        qui_grid.attach_next_to(opt_frame, inp_frame, Gtk.PositionType.BOTTOM, 1, 1)
        self.case_chk = Gtk.CheckButton("Case insensitive")
        self.case_chk.set_tooltip_text("Match search term regardless of case.")
        self.case_chk.set_active(config["default_case_insensitive"])
        self.case_chk.set_margin_top(5)
        self.case_chk.set_margin_bottom(5)
        opt_frame.add(self.case_chk)
        
        # Connect 'Enter' key to the OK button.
        self.inp_ent.set_activates_default(True)
        ok_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
