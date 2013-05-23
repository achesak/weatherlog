# Define the UI variables.
VERSION = "0.1"
TITLE = "Weather Or Not"
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
      <menuitem action="exit" />
    </menu>
    <menu action="help_menu">
      <menuitem action="about" />
    </menu>
  </menubar>
  <toolbar name="toolbar">
    <toolitem action="add_new" />
    <toolitem action="info" />
    <separator />
    <toolitem action="import" />
    <toolitem action="export" />
    <separator />
    <toolitem action="exit" />
  </toolbar>
</ui>
"""