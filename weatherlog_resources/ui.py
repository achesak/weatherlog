# -*- coding: utf-8 -*-


# This file defines variables used by the UI.


# Define the version and title. These are used in the About dialog.
VERSION = "1.9"
TITLE = "WeatherLog"

# Define the menu and toolbar XML.
menu_file = open("weatherlog_resources/menu.xml", "r")
MENU_DATA = menu_file.read()
menu_file.close()
