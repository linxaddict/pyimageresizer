import os
import sys

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio
from pyimageresizer.ui import MainWindow
from pyimageresizer.ui import MainPresenter
from pyimageresizer.image import ImageProcessor

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

# This would typically be its own file
MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <attribute name="label" translatable="yes">Change label</attribute>
      <item>
        <attribute name="action">win.change_label</attribute>
        <attribute name="target">String 1</attribute>
        <attribute name="label" translatable="yes">String 1</attribute>
      </item>
      <item>
        <attribute name="action">win.change_label</attribute>
        <attribute name="target">String 2</attribute>
        <attribute name="label" translatable="yes">String 2</attribute>
      </item>
      <item>
        <attribute name="action">win.change_label</attribute>
        <attribute name="target">String 3</attribute>
        <attribute name="label" translatable="yes">String 3</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">win.maximize</attribute>
        <attribute name="label" translatable="yes">Maximize</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""


class Application(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id="com.machineinsight-it.pyimageresizer", **kwargs)
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        if not self.window:
            gtk_builder = Gtk.Builder()
            image_processor = ImageProcessor()

            base_path = os.path.abspath(os.path.dirname(__file__))
            resource_path = os.path.join(base_path, 'data/pyimageresizer.gresource')
            resource = Gio.Resource.load(resource_path)
            # noinspection PyProtectedMember
            Gio.Resource._register(resource)

            self.window = MainWindow('/main_window/main_window.glade', gtk_builder, self)
            main_presenter = MainPresenter(self.window, image_processor)
            self.window.set_presenter(main_presenter)

        self.window.window.set_wmclass('PyImageResizer', 'PyImageResizer')
        self.window.show()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()

        if options.contains("test"):
            # This is printed on the main instance
            print("Test argument recieved")

        self.activate()
        return 0

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()


if __name__ == '__main__':
    app = Application()
    app.run(sys.argv)
