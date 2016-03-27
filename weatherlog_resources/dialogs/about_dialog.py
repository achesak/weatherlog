# -*- coding: utf-8 -*-


# This file defines the About dialog.


# Import Gtk for the dialog.
from gi.repository import Gtk


class WeatherLogAboutDialog(Gtk.AboutDialog):
    """Shows the About dialog."""
    
    def __init__(self, parent, title, version, icon, license_text):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.AboutDialog.__init__(self, parent)
        
        # Set the details.
        self.set_title("About WeatherLog")
        self.set_program_name(title)
        self.set_logo(icon)
        self.set_version(version)
        self.set_comments("WeatherLog is an application for keeping track of the weather\nand getting information about past trends.")
        self.set_copyright("Copyright (c) 2013-2016 Adam Chesak")
        self.set_authors(["Adam Chesak <achesak@yahoo.com>"])
        self.set_license(license_text)
        self.set_website("https://github.com/achesak/weatherlog")
        self.set_website_label("https://github.com/achesak/weatherlog")
        
        # Show the dialog.
        self.show_all()
