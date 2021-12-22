from .base import AoiInfo
from .utils import parse_klarf
import os
from pathlib import Path
import numpy as np
import glob

class KlarfInfo(AoiInfo):
    def __init__(self, aoi_info):
        self.aoi_info = aoi_info

    @property
    def pixel_size(self) -> tuple:
        """ Return the camera resolution in pixel size in xy manner (eg: (0.95, 0.95)) """
        return (.95, .95)

    @property
    def location_in_die(self) -> tuple:
        """
        Return the location of the image center relative to a die, whose top-left corner as the origin (0, 0).
        The location is normalized by the die size (eg: (0.664, 0.23)).
        """
        # die size in pixel (wafer coordinates)
        die_size_col = self.aoi_info['die_size_col']
        die_size_row = self.aoi_info['die_size_row']
        # defect location (usually the image center in Camtek settings) in pixel (wafer coordinates)
        col = self.aoi_info['col']
        row = self.aoi_info['row']

        # image center location
        image_center_location = (col / die_size_col, 1. - row / die_size_row)
        return image_center_location

    @property
    def magnification(self) -> float:
        """
        Lens magnification ratio (eg: 5x, 10x), which is negtively relative to the pixel size.
        Relations of the lens mag and the pixel size differ among different AOI device manufacturers.
        """
        k = 0.9 * 10  # pixel size = 0.9um in mag 10x
        mag = k / np.mean(self.pixel_size)
        return mag

    @property
    def die_size(self) -> str:
        """ Return the die size in pixel, in current pixel resolution, in xy manner (eg: (1092, 2500)) """
        die_size_col = self.aoi_info['die_size_col']
        die_size_row = self.aoi_info['die_size_row']
        return (die_size_col, die_size_row)



    @classmethod
    def from_path(cls, image_path):
        return cls.from_image_path(image_path)


    @classmethod
    def from_image_path(cls, image_path):
        assert os.path.exists(image_path), 'image_path {} not found'.format(image_path)

        # get ProductInfo
        image_path_instance = Path(image_path)
        file_name = image_path_instance.name

        image_dir = os.path.dirname(image_path)
        klarf_files = glob.glob(os.path.join(image_dir, '*.klarf'))
        assert len(klarf_files) == 1, "Find 0 or more than one klarf files in folder: {}".format(image_dir)

        klarf_info = parse_klarf(klarf_files[0])
        df = klarf_info['defects']
        img_info = df[df['IMAGENAME'] == file_name]
        assert len(img_info) == 1, "Find 0 or more than one record about file: {}".format(image_path)
        die_size_col, die_size_row = klarf_info['die_size_xy']

        aoi_info = dict(
            image_path=image_path, 
            file_name=file_name,
            setup_id=klarf_info['setup_id'],
            die_size_col=die_size_col,
            die_size_row=die_size_row,
            col=float(img_info['XINDEX']),
            row=float(img_info['YINDEX'])
        )

        return cls(aoi_info)
