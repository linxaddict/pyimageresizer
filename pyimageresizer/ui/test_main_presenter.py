import unittest
from unittest.mock import call, Mock

import gi
from image import ImageProcessor

from pyimageresizer.model import Density
from pyimageresizer.ui import MainPresenter
from pyimageresizer.ui import MainWindow

gi.require_version('Gtk', '3.0')

# noinspection PyUnresolvedReferences
from gi.repository import GLib


class MainPresenterTest(unittest.TestCase):
    def setUp(self):
        self.mock_window = Mock(spec=MainWindow)
        self.mock_image_processor = Mock(spec=ImageProcessor)

        # noinspection PyTypeChecker
        self.main_presenter = MainPresenter(self.mock_window, self.mock_image_processor)

    def test_get_selected_densities_xxxhdpi(self):
        self.main_presenter.xxxhdpi = True
        densities = self.main_presenter._get_selected_densities()

        self.assertIn(Density.xxxhdpi, densities)
        self.assertEqual(1, len(densities))

    def test_get_selected_densities_xxhdpi(self):
        self.main_presenter.xxhdpi = True
        densities = self.main_presenter._get_selected_densities()

        self.assertIn(Density.xxhdpi, densities)
        self.assertEqual(1, len(densities))

    def test_get_selected_densities_xhdpi(self):
        self.main_presenter.xhdpi = True
        densities = self.main_presenter._get_selected_densities()

        self.assertIn(Density.xhdpi, densities)
        self.assertEqual(1, len(densities))

    def test_get_selected_densities_hdpi(self):
        self.main_presenter.hdpi = True
        densities = self.main_presenter._get_selected_densities()

        self.assertIn(Density.hdpi, densities)
        self.assertEqual(1, len(densities))

    def test_get_selected_densities_mdpi(self):
        self.main_presenter.mdpi = True
        densities = self.main_presenter._get_selected_densities()

        self.assertIn(Density.mdpi, densities)
        self.assertEqual(1, len(densities))

    def test_get_selected_densities_ldpi(self):
        self.main_presenter.ldpi = True
        densities = self.main_presenter._get_selected_densities()

        self.assertIn(Density.ldpi, densities)
        self.assertEqual(1, len(densities))

    def test_get_selected_densities(self):
        self.main_presenter.xxxhdpi = True
        self.main_presenter.xxhdpi = True
        self.main_presenter.xhdpi = True
        self.main_presenter.hdpi = True
        self.main_presenter.mdpi = True
        self.main_presenter.ldpi = True

        densities = self.main_presenter._get_selected_densities()

        self.assertIn(Density.xxxhdpi, densities)
        self.assertIn(Density.xxhdpi, densities)
        self.assertIn(Density.xhdpi, densities)
        self.assertIn(Density.hdpi, densities)
        self.assertIn(Density.mdpi, densities)
        self.assertIn(Density.ldpi, densities)

    def test_scale(self):
        GLib.idle_add = Mock()

        self.main_presenter.loaded_files.append('test_file.png')
        self.main_presenter.xxxhdpi = True
        self.main_presenter.hdpi = True
        self.main_presenter.density = Density.xxxhdpi

        self.main_presenter._scale()

        glib_calls = [
            call(self.mock_window.on_scale_button_sensitivity_changed, False),
            call(self.mock_window.on_scale_button_sensitivity_changed, True)
        ]

        GLib.idle_add.assert_has_calls(glib_calls)

        calls = [
            call(Density.xxxhdpi, Density.xxxhdpi, 'test_file.png', self.main_presenter.override_existing_files),
            call(Density.xxxhdpi, Density.hdpi, 'test_file.png', self.main_presenter.override_existing_files)
        ]
        self.mock_image_processor.scale.assert_has_calls(calls)

    def test_scale_ioerror(self):
        GLib.idle_add = Mock()

        self.mock_image_processor.scale = Mock(side_effect=IOError('test'))

        self.main_presenter._loaded_files.append('test_file.png')
        self.main_presenter.xxxhdpi = True
        self.main_presenter.density = Density.xxxhdpi

        self.main_presenter._scale()

        glib_calls = [
            call(self.mock_window.on_scale_button_sensitivity_changed, False),
            call(self.mock_window.show_image_error_dialog),
            call(self.mock_window.on_scale_button_sensitivity_changed, True)
        ]

        GLib.idle_add.assert_has_calls(glib_calls)

    def test_get_image_info(self):
        self.mock_image_processor.image_size = Mock(side_effect=[(10, 10)])
        self.mock_image_processor.image_format = Mock(side_effect=['png'])
        self.mock_image_processor.image_mode = Mock(side_effect=['argb'])

        size, img_name, img_format, mode = self.main_presenter.get_image_info('test_file.png')

        self.assertEqual((10, 10), size)
        self.assertEqual('test_file', img_name)
        self.assertEqual('png', img_format)
        self.assertEqual('argb', mode)

    def test_generate_densities(self):
        densities = self.main_presenter.generate_densities()
        expected = [['xxxhdpi'], ['xxhdpi'], ['xhdpi'], ['hdpi'], ['mdpi'], ['ldpi']]

        self.assertTrue(all(d in densities for d in expected))

    def test_xxxhdpi(self):
        self.main_presenter.xxxhdpi = True
        self.assertTrue(self.main_presenter.xxxhdpi)

        self.main_presenter.xxxhdpi = False
        self.assertFalse(self.main_presenter.xxxhdpi)

    def test_xxhdpi(self):
        self.main_presenter.xxhdpi = True
        self.assertTrue(self.main_presenter.xxhdpi)

        self.main_presenter.xxhdpi = False
        self.assertFalse(self.main_presenter.xxhdpi)

    def test_xhdpi(self):
        self.main_presenter.xhdpi = True
        self.assertTrue(self.main_presenter.xhdpi)

        self.main_presenter.xhdpi = False
        self.assertFalse(self.main_presenter.xhdpi)

    def test_hdpi(self):
        self.main_presenter.hdpi = True
        self.assertTrue(self.main_presenter.hdpi)

        self.main_presenter.hdpi = False
        self.assertFalse(self.main_presenter.hdpi)

    def test_mdpi(self):
        self.main_presenter.mdpi = True
        self.assertTrue(self.main_presenter.mdpi)

        self.main_presenter.mdpi = False
        self.assertFalse(self.main_presenter.mdpi)

    def test_ldpi(self):
        self.main_presenter.ldpi = True
        self.assertTrue(self.main_presenter.ldpi)

        self.main_presenter.ldpi = False
        self.assertFalse(self.main_presenter.ldpi)

    def test_density(self):
        self.main_presenter.density = Density.xxxhdpi
        self.assertEqual(Density.xxxhdpi, self.main_presenter.density)

        self.main_presenter.density = Density.hdpi
        self.assertEqual(Density.hdpi, self.main_presenter.density)

    def test_override_existing_files(self):
        self.main_presenter.override_existing_files = True
        self.assertTrue(self.main_presenter.override_existing_files)

        self.main_presenter.override_existing_files = False
        self.assertFalse(self.main_presenter.override_existing_files)

    def test_add_image(self):
        filename = 'test_filename.png'
        result = self.main_presenter.add_image(filename)

        self.assertIn(filename, self.main_presenter.loaded_files)
        self.mock_window.on_scale_button_sensitivity_changed.assert_called_once_with(True)
        self.mock_window.on_clear_button_sensitivity_changed.assert_called_once_with(True)

        self.assertTrue(result)

    def test_add_image_two_files(self):
        filename = 'test_filename.png'
        self.main_presenter.loaded_files.append(filename)

        filename2 = 'test2_filename.png'
        result = self.main_presenter.add_image(filename2)

        self.assertIn(filename, self.main_presenter.loaded_files)
        self.assertIn(filename2, self.main_presenter.loaded_files)

        self.mock_window.hide_image_placeholder.assert_called_once_with()
        self.mock_window.show_images_list.assert_called_once_with()

        self.mock_window.on_scale_button_sensitivity_changed.assert_called_once_with(True)
        self.mock_window.on_clear_button_sensitivity_changed.assert_called_once_with(True)

        self.assertTrue(result)

    def test_add_image_already_added(self):
        filename = 'test_filename.png'
        self.main_presenter.loaded_files.append(filename)

        result = self.main_presenter.add_image(filename)

        self.assertEqual(1, len(self.main_presenter.loaded_files))
        self.assertFalse(result)

    def test_remove_image(self):
        filename = 'test_filename.png'
        self.main_presenter.loaded_files.append(filename)

        self.main_presenter.remove_image(filename)

        self.assertEqual(0, len(self.main_presenter.loaded_files))
        self.mock_window.on_scale_button_sensitivity_changed.assert_called_once_with(False)
        self.mock_window.on_clear_button_sensitivity_changed.assert_called_once_with(False)

    def test_remove_image_list_not_empty_after_remove(self):
        filename = 'test_filename.png'
        filename2 = 'test_filename2.png'
        filename3 = 'test_filename3.png'

        self.main_presenter.loaded_files.extend([filename, filename2, filename3])

        self.main_presenter.remove_image(filename)

        self.assertIn(filename2, self.main_presenter.loaded_files)
        self.assertIn(filename3, self.main_presenter.loaded_files)

        self.mock_window.show_image_placeholder.assert_called_once_with()
        self.mock_window.hide_images_list.assert_called_once_with()

    def test_clear(self):
        filename = 'test_filename.png'
        filename2 = 'test_filename2.png'
        filename3 = 'test_filename3.png'

        self.main_presenter.loaded_files.extend([filename, filename2, filename3])

        self.main_presenter.clear()

        self.assertEqual(0, len(self.main_presenter.loaded_files))

        self.mock_window.on_scale_button_sensitivity_changed.assert_called_once_with(False)
        self.mock_window.on_clear_button_sensitivity_changed.assert_called_once_with(False)
        self.mock_window.show_image_placeholder.assert_called_once_with()
        self.mock_window.hide_images_list.assert_called_once_with()
        self.mock_window.load_default_placeholder.assert_called_once_with()

