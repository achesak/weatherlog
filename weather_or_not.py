# -*- coding: utf-8 -*-


################################################################################

# Weather Or Not
# Version 0.1

# Weather Or Not is an application for keeping track of the weather.

# Released under the MIT open source license:
"""
Copyright (c) 2013 Adam Chesak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

################################################################################


# Import any needed modules.
# Import Gtk for the interface.
from gi.repository import Gtk
# Import json for loading and saving the data.
import json
# Import os for creating a directory.
import os
# Import os.path for seeing if a directory exists.
import os.path
# Import sys for sys.exit().
import sys

# Tell Python not to create bytecode files.
sys.dont_write_bytecode = True

# Import the application's UI data.
from resources.ui import *
# Import the functions for various tasks.
import resources.utility_functions as utility_functions
# Import the functions for getting the data.
import resources.info_functions as info_functions
# Import the functions for exporting the data.
import resources.export as export
# Import the dialogs.
from resources.dialogs.new_dialog import *
from resources.dialogs.info_dialog import *


# Check to see if the directory exists, and create it if it doesn't.
main_dir = "%s/.weatherornot" % os.path.expanduser("~")
if not os.path.exists(main_dir) or not os.path.isdir(main_dir):
    # Create the directory.
    os.makedirs(main_dir)
    data = []
else:
    # If the directory exists, load the data.
    try:
        # This should be ~/.weatherornot/data.weather on Linux.
        data_file = open("%s/data.weather" % main_dir, "rb")
        data = json.load(data_file)
        data_file.close()
    
    except IOError:
        # Show the error message, and close the application.
        # This one shows if there was a problem reading the file.
        print("Error importing data (IOError).")
        sys.exit()
    
    except (TypeError, ValueError):
        # Show the error message, and close the application.
        # This one shows if there was a problem with the data type.
        print("Error importing data (TypeError or ValueError).")
        sys.exit()


class Weather(Gtk.Window):
    """Shows the main application."""
    def __init__(self):
        """Create the application."""
        # Create the window.
        Gtk.Window.__init__(self, title = TITLE)
        # Set the default size. This should be a good value on all except very tiny screens.
        self.set_default_size(900, 500)
        # Set the icon.
        self.set_icon_from_file("resources/images/icon.png")
        
        # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str, str, str, str, str, str, str, str)
        # Add the data.
        for i in data:
            self.liststore.append(i)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        # Create the Date column.
        date_text = Gtk.CellRendererText()
        date_col = Gtk.TreeViewColumn("Date", date_text, text = 0)
        self.treeview.append_column(date_col)
        # Create the Temperature column.
        temp_text = Gtk.CellRendererText()
        temp_col = Gtk.TreeViewColumn("Temperature (°C)", temp_text, text = 1)
        self.treeview.append_column(temp_col)
        # Create the Precipation column.
        prec_text = Gtk.CellRendererText()
        prec_col = Gtk.TreeViewColumn("Precipation (cm)", prec_text, text = 2)
        self.treeview.append_column(prec_col)
        # Create the Wind column.
        wind_text = Gtk.CellRendererText()
        wind_col = Gtk.TreeViewColumn("Wind (kph)", wind_text, text = 3)
        self.treeview.append_column(wind_col)
        # Create the Humidity column.
        humi_text = Gtk.CellRendererText()
        humi_col = Gtk.TreeViewColumn("Humidity (%)", humi_text, text = 4)
        self.treeview.append_column(humi_col)
        # Create the Air Pressure column.
        airp_text = Gtk.CellRendererText()
        airp_col = Gtk.TreeViewColumn("Air Pressure (mbar)", airp_text, text = 5)
        self.treeview.append_column(airp_col)
        # Create the Cloud Cover column.
        clou_text = Gtk.CellRendererText()
        clou_col = Gtk.TreeViewColumn("Cloud Cover", clou_text, text = 6)
        self.treeview.append_column(clou_col)
        # Create the Notes column.
        note_text = Gtk.CellRendererText()
        note_col = Gtk.TreeViewColumn("Notes", note_text, text = 7)
        self.treeview.append_column(note_col)
        
        # Create the ScrolledWindow for displaying the list with a scrollbar.
        scrolled_win = Gtk.ScrolledWindow()
        # The container should scroll both horizontally and vertically.
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        # Display the TreeView.
        scrolled_win.add(self.treeview)
        
        # Create the action group for the menus.
        action_group = Gtk.ActionGroup("actions")
        # Create the Weather menu.
        action_group.add_actions([
            ("weather_menu", None, "Weather"),
            ("add_new", Gtk.STOCK_NEW, "Add _New...", None, "Add a new day to the list", self.add_new),
            ("import", Gtk.STOCK_OPEN, "_Import...", None, "Import data from a file", self.import_file),
            ("export", Gtk.STOCK_SAVE, "_Export...", None, "Export data to a file", self.export_file),
            ("export_html", None, "Export to _HTML...", None, None, self.export_file_html),
            ("export_csv", None, "Export to _CSV...", None, None, self.export_file_csv),
            ("info", Gtk.STOCK_INFO, "_Info...", "<Control>i", "Show info about the data", self.show_info)
        ])
        
        # Create the Weather -> More Info submenu.
        action_weather_info_group = Gtk.Action("info_menu", "_More Info...", None, None)
        action_group.add_action(action_weather_info_group)
        action_group.add_actions([
            ("temperature", None, "_Temperature...", "<Control>t", None, None),
            ("precipitation", None, "_Precipitation...", "<Control>p", None, None),
            ("wind", None, "_Wind...", "<Control>w", None, None),
            ("humidity", None, "_Humidity...", "<Control>h", None, None),
            ("air_pressure", None, "_Air Pressure...", "<Control>a", None, None),
            ("cloud_cover", None, "_Cloud Cover...", "<Control>c", None, None),
            ("clear_data", None, "Clear _Data...", "<Control>d", None, self.clear),
            ("exit", Gtk.STOCK_QUIT, "E_xit...", None, "Close the application", lambda x: self.exit("ignore", "this"))
        ])
        
        # Create the Help menu.
        action_group.add_actions([
            ("help_menu", None, "Help"),
            ("about", Gtk.STOCK_ABOUT, "_About...", "<Shift>F1", None, self.about),
            ("help", Gtk.STOCK_HELP, "_Help...", None, None, None)
        ])
        
        # Create the UI manager.
        ui_manager = Gtk.UIManager()
        ui_manager.add_ui_from_string(MENU_DATA)
        
        # Add the accelerator group to the toplevel window
        accel_group = ui_manager.get_accel_group()
        self.add_accel_group(accel_group)
        ui_manager.insert_action_group(action_group)
        
        # Create the grid for the UI.
        grid = Gtk.Grid()
        
        # Add the menubar
        menubar = ui_manager.get_widget("/menubar")
        grid.add(menubar)
        
        # Add the toolbar.
        toolbar = ui_manager.get_widget("/toolbar")
        grid.attach_next_to(toolbar, menubar, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Add the ScrolledWindow with the TreeView.
        grid.attach_next_to(scrolled_win, toolbar, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Add the grid to the main window.
        self.add(grid)
        self.show_all()
    
    
    def add_new(self, event):
        """Shows the dialog for input of new data."""
        
        # Show the dialog.
        new_dlg = AddNewDialog(self)
        # Get the response.
        response = new_dlg.run()
        
        # If the user clicked the OK button, add the data.
        if response == Gtk.ResponseType.OK:
            
            # Get the data from the entries and comboboxes.
            date = new_dlg.date_ent.get_text()
            temp = new_dlg.temp_ent.get_text()
            prec = new_dlg.prec_ent.get_text()
            prec_type = new_dlg.prec_com.get_active_text()
            wind = new_dlg.wind_ent.get_text()
            wind_dir = new_dlg.wind_com.get_active_text()
            humi = new_dlg.humi_ent.get_text()
            airp = new_dlg.airp_ent.get_text()
            clou = new_dlg.clou_com.get_active_text()
            note = new_dlg.note_ent.get_text()
            
            # If anything required was missing, cancel this action. Everything is required except for the notes.
            if not date or not temp or not prec or not prec_type or not wind or not wind_dir or not humi or not airp or not clou:
                # Create the error dialog.
                err_miss_dlg = Gtk.MessageDialog(new_dlg, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Add New")
                err_miss_dlg.format_secondary_text("One or more fields was left blank.")
                # Show the error dialog.
                err_miss_dlg.run()
                # Close the error dialog and the "Add New" dialog. The second one
                # is needed because of a bug where the window will stop responding
                # to events, making it useless. Fix later!
                err_miss_dlg.destroy()
                new_dlg.destroy()
            else:
                
                # Add the data to the list
                new_data = [date, temp, "%s %s" % (prec, prec_type), "%s %s" % (wind, wind_dir), humi, airp, clou, note]
                self.liststore.append(new_data)
                data.append(new_data)
                
                # Close the dialog.
                new_dlg.destroy()
    
    
    def show_info(self, event):
        """Shows info about the data."""
        
        # Get the info.
        ### ADD CODE TO CALCULATE THESE LATER!!
        data = [["First day", "5/13/13"], ["Last day", "5/14/13"], ["Number of days", "1"], ["Average temperature", "40 °C"], ["Lowest temperature", "30 °C"], 
            ["Highest temperature", "50 °C"], ["Average precipitation", "3.45 cm"], ["Total precipitation", "56.42 cm"], ["Average wind speed", "45 kph"],
            ["Lowest wind speed", "0 kph"], ["Highest wind speed", "99861 kph"], ["Average humidity", "45%"], ["Lowest humidity", "1%"], 
            ["Highest humidity", "99.8%"], ["Average air pressure", "45 mbar"], ["Lowest air pressure", "2 mbar"], ["Highest air pressure", "100 mbar"]]        
        
        # Show the dialog.
        info_dlg = GenericInfoDialog(self, "Info", data)
        info_dlg.run()
        
        # Close the dialog. The response can be ignored.
        info_dlg.destroy()
    
    
    def import_file(self, event):
        """Imports data from a file."""
        
        # Create the dialog.
        import_dlg = Gtk.FileChooserDialog("Import", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        # Get the response.
        response = import_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Get the filename.
            filename = import_dlg.get_filename()
            
            # Clear the data.
            global data
            data[:] = []
            # Clear the ListStore.
            self.liststore.clear()
            
            # Read the data.
            try:
                # Read from the specified file. 
                data_file = open(filename, "rb")
                data = json.load(data_file)
                data_file.close()
                
            except IOError:
                # Show the error message, and don't add the data.
                # This one shows if there was a problem reading the file.
                print("Error importing data (IOError).")
            
            except (TypeError, ValueError):
                # Show the error message, and don't add the data.
                # This one shows if there was a problem with the data type.
                print("Error importing data (TypeError or ValueError).")
            
            else:
                # Add the new data.
                for i in data:
                    self.liststore.append(i)
            
        # Close the dialog.
        import_dlg.destroy()
    
    
    def export_file(self, event):
        """Exports the data to a file."""
        
        # Create the dialog.
        export_dlg = Gtk.FileChooserDialog("Export", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        export_dlg.set_do_overwrite_confirmation(True)
        
        # Get the response.
        response = export_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Get the filename.
            filename = export_dlg.get_filename()
            
        # Save to the file.
        try:
            # This should save to ~/.weatherornot/data.weather on Linux.
            data_file = open("%s/data.weather" % main_dir, "wb")
            json.dump(data, data_file, indent = 4)
            data_file.close()
            
        except IOError:
            # Show the error message if something happened, but continue.
            # This one is shown if there was an error writing to the file.
            print("Error saving data file (IOError).")
        
        except (TypeError, ValueError):
            # Show the error message if something happened, but continue.
            # This one is shown if there was an error with the data type.
            print("Error saving data file (TypeError or ValueError).")
            
        # Close the dialog.
        export_dlg.destroy()
    
    
    def export_file_html(self, event):
        """Formats the data into a HTML table, then exports it to a file."""
        
        # Convert to data to HTML.
        html = export.html(data)
        
        # Create the dialog.
        export_html_dlg = Gtk.FileChooserDialog("Export to HTML", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        export_html_dlg.set_do_overwrite_confirmation(True)
        
        # Get the response.
        response = export_html_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Get the filename.
            filename = export_html_dlg.get_filename()
            
            # Save the data.
            try:
                # Write to the specified file.
                data_file = open(filename, "w")
                data_file.write(html)
                data_file.close()
                
            except IOError:
                # Show the error message.
                # This only shows if the error occurred when writing to the file.
                print("Error exporting data to HTML (IOError).")
            
        # Close the dialog.
        export_html_dlg.destroy()
    
    
    def export_file_csv(self, event):
        """Formats the data into CSV, then exports it to a file."""
        
        # Convert the data to CSV.
        csv = export.csv(data)
        
        # Create the dialog.
        export_csv_dlg = Gtk.FileChooserDialog("Export to CSV", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        export_csv_dlg.set_do_overwrite_confirmation(True)
        
        # Get the response.
        response = export_csv_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Get the filename.
            filename = export_csv_dlg.get_filename()
            
            # Save the data.
            try:
                # Write to the specified file.
                data_file = open(filename, "w")
                data_file.write(csv)
                data_file.close()
                
            except IOError:
                # Show the error.
                # This only shows if the error occurred when writing to the file.
                print("Error exporting data to CSV (IOError).")
            
        # Close the dialog.
        export_csv_dlg.destroy()
    
    
    def clear(self, event):
        """Clears the data."""
        
        # Confirm that the user wants to clear the data.
        clear_dlg = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "Confirm Clear")
        clear_dlg.format_secondary_text("Are you sure you want to clear the data?")
        
        # Get the response.
        response = clear_dlg.run()
        
        # If the user confirms the clear:
        if response == Gtk.ResponseType.OK:
            
            # Clear the data.
            global data
            data[:] = []
            
            # Clear the ListStore.
            self.liststore.clear()
        
        # Close the dialog.
        clear_dlg.destroy()
    
    
    def about(self, event):
        """Shows the About dialog."""
        
        # Create the dialog.
        about_dlg = Gtk.AboutDialog()
        
        # Set the title.
        about_dlg.set_title("About Weather Or Not")
        # Set the program name.
        about_dlg.set_program_name(TITLE)
        # Set the program version.
        about_dlg.set_version(VERSION)
        # Set the comments. Maybe come up with something better later?
        about_dlg.set_comments("Weather Or Not is an application for keeping track of the weather.")
        # Set the copyright notice. Legal stuff, bleh.
        about_dlg.set_copyright("Copyright (c) 2013 Adam Chesak")
        # Set the authors. This is, of course, only me. I feel special.
        about_dlg.set_authors(["Adam Chesak <achesak@yahoo.com>"])
        # Set the license. I think this can be used with GTK3? (It's LGPL.)
        about_dlg.set_license_type(Gtk.License.MIT_X11)
        # Set the website. Change this to the site on github, when I get that up.
        about_dlg.set_website("http://poultryandprogramming.wordpress.com/")
        about_dlg.set_website_label("http://poultryandprogramming.wordpress.com/")
        
        # Show the dialog.
        about_dlg.show_all()
        
        # Have the dialog close when the user presses the Close button.
        # There is only one button, so it's not necessary to check for 
        # Gtk.ResponseType.CLOSE here.
        about_dlg.run()
        about_dlg.destroy()


    def exit(self, x, y):
        """Saves data and closes the application."""
        
        # Save to the file.
        try:
            # This should save to ~/.weatherornot/data.weather on Linux.
            data_file = open("%s/data.weather" % main_dir, "wb")
            json.dump(data, data_file, indent = 4)
            data_file.close()
            
        except IOError:
            # Show the error message if something happened, but continue.
            # This one is shown if there was an error writing to the file.
            print("Error saving data file (IOError).")
        
        except (TypeError, ValueError):
            # Show the error message if something happened, but continue.
            # This one is shown if there was an error with the data type.
            print("Error saving data file (TypeError or ValueError).")
        
        # Close the  application.
        Gtk.main_quit()


# Show the window and start the application.
if __name__ == "__main__":
    win = Weather()
    win.connect("delete-event", win.exit)
    win.show_all()
    Gtk.main()