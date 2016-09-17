import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from model import Density

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class MainWindow:

    def _find_window(self, builder: Gtk.Builder) -> Gtk.Window:
        return builder.get_object('window_main')

    def _find_density_list_store(self, builder: Gtk.Builder) -> Gtk.CheckButton:
        return builder.get_object('density_list_store')

    def _find_density_cbox(self, builder: Gtk.Builder) -> Gtk.CheckButton:
        return builder.get_object('cbox_density')

    def _find_xxxhdpi_chbox(self, builder: Gtk.Builder) -> Gtk.CheckButton:
        return builder.get_object('chbox_xxxhdpi')

    def _find_xxhdpi_chbox(self, builder: Gtk.Builder) -> Gtk.CheckButton:
        return builder.get_object('chbox_xxhdpi')

    def _find_xhdpi_chbox(self, builder: Gtk.Builder) -> Gtk.CheckButton:
        return builder.get_object('chbox_xhdpi')

    def _find_hdpi_chbox(self, builder: Gtk.Builder) -> Gtk.CheckButton:
        return builder.get_object('chbox_hdpi')

    def _find_mdpi_chbox(self, builder: Gtk.Builder) -> Gtk.CheckButton:
        return builder.get_object('chbox_mdpi')

    def _find_ldpi_chbox(self, builder: Gtk.Builder) -> Gtk.CheckButton:
        return builder.get_object('chbox_ldpi')

    def _append_densities(self, list_store: Gtk.ListStore, densities: [str]):
        for density in densities:
            list_store.append(density)

    def _initialize_views_state(self, presenter) -> None:
        self.chbox_xxxhdpi.set_active(presenter.xxxhdpi)
        self.chbox_xxhdpi.set_active(presenter.xxhdpi)
        self.chbox_xhdpi.set_active(presenter.xhdpi)
        self.chbox_hdpi.set_active(presenter.hdpi)
        self.chbox_mdpi.set_active(presenter.mdpi)
        self.chbox_ldpi.set_active(presenter.ldpi)

        self._append_densities(self.density_list_store, presenter.generate_densities())
        self.cbox_density.set_active(0)

    def __init__(self, view_resource: str, gtk_builder: Gtk.Builder):
        gtk_builder.add_from_file(view_resource)
        gtk_builder.connect_signals(self)

        self.window = self._find_window(gtk_builder)
        self.density_list_store = self._find_density_list_store(gtk_builder)
        self.cbox_density = self._find_density_cbox(gtk_builder)

        self.chbox_xxxhdpi = self._find_xxxhdpi_chbox(gtk_builder)
        self.chbox_xxhdpi = self._find_xxhdpi_chbox(gtk_builder)
        self.chbox_xhdpi = self._find_xhdpi_chbox(gtk_builder)
        self.chbox_hdpi = self._find_hdpi_chbox(gtk_builder)
        self.chbox_mdpi = self._find_mdpi_chbox(gtk_builder)
        self.chbox_ldpi = self._find_ldpi_chbox(gtk_builder)

    def set_presenter(self, presenter) -> None:
        self.presenter = presenter
        self._initialize_views_state(presenter)

    def show(self) -> None:
        self.window.show_all()

    def on_delete_window(self, widget: Gtk.Widget, data) -> None:
        Gtk.main_quit()

    def on_xxxhdpi_toggled(self, widget: Gtk.Widget) -> None:
        if self.presenter.xxxhdpi != widget.get_active():
            self.presenter.xxxhdpi = widget.get_active()

    def on_xxhdpi_toggled(self, widget: Gtk.Widget) -> None:
        if self.presenter.xxhdpi != widget.get_active():
            self.presenter.xxhdpi = widget.get_active()

    def on_xhdpi_toggled(self, widget: Gtk.Widget) -> None:
        if self.presenter.xhdpi != widget.get_active():
            self.presenter.xhdpi = widget.get_active()

    def on_hdpi_toggled(self, widget: Gtk.Widget) -> None:
        if self.presenter.hdpi != widget.get_active():
            self.presenter.hdpi = widget.get_active()

    def on_mdpi_toggled(self, widget: Gtk.Widget) -> None:
        if self.presenter.mdpi != widget.get_active():
            self.presenter.mdpi = widget.get_active()

    def on_ldpi_toggled(self, widget: Gtk.Widget) -> None:
        if self.presenter.ldpi != widget.get_active():
            self.presenter.ldpi = widget.get_active()

    def on_density_cbox_changed(self, widget: Gtk.Widget) -> None:
        tree_iter = widget.get_active_iter()

        if tree_iter != None:
            model = widget.get_model()
            name = model[tree_iter][:1]

            self.presenter.density = Density(name[0])

    def toggle_xxxhdpi(self, toggled: bool) -> None:
        self.chbox_xxxhdpi.set_active(toggled)

    def toggle_xxhdpi(self, toggled: bool) -> None:
        self.chbox_xxhdpi.set_active(toggled)

    def toggle_xhdpi(self, toggled: bool) -> None:
        self.chbox_xhdpi.set_active(toggled)

    def toggle_hdpi(self, toggled: bool) -> None:
        self.chbox_hdpi.set_active(toggled)

    def toggle_mdpi(self, toggled: bool) -> None:
        self.chbox_mdpi.set_active(toggled)

    def toggle_ldpi(self, toggled: bool) -> None:
        self.chbox_ldpi.set_active(toggled)
