import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import Gdk
from gi.repository import GLib
from pyimageresizer.model import Density

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class MainWindow:
    IMAGE_WIDTH = 250
    IMAGE_HEIGHT = 250

    THUMBNAIL_WIDTH = 45
    THUMBNAIL_HEIGHT = 45

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

        self.chbox_override_existing_files = builder.get_object('chbox_override_existing_files')

        self.imgv_preview = builder.get_object('imgv_preview')
        self.btn_scale = builder.get_object('btn_scale')
        self.btn_clear = builder.get_object('btn_clear')

        self.dialog_image_error = builder.get_object('dialog_image_error')

        self.box_image_container = builder.get_object('box_image_container')

        self.treev_model = builder.get_object('images_list_store')
        self.treev_images = builder.get_object('tree_view_images')

        self.overlay = builder.get_object('overlay')
        self.box_main = builder.get_object('box_main')

    @staticmethod
    def _append_densities(list_store: Gtk.ListStore, densities: [str]):
        for density in densities:
            list_store.append(density)

    @staticmethod
    def _parse_uri(uri: str) -> str:
        path = ""

        if uri.startswith('file:\\\\\\'):  # windows
            path = uri[8:]  # 8 is len('file:///')
        elif uri.startswith('file://'):  # nautilus, rox
            path = uri[7:]  # 7 is len('file://')
        elif uri.startswith('file:'):  # xffm
            path = uri[5:]  # 5 is len('file:')

        path = path.strip('\r\n\x00')  # remove \r\n and NULL

        return path

    def _initialize_views_state(self, presenter) -> None:
        self.chbox_xxxhdpi.set_active(presenter.xxxhdpi)
        self.chbox_xxhdpi.set_active(presenter.xxhdpi)
        self.chbox_xhdpi.set_active(presenter.xhdpi)
        self.chbox_hdpi.set_active(presenter.hdpi)
        self.chbox_mdpi.set_active(presenter.mdpi)
        self.chbox_ldpi.set_active(presenter.ldpi)

        self.chbox_override_existing_files.set_active(presenter.override_existing_files)

        self._append_densities(self.density_list_store, presenter.generate_densities())
        self.cbox_density.set_active(0)

    @staticmethod
    def _generate_preview(filename: str) -> GdkPixbuf.Pixbuf:
        return GdkPixbuf.Pixbuf.new_from_file_at_scale(filename, width=MainWindow.IMAGE_WIDTH,
                                                       height=MainWindow.IMAGE_HEIGHT, preserve_aspect_ratio=True)

    @staticmethod
    def _generate_thumbnail(filename: str) -> GdkPixbuf.Pixbuf:
        return GdkPixbuf.Pixbuf.new_from_file_at_scale(filename, width=MainWindow.THUMBNAIL_WIDTH,
                                                       height=MainWindow.THUMBNAIL_HEIGHT, preserve_aspect_ratio=True)

    def _choose_file(self, filename):
        if self.presenter.add_image(filename):
            self.imgv_preview.set_from_pixbuf(self._generate_preview(filename))

            thumbnail = self._generate_thumbnail(filename)
            size, name, img_format, mode = self.presenter.get_image_info(filename)

            self.treev_model.append([thumbnail, name, '%d x %d' % (size[0], size[1]), img_format])

    def __init__(self, view_resource: str, gtk_builder: Gtk.Builder, application: Gtk.Application):
        gtk_builder.add_from_resource(view_resource)
        gtk_builder.connect_signals(self)

        self._find_views(gtk_builder)

        self.box_main.drag_dest_set(Gtk.DestDefaults.ALL,
                                    [Gtk.TargetEntry.new("text/uri-list", 0, 0)], Gdk.DragAction.COPY)

        self.presenter = None
        self.window.set_application(application)

    def set_presenter(self, presenter) -> None:
        self.presenter = presenter
        self._initialize_views_state(presenter)

    def show(self) -> None:
        self.window.present()

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

    def on_clear_button_sensitivity_changed(self, sensitive: bool) -> None:
        self.btn_clear.set_sensitive(sensitive)

    def on_density_cbox_changed(self, widget: Gtk.Widget) -> None:
        tree_iter = widget.get_active_iter()

        if tree_iter is not None:
            model = widget.get_model()
            name = model[tree_iter][:1]

            self.presenter.density = Density(name[0])

    def on_override_existing_files_toggled(self, widget: Gtk.Widget) -> None:
        if self.presenter.override_existing_files != widget.get_active():
            self.presenter.override_existing_files = widget.get_active()

    def on_file_chosen(self, widget):
        filename = widget.get_filename()
        self._choose_file(filename)

    # noinspection PyUnusedLocal
    def on_dialog_closed(self, widget, response_id):
        self.dialog_image_error.hide()

    # noinspection PyUnusedLocal
    def on_drag_data_received(self, widget, context, x, y, selection, target_type, timestamp):
        data = selection.get_data().decode('UTF-8')

        try:
            for uri in data.split('\n'):
                if uri.strip():
                    path = self._parse_uri(uri)
                    self._choose_file(path)
        except GLib.Error:
            self.show_image_error_dialog()

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

    # noinspection PyUnusedLocal
    def on_scale_selected_file(self, widget):
        self.presenter.scale_selected_files()

    def on_clear(self, widget):
        self.treev_model.clear()
        self.presenter.clear()

    def show_image_placeholder(self):
        self.imgv_preview.set_visible(True)

    def hide_image_placeholder(self):
        self.imgv_preview.set_visible(False)

    def show_images_list(self):
        self.treev_images.set_visible(True)

    def hide_images_list(self):
        self.treev_images.set_visible(False)

    def load_default_placeholder(self):
        self.imgv_preview.set_from_file('res/img/ic_image.png')
