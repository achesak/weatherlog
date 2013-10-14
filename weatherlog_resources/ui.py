# -*- coding: utf-8 -*-


# This file defines variables used by the UI.


# Define the version and title. These are used in the About dialog.
VERSION = "1.4.3"
TITLE = "WeatherLog"

# Define the menu and toolbar XML.
MENU_DATA = """
<ui>
  <menubar name="menubar">
    <menu action="weather_menu">
      <menuitem action="add_new" />
      <menuitem action="remove" />
      <separator />
      <menuitem action="import" />
      <menuitem action="import_profile" />
      <menuitem action="import_append" />
      <menuitem action="export" />
      <menu action="export_menu">
        <menuitem action="export_html" />
        <menuitem action="export_csv" />
        <separator />
        <menuitem action="export_pastebin" />
        <menuitem action="export_pastebin_html" />
        <menuitem action="export_pastebin_csv" />
      </menu>
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
      <menuitem action="info_range" />
      <menu action="info_range_menu">
        <menuitem action="temperature_range" />
        <menuitem action="precipitation_range" />
        <menuitem action="wind_range" />
        <menuitem action="humidity_range" />
        <menuitem action="air_pressure_range" />
        <menuitem action="cloud_cover_range" />
      </menu>
      <separator />
      <menuitem action="clear_data" />
      <menuitem action="clear_all" />
      <separator />
      <menuitem action="reload_current" />
      <menuitem action="manual_save" />
      <separator />
      <menuitem action="fullscreen" />
      <separator />
      <menuitem action="exit" />
    </menu>
    <menu action="profiles_menu">
      <menuitem action="switch_profile" />
      <separator />
      <menuitem action="add_profile" />
      <menuitem action="remove_profile" />
    </menu>
    <menu action="options_menu">
      <menuitem action="options" />
    </menu>
    <menu action="help_menu">
      <menuitem action="about" />
      <separator />
      <menuitem action="help" />
    </menu>
  </menubar>
  <toolbar name="toolbar">
    <toolitem action="add_new" />
    <toolitem action="remove" />
    <separator />
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
