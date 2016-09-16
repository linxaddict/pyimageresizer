class MainPresenter:
    def __init__(main_view):
        self.main_view = main_view

        self._xxxhdpi = False
        self._xxhdpi = False
        self._xhdpi = False
        self._hdpi = False
        self._mdpi = False
        self._ldpi = False

    @property
    def xxxhdpi(self):
        return self._xxxhdpi

    @xxxhdpi.setter
    def xxxhdpi(self, value):
        self._xxxhdpi = value

    @property
    def xxhdpi(self):
        return self._xxhdpi

    @xxhdpi.setter
    def xxhdpi(self, value):
        self._xxhdpi = value

    @property
    def xhdpi(self):
        return self._xhdpi

    @xhdpi.setter
    def xhdpi(self, value):
        self._xhdpi = value

    @property
    def hdpi(self):
        return self.hdpi

    @hdpi.setter
    def hdpi(self, value):
        self._hdpi = value

    @property
    def mdpi(self):
        return self._mdpi

    @mdpi.setter
    def mdpi(self, value):
        self._mdpi = value

    @property
    def ldpi(self):
        return self._ldpi

    @ldpi.setter
    def ldpi(self, value):
        self._ldpi = value
