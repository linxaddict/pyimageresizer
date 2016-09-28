import threading

import gi

gi.require_version('Gtk', '3.0')

# noinspection PyUnresolvedReferences
from gi.repository import GLib

import os

from pyimageresizer.image import ImageProcessor
from pyimageresizer.model import Density

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class MainPresenter:
    def _get_selected_densities(self) -> [Density]:
        densities = []

        if self.xxxhdpi:
            densities.append(Density.xxxhdpi)

        if self.xxhdpi:
            densities.append(Density.xxhdpi)

        if self.xhdpi:
            densities.append(Density.xhdpi)

        if self.hdpi:
            densities.append(Density.hdpi)

        if self.mdpi:
            densities.append(Density.mdpi)

        if self.ldpi:
            densities.append(Density.ldpi)

        return densities

    def _scale(self):
        GLib.idle_add(self.main_view.on_scale_button_sensitivity_changed, False)
        error_occurred = False

        for file in self._loaded_files:
            try:
                for d in self._get_selected_densities():
                    self._image_processor.scale(self.density, d, file, self.override_existing_files)
            except IOError:
                error_occurred = True

        if error_occurred:
            GLib.idle_add(self.main_view.show_image_error_dialog)

        GLib.idle_add(self.main_view.on_scale_button_sensitivity_changed, True)

    def __init__(self, main_view, image_processor: ImageProcessor):
        self.main_view = main_view

        self._xxxhdpi = False
        self._xxhdpi = False
        self._xhdpi = False
        self._hdpi = False
        self._mdpi = False
        self._ldpi = False

        self._override_existing_files = False

        self._density = Density.xxxhdpi
        self._image_processor = image_processor

        self._loaded_files = []

    def get_image_info(self, filename) -> ((int, int), str, str, str):
        size = self._image_processor.image_size(filename)
        name = os.path.basename(filename)
        img_format = self._image_processor.image_format(filename)
        mode = self._image_processor.image_mode(filename)

        img_name, _ = os.path.splitext(name)

        return size, img_name, img_format, mode

    @staticmethod
    def generate_densities() -> [str]:
        d = []

        for density in Density:
            d.append([density.value])

        return d

    @property
    def xxxhdpi(self) -> bool:
        return self._xxxhdpi

    @xxxhdpi.setter
    def xxxhdpi(self, value: bool) -> None:
        self._xxxhdpi = value
        self.main_view.toggle_xxxhdpi(value)

    @property
    def xxhdpi(self) -> bool:
        return self._xxhdpi

    @xxhdpi.setter
    def xxhdpi(self, value: bool) -> None:
        self._xxhdpi = value
        self.main_view.toggle_xxhdpi(value)

    @property
    def xhdpi(self) -> bool:
        return self._xhdpi

    @xhdpi.setter
    def xhdpi(self, value: bool) -> None:
        self._xhdpi = value
        self.main_view.toggle_xhdpi(value)

    @property
    def hdpi(self) -> bool:
        return self._hdpi

    @hdpi.setter
    def hdpi(self, value: bool) -> None:
        self._hdpi = value
        self.main_view.toggle_hdpi(value)

    @property
    def mdpi(self) -> bool:
        return self._mdpi

    @mdpi.setter
    def mdpi(self, value: bool) -> None:
        self._mdpi = value
        self.main_view.toggle_mdpi(value)

    @property
    def ldpi(self) -> bool:
        return self._ldpi

    @ldpi.setter
    def ldpi(self, value: bool) -> None:
        self._ldpi = value
        self.main_view.toggle_ldpi(value)

    @property
    def density(self) -> Density:
        return self._density

    @density.setter
    def density(self, value: Density) -> None:
        self._density = value

    @property
    def override_existing_files(self) -> bool:
        return self._override_existing_files

    @override_existing_files.setter
    def override_existing_files(self, value) -> None:
        self._override_existing_files = value

    @property
    def loaded_files(self) -> [str]:
        return self._loaded_files

    def add_image(self, filename: str) -> bool:
        if filename not in self._loaded_files:
            self._loaded_files.append(filename)

            if len(self._loaded_files) > 1:
                self.main_view.hide_image_placeholder()
                self.main_view.show_images_list()

            self.main_view.on_scale_button_sensitivity_changed(True)
            self.main_view.on_clear_button_sensitivity_changed(True)

            return True

        return False

    def remove_image(self, filename: str) -> None:
        self._loaded_files.remove(filename)

        if len(self._loaded_files) > 1:
            self.main_view.show_image_placeholder()
            self.main_view.hide_images_list()
        elif not self._loaded_files:
            self.main_view.on_clear_button_sensitivity_changed(False)
            self.main_view.on_scale_button_sensitivity_changed(False)

    def scale_selected_files(self) -> None:
        thread = threading.Thread(target=self._scale)
        thread.daemon = True
        thread.start()

    def clear(self):
        self._loaded_files.clear()

        self.main_view.on_clear_button_sensitivity_changed(False)
        self.main_view.on_scale_button_sensitivity_changed(False)
        self.main_view.show_image_placeholder()
        self.main_view.hide_images_list()
        self.main_view.load_default_placeholder()
