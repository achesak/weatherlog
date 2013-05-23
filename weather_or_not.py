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
# Import pickle for loading and saving the data.
import pickle
# Import os for creating a directory.
import os
# Import os.path for seeing if a directory exists.
import os.path
# Import sys for sys.exit().
import sys


# Import the application's UI data.
from resources.ui import *
# Import the functions for getting the data.
import resources.functions as functions


# Check to see if the directory exists, and create it if it doesn't.
main_dir = "%s/.weatherornot" % os.path.expanduser("~")
if not os.path.exists(main_dir):
    # Create the directory.
    os.makedirs(main_dir)
    data = []
else:
    # If the directory exists, load the data.
    try:
        # This should be ~/.weatherornot/data.weather on Linux.
        data_file = open("%s/data.weather" % main_dir, "rb")
        data = pickle.load(data_file)
        data_file.close()
    
    except IOError:
        # Show the error message, and close the application.
        # This one shows if there was a problem reading the file.
        print("Error importing data (file could not be read).")
        sys.exit()
    
    except PickleError:
        # Show the error message, and close the application.
        # This one shows if there was a problem unpickling the data.
        print("Error importing data (data could not be unpickled).")
        sys.exit()


class AddNewDialog(Gtk.Dialog):
    """Shows the "Add New" dialog."""
    def __init__(self, parent):
        """Create the dialog."""
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Add New", parent, Gtk.DialogFlags.MODAL)
        
        # Add the buttons.
        self.add_button("OK", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        
        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        new_box.add(new_grid)
        
        # Create the Date label and entry. Replace with a proper datepicker later?
        date_lbl = Gtk.Label("Date: ")
        date_lbl.set_alignment(0, 0.5)
        new_grid.add(date_lbl)
        self.date_ent = Gtk.Entry()
        new_grid.attach_next_to(self.date_ent, date_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Temperature label and entry.
        temp_lbl = Gtk.Label("Temperature (°C): ")
        temp_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(temp_lbl, date_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.temp_ent = Gtk.Entry()
        new_grid.attach_next_to(self.temp_ent, temp_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Precipitation label, entry, and combobox.
        prec_lbl = Gtk.Label("Precipitation (cm): ")
        prec_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(prec_lbl, temp_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.prec_ent = Gtk.Entry()
        new_grid.attach_next_to(self.prec_ent, prec_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.prec_com = Gtk.ComboBoxText()
        for i in ["Rain", "Snow", "Hail", "Sleet"]:
            self.prec_com.append_text(i)
        new_grid.attach_next_to(self.prec_com, self.prec_ent, Gtk.PositionType.RIGHT, 1, 1)
        # Create the Wind label, entry, and combobox.
        wind_lbl = Gtk.Label("Wind (kph): ")
        wind_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(wind_lbl, prec_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.wind_ent = Gtk.Entry()
        new_grid.attach_next_to(self.wind_ent, wind_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.wind_com = Gtk.ComboBoxText()
        for i in ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]:
            self.wind_com.append_text(i)
        new_grid.attach_next_to(self.wind_com, self.wind_ent, Gtk.PositionType.RIGHT, 1, 1)
        # Create the Humidity label and entry.
        humi_lbl = Gtk.Label("Humidity (%): ")
        humi_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(humi_lbl, wind_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.humi_ent = Gtk.Entry()
        new_grid.attach_next_to(self.humi_ent, humi_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Air Pressure label and entry.
        airp_lbl = Gtk.Label("Air Pressure (mbar): ")
        airp_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(airp_lbl, humi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.airp_ent = Gtk.Entry()
        new_grid.attach_next_to(self.airp_ent, airp_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Cloud Cover label and combobox.
        clou_lbl = Gtk.Label("Cloud Cover: ")
        clou_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(clou_lbl, airp_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.clou_com = Gtk.ComboBoxText()
        for i in ["Sunny", "Mostly Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy"]:
            self.clou_com.append_text(i)
        new_grid.attach_next_to(self.clou_com, clou_lbl, Gtk.PositionType.RIGHT, 2, 1)
        # Create the Notes label and entry.
        note_lbl = Gtk.Label("Notes: ")
        note_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(note_lbl, clou_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.note_ent = Gtk.Entry()
        new_grid.attach_next_to(self.note_ent, note_lbl, Gtk.PositionType.RIGHT, 2, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()


class InfoDialog(Gtk.Dialog):
    """Shows the "Info" dialog."""
    def __init__(self, parent):
        """Create the dialog."""
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Info", parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        
        # Add the button.
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str, str)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        # Create the Category column.
        cate_text = Gtk.CellRendererText()
        cate_col = Gtk.TreeViewColumn("Category", cate_text, text = 0)
        self.treeview.append_column(cate_col)
        # Create the Value column.
        valu_text = Gtk.CellRendererText()
        valu_col = Gtk.TreeViewColumn("Value", valu_text, text = 1)
        self.treeview.append_column(valu_col)
        
        # Create the ScrolledWindow for displaying the list with a scrollbar.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        # Display the TreeView.
        scrolled_win.add(self.treeview)
        self.get_content_area().add(scrolled_win)
        
        # Add the data.
        ####### ADD THE STUFF TO CALCULATE THIS!
        self.liststore.append(["First day", "5/13/13"])
        self.liststore.append(["Last day", "5/14/13"])
        self.liststore.append(["Number of days", "1"])
        self.liststore.append(["Average temperature", "40 °C"])
        self.liststore.append(["Lowest temperature", "30 °C"])
        self.liststore.append(["Highest temperature", "50 °C"])
        self.liststore.append(["Average precipitation", "3.45 cm"])
        self.liststore.append(["Total precipitation", "56.42 cm"])
        self.liststore.append(["Average wind speed", "45 kph"])
        self.liststore.append(["Lowest wind speed", "0 kph"])
        self.liststore.append(["Highest wind speed", "99861 kph"])
        self.liststore.append(["Average humidity", "45%"])
        self.liststore.append(["Lowest humidity", "1%"])
        self.liststore.append(["Highest humidity", "99.8%"])
        self.liststore.append(["Average air pressure", "45 mbar"])
        self.liststore.append(["Lowest air pressure", "2 mbar"])
        self.liststore.append(["Highest air pressure", "100 mbar"])
        
        # Show the dialog. There's no need to get the response.
        self.show_all()


class Weather(Gtk.Window):
    """Shows the main application."""
    def __init__(self):
        """Create the application."""
        # Create the window.
        Gtk.Window.__init__(self, title = TITLE)
        # Set the default size. This should be a good value on all except
        # very tiny screens.
        self.set_default_size(900, 500)
        # Set the icon.
        self.set_icon_from_file("resources/icon.png")
        
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
            ("temperature", None, "_Temperature...", None, None, None),
            ("precipitation", None, "_Precipitation...", None, None, None),
            ("wind", None, "_Wind...", None, None, None),
            ("humidity", None, "_Humidity...", None, None, None),
            ("air_pressure", None, "_Air Pressure...", None, None, None),
            ("cloud_cover", None, "_Cloud Cover...", None, None, None),
            ("exit", Gtk.STOCK_QUIT, "E_xit...", None, "Close the application", lambda x: self.exit("ignore", "this"))
        ])
        
        # Create the Help menu.
        action_group.add_actions([
            ("help_menu", None, "Help"),
            ("about", Gtk.STOCK_ABOUT, "_About...", "F1", None, self.about)
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
        
        # Show the dialog.
        info_dlg = InfoDialog(self)
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
                data = pickle.load(data_file)
                data_file.close()
                
            except IOError:
                # Show the error message, and don't add the data.
                # This one shows if there was a problem reading the file.
                print("Error importing data (file could not be read).")
            
            except PickleError:
                # Show the error message, and don't add the data.
                # This one shows if there was a problem unpickling the data.
                print("Error importing data (data could not be unpickled).")
            
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
            
            # Save the data.
            try:
                # Write to the specified file.
                data_file = open(filename, "wb")
                pickle.dump(data, data_file)
                data_file.close()
            
            except IOError:
                # Show the error message.
                # This one shows if there was a problem writing to the file.
                print("Error importing data (file could not be written).")
            
            except PickleError:
                # Show the error message.
                # This one shows if there was a problem pickling the data.
                print("Error importing data (data could not be pickled).")
            
        # Close the dialog.
        export_dlg.destroy()
    
    
    def export_file_html(self, event):
        """Formats the data into a HTML table, then exports it to a file."""
        
        # Build the string.
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
<title>Data exported from Weather Or Not</title>
<meta charset="utf-8" />
</head>
<body>
<table>
<tr>
<th>Date</th>
<th>Temperature (°C)</th>
<th>Precipitation (cm)</th>
<th>Wind (kph)</th>
<th>Humidity (%)</th>
<th>Air Pressure (mbar)</th>
<th>Cloud Cover</th>
<th>Notes</th>
</tr>"""
        
        # Add the data. Loop through each list, and add it as a table row.
        for i in data:
            html += """
<tr>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
</tr>""" % (i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])
        
        html += """
</table>
</body>
</html>"""
        
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
                data_file.write(html.lstrip().rstrip())
                data_file.close()
                
            except IOError:
                # Show the error message.
                # This only shows if the error occurred when writing to the file.
                print("Error exporting data to HTML (file could not be written).")
            
        # Close the dialog.
        export_html_dlg.destroy()
    
    
    def export_file_csv(self, event):
        """Formats the data into CSV, then exports it to a file."""
        
        # Build the string.
        csv = ""
        for i in data:
            csv += """"%s","%s","%s","%s","%s","%s","%s","%s"\n""" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        
        # Remove the last newline character.
        csv = csv[:-1]
        
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
                print("Error exporting data to CSV.")
            
        # Close the dialog.
        export_csv_dlg.destroy()
    
    
    def about(self, event):
        """Shows the About dialog."""
        
        # Create the dialog.
        about_dlg = Gtk.AboutDialog()
        
        # Set the title.
        about_dlg.set_title("About Weather Or Not")
        # Set the program name.
        about_dlg.set_program_name("Weather Or Not")
        # Set the program version.
        about_dlg.set_version("0.1")
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
            pickle.dump(data, data_file)
            data_file.close()
            
        except:
            # Show the error message if something happened, but continue.
            print("Error saving data file.")
        
        # Close the application.
        Gtk.main_quit()


# Show the window and start the application.
if __name__ == "__main__":
    win = Weather()
    win.connect("delete-event", win.exit)
    win.show_all()
    Gtk.main()