import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from main_view import MainWindow

class Application:
    def run(self):
        main_window = MainWindow('main_window.glade')
        main_window.show()

        Gtk.main()

if __name__ == '__main__':
    app = Application()
    app.run()
