import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import GdkPixbuf
from model import Density

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class MainWindow:
    IMAGE_WIDTH = 250
    IMAGE_HEIGHT = 250

    def _find_views(self, builder: Gtk.Builder) -> None:
        self.window = builder.get_object('window_main')

        self.density_list_store = builder.get_object('density_list_store')
        self.cbox_density = builder.get_object('cbox_density')

        self.chbox_xxxhdpi = builder.get_object('chbox_xxxhdpi')
        self.chbox_xxhdpi = builder.get_object('chbox_xxhdpi')
        self.chbox_xhdpi = builder.get_object('chbox_xhdpi')
        self.chbox_hdpi = builder.get_object('chbox_hdpi')
        self.chbox_mdpi = builder.get_object('chbox_mdpi')
        self.chbox_ldpi = builder.get_object('chbox_ldpi')

        self.imgv_preview = builder.get_object('imgv_preview')
        self.btn_scale = builder.get_object('btn_scale')

        self.dialog_image_error = builder.get_object('dialog_image_error')

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

        self._find_views(gtk_builder)

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

    def on_scale_button_sensitivity_changed(self, sensitive: bool) -> None:
        self.btn_scale.set_sensitive(sensitive)

    def on_density_cbox_changed(self, widget: Gtk.Widget) -> None:
        tree_iter = widget.get_active_iter()

        if tree_iter != None:
            model = widget.get_model()
            name = model[tree_iter][:1]

            self.presenter.density = Density(name[0])

    def on_file_chosen(self, widget):
        filename = widget.get_filename()

        self.presenter.set_image(filename)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename,
                                                         width=MainWindow.IMAGE_WIDTH,
                                                         height=MainWindow.IMAGE_HEIGHT,
                                                 preserve_aspect_ratio=True)
        self.imgv_preview.set_from_pixbuf(pixbuf)

        self.on_scale_button_sensitivity_changed(True)

    def on_dialog_closed(self, widget, response_id):
        self.dialog_image_error.hide()

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

    def show_image_error_dialog(self):
        self.dialog_image_error.run()

    def on_scale_selected_file(self, widget):
        self.presenter.scale_selected_file()
