import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from ui import MainWindow
from ui import MainPresenter

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class Application:

    def run(self) -> None:
        gtk_builder = Gtk.Builder()

        main_window = MainWindow('res/main_window.glade', gtk_builder)
        main_presenter = MainPresenter(main_window)
        main_window.set_presenter(main_presenter)

        main_window.show()

        Gtk.main()

if __name__ == '__main__':
    app = Application()
    app.run()
