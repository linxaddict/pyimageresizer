import os

from model import Density
from PIL import Image

class ImageProcessor:
    DRAWABLE_XXXHDPI = 'drawable-xxxhdpi'
    DRAWABLE_XXHDPI = 'drawable-xxhdpi'
    DRAWABLE_XHDPI = 'drawable-xhdpi'
    DRAWABLE_HDPI = 'drawable-hdpi'
    DRAWABLE_MDPI = 'drawable-mdpi'
    DRAWABLE_LDPI = 'drawable-ldpi'

    def _create_dir(self, dir_name: str):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    def _generate_out_path(self, filename:str, density: Density) -> str:
        dirname = os.path.dirname(filename)
        drawable_dir = self._density_to_dir_map[density]
        basename = os.path.basename(filename)

        out_path = os.path.join(dirname, drawable_dir)
        out_path = os.path.join(out_path, basename)

        return out_path

    def __init__(self):
        self._density_to_dir_map = {
            Density.xxxhdpi: ImageProcessor.DRAWABLE_XXXHDPI,
            Density.xxhdpi: ImageProcessor.DRAWABLE_XXHDPI,
            Density.xhdpi: ImageProcessor.DRAWABLE_XHDPI,
            Density.hdpi: ImageProcessor.DRAWABLE_HDPI,
            Density.mdpi: ImageProcessor.DRAWABLE_MDPI,
            Density.ldpi: ImageProcessor.DRAWABLE_LDPI
        }

        self._density_to_multiplier_map = {
            Density.xxxhdpi: 4.0,
            Density.xxhdpi: 3.0,
            Density.xhdpi: 2.0,
            Density.hdpi: 1.5,
            Density.mdpi: 1.0,
            Density.ldpi: 0.75
        }

    def scale(self, in_density: Density, out_density: Density, filename: str) -> str:
        out_path = self._generate_out_path(filename, out_density)
        drawable_dir = os.path.dirname(out_path)
        self._create_dir(drawable_dir)

        image = Image.open(filename)
        size = image.size

        in_density_multiplier = self._density_to_multiplier_map[in_density]
        out_density_multiplier = self._density_to_multiplier_map[out_density]

        multiplier = out_density_multiplier / in_density_multiplier

        width = (int) (size[0] * multiplier)
        height = (int) (size[1] * multiplier)

        out_image = image.resize((width, height), Image.BICUBIC)
        out_image.save(out_path)

        return out_path

    def image_size(self, filename: str) -> (int, int):
        image = Image.open(filename)
        return image.size

    def image_format(self, filename: str) -> str:
        image = Image.open(filename)
        return image.format

    def image_mode(self, filename: str) -> str:
        image = Image.open(filename)
        return image.mode
