class MainPresenter:
    def __init__(self, main_view):
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
        print('xxxhdpi toggled: %s' % value)
        self._xxxhdpi = value
        self.main_view.toggle_xxxhdpi(value)

    @property
    def xxhdpi(self):
        return self._xxhdpi

    @xxhdpi.setter
    def xxhdpi(self, value):
        print('xxhdpi toggled: %s' % value)
        self._xxhdpi = value
        self.main_view.toggle_xxhdpi(value)

    @property
    def xhdpi(self):
        return self._xhdpi

    @xhdpi.setter
    def xhdpi(self, value):
        print('xhdpi toggled: %s' % value)
        self._xhdpi = value
        self.main_view.toggle_xhdpi(value)

    @property
    def hdpi(self):
        return self._hdpi

    @hdpi.setter
    def hdpi(self, value):
        print('hdpi toggled: %s' % value)
        self._hdpi = value
        self.main_view.toggle_hdpi(value)

    @property
    def mdpi(self):
        return self._mdpi

    @mdpi.setter
    def mdpi(self, value):
        print('mdpi toggled: %s' % value)
        self._mdpi = value
        self.main_view.toggle_mdpi(value)

    @property
    def ldpi(self):
        return self._ldpi

    @ldpi.setter
    def ldpi(self, value):
        print('ldpi toggled: %s' % value)
        self._ldpi = value
        self.main_view.toggle_ldpi(value)
