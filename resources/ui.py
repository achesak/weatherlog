# -*- coding: utf-8 -*-


# This file defines variables used by the UI.


# Define the version and title. These are used in the About dialog.
VERSION = "0.1"
TITLE = "Weather Or Not"


# Define the menu and toolbar XML.
MENU_DATA = """
<ui>
  <menubar name="menubar">
    <menu action="weather_menu">
      <menuitem action="add_new" />
      <separator />
      <menuitem action="import" />
      <menuitem action="export" />
      <menuitem action="export_html" />
      <menuitem action="export_csv" />
      <separator />
      <menuitem action="info" />
      <menu action="info_menu">
        <menuitem action="temperature" />
        <menuitem action="precipitation" />
        <menuitem action="wind" />
        <menuitem action="humidity" />
        <menuitem action="air_pressure" />
        <menuitem action="cloud_cover" />
      </menu>
      <separator />
      <menuitem action="clear_data" />
      <separator />
      <menuitem action="fullscreen" />
      <separator />
      <menuitem action="exit" />
    </menu>
    <menu action="help_menu">
      <menuitem action="about" />
      <menuitem action="help" />
    </menu>
  </menubar>
  <toolbar name="toolbar">
    <toolitem action="add_new" />
    <toolitem action="info" />
    <separator />
    <toolitem action="import" />
    <toolitem action="export" />
    <separator />
    <toolitem action="clear_data" />
    <separator />
    <toolitem action="fullscreen" />
    <separator />
    <toolitem action="exit" />
  </toolbar>
</ui>
"""