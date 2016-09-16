import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


class MainWindow:
    DENSITIES = [
        ['xxxhdpi'],
        ['xxhdpi'],
        ['xhdpi'],
        ['hdpi'],
        ['mdpi'],
        ['ldpi']
    ]

    def _find_window(self, builder):
        return builder.get_object('window_main')

    def _find_density_list_store(self, builder):
        return builder.get_object('density_list_store')

    def _find_density_cbox(self, builder):
        return builder.get_object('cbox_density')

    def _append_densities(self, list_store):
        for density in MainWindow.DENSITIES:
            list_store.append(density)

    def __init__(self, view_resource: str):
        builder = Gtk.Builder()

        builder.add_from_file(view_resource)
        builder.connect_signals(self)

        self.window = self._find_window(builder)
        self.density_list_store = self._find_density_list_store(builder)
        self.cbox_density = self._find_density_cbox(builder)

        self._append_densities(self.density_list_store)

        self.cbox_density.set_active(0)

    def show(self):
        self.window.show_all()

    def on_delete_window(self, widget, data):
        Gtk.main_quit()

