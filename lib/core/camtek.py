from .base import AoiInfo
import configparser
import os.path as osp
from pathlib import Path
import numpy as np
import cv2

class CamtekInfo(AoiInfo):
    def __init__(self, aoi_info):
        self.aoi_info = aoi_info

    @property
    def pixel_size(self) -> tuple:
        """ Return the camera resolution in pixel size in xy manner (eg: (0.95, 0.95)) """
        return (self.aoi_info['image_pix_size_col'], self.aoi_info['image_pix_size_row'])

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

        # compute the relative location of the defect in die (die coordinates)
        offset_col = col % die_size_col
        offset_row = row % die_size_row

        # image center location
        image_center_location = (offset_col / die_size_col, offset_row / die_size_row)
        return image_center_location

    @property
    def magnification(self) -> float:
        """
        Lens magnification ratio (eg: 5x, 10x), which is negtively relative to the pixel size.
        Relations of the lens mag and the pixel size differ among different AOI device manufacturers.
        """
        k = 0.93 * 5  # pixel size = 0.93um in mag 5x
        mag = k / np.mean(self.pixel_size)
        return mag

    @property
    def die_size(self) -> str:
        """ Return the die size in pixel, in current pixel resolution, in xy manner (eg: (1092, 2500)) """
        pixel_size_col, pixel_size_row = self.pixel_size
        die_size_col = self.aoi_info['die_size_col'] / pixel_size_col
        die_size_row = self.aoi_info['die_size_row'] / pixel_size_row
        return (die_size_col, die_size_row)

    @property
    def image(self) -> np.ndarray:
        image_path = self.aoi_info['image_path']
        assert osp.exists(image_path)
        return cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

    @property
    def img(self) -> np.ndarray:
        return self.image
    



    @classmethod
    def from_path(cls, image_path):
        return cls.from_image_path(image_path)


    @classmethod
    def from_image_path(cls, image_path):
        assert osp.exists(image_path), 'image_path {} not found'.format(image_path)

        # get ProductInfo
        image_path_instance = Path(image_path)
        file_name = image_path_instance.name
        product_info = str(image_path_instance.with_name('ProductInfo.ini'))
        colorImageGrabingInfo = str(image_path_instance.with_name('ColorImageGrabingInfo.ini'))
        assert osp.exists(product_info), "product_info file {} not found.".format(product_info)
        assert osp.exists(colorImageGrabingInfo), "colorImageGrabingInfo file {} not found.".format(colorImageGrabingInfo)
        ini_parser = configparser.ConfigParser(strict=False)
        ini_parser.read(product_info)

        die_size_col = float(ini_parser.get('Geometric', 'XDieIndex'))
        die_size_row = float(ini_parser.get('Geometric', 'YDieIndex'))

        # get colorImageGrabingInfo
        ini_parser.read(colorImageGrabingInfo)
        image_pix_size_col = None
        image_pix_size_row = None
        if ini_parser.has_option(file_name, 'PixelSizeX'):
            image_pix_size_col = float(ini_parser.get(file_name, 'PixelSizeX'))
            image_pix_size_row = float(ini_parser.get(file_name, 'PixelSizeY'))
            pix_col = int(ini_parser.get(file_name, 'Col'))
            pix_row = int(ini_parser.get(file_name, 'Row'))
            image_size_col = int(ini_parser.get(file_name, 'ImageSizeX'))
            image_size_row = int(ini_parser.get(file_name, 'ImageSizeY'))
        else:
            for sess in ini_parser.sections():
                if sess.endswith(Path(image_path).suffix) and ini_parser.has_option(sess, 'PixelSizeX'):
                    image_pix_size_col = float(ini_parser.get(sess, 'PixelSizeX'))
                    image_pix_size_row = float(ini_parser.get(sess, 'PixelSizeY'))
                    pix_col = int(ini_parser.get(sess, 'Col'))
                    pix_row = int(ini_parser.get(sess, 'Row'))
                    image_size_col = int(ini_parser.get(sess, 'ImageSizeX'))
                    image_size_row = int(ini_parser.get(sess, 'ImageSizeY'))
                    break

        if image_pix_size_col is None or image_pix_size_row is None:
            raise Exception("PixelSizeX({}) and PixelSizeY({}) must be not None.".format(image_pix_size_col, image_pix_size_row))

        # get image offset
        col = float(file_name.split('.')[0])
        row = float(file_name.split('.')[1])

        die_col = round((col - 0.5 * die_size_col) / die_size_col)
        die_row = round((row - 0.5 * die_size_row) / die_size_row)

        aoi_info = dict(
            image_path=image_path, 
            file_name=file_name,
            die_size_col=die_size_col,
            die_size_row=die_size_row,
            image_pix_size_col=image_pix_size_col,
            image_pix_size_row=image_pix_size_row,
            pix_col=pix_col,
            pix_row=pix_row,
            die_col=die_col,
            die_row=die_row,
            image_size_col=image_size_col,
            image_size_row=image_size_row,
            col = col,
            row = row
        )

        return cls(aoi_info)
