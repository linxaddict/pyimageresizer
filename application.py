import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from main_view import MainWindow
from main_presenter import MainPresenter


class Application:
    def run(self) -> None:
        gtk_builder = Gtk.Builder()

        main_window = MainWindow('main_window.glade', gtk_builder)
        main_presenter = MainPresenter(main_window)
        main_window.set_presenter(main_presenter)

        main_window.show()

        Gtk.main()

if __name__ == '__main__':
    app = Application()
    app.run()
