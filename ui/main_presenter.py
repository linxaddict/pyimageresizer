from model import Density

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class MainPresenter:

    def __init__(self, main_view):
        self.main_view = main_view

        self._xxxhdpi = False
        self._xxhdpi = False
        self._xhdpi = False
        self._hdpi = False
        self._mdpi = False
        self._ldpi = False

        self._density = Density.xxxhdpi

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
