import os

from model import Density
from image import ImageProcessor

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

    def _generate_image_info(self, filename) -> str:
        size = self._image_processor.image_size(filename)
        img_format = self._image_processor.image_format(filename)
        mode = self._image_processor.image_mode(filename)

        return '%d x %d, %s, %s' % (size[0], size[1], img_format, mode)

    def __init__(self, main_view, image_processor: ImageProcessor):
        self.main_view = main_view

        self._xxxhdpi = False
        self._xxhdpi = False
        self._xhdpi = False
        self._hdpi = False
        self._mdpi = False
        self._ldpi = False

        self._density = Density.xxxhdpi

        self._image_processor = image_processor

    def generate_densities(self) -> [str]:
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

    def set_image(self, filename: str) -> None:
        self.file_name = filename
        self.main_view.set_filename(os.path.basename(filename))
        self.main_view.set_image_info(self._generate_image_info(filename))

    def scale_selected_file(self) -> None:
        if self.file_name:
            try:
                for d in self._get_selected_densities():
                    self._image_processor.scale(self.density, d, self.file_name)
            except IOError:
                self.main_view.show_image_error_dialog()
