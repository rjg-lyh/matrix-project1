from .core.camtek import CamtekInfo
import re
import configparser
import os.path as osp
from pathlib import Path

class SananAoiInfo(CamtekInfo):
    @property
    def product_name(self) -> str:
        """ Return the product name (eg: '8-X68E42B-FI23') """
        assert 'image_path' in self.aoi_info
        product_name = self.get_product_name_from_image_path(self.aoi_info['image_path'])
        return product_name

    @staticmethod
    def get_product_name_from_image_path(image_path: str):
        PRODUCT_NAME_PATTERN = r'[A-Z]{1}\w+\d+'
        product_names = re.findall(PRODUCT_NAME_PATTERN, image_path)
        product_names = set(x for x in product_names)
        if len(product_names) == 1:
            return product_names.pop()
        else:
            raise RuntimeError("Can not find a product name for path: {}".format(image_path))

    @property
    def magnification(self) -> float:
        """
        Lens magnification ratio (eg: 5x, 10x), which is negtively relative to the pixel size.
        Relations of the lens mag and the pixel size differ among different AOI device manufacturers.
        """
        return self.aoi_info['magnification']


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

        ## suggested by du yanwei 
        # die_size_col = float(ini_parser.get('Geometric', 'CustomerDiePitch_X'))
        # die_size_row = float(ini_parser.get('Geometric', 'CustomerDiePitch_Y'))

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
            col = float(ini_parser.get(file_name, 'X'))
            row = float(ini_parser.get(file_name, 'Y'))
            magnification = float(ini_parser.get(file_name, 'Mag'))
        else:
            for sess in ini_parser.sections():
                if sess.endswith(Path(image_path).suffix) and ini_parser.has_option(sess, 'PixelSizeX'):
                    image_pix_size_col = float(ini_parser.get(sess, 'PixelSizeX'))
                    image_pix_size_row = float(ini_parser.get(sess, 'PixelSizeY'))
                    pix_col = int(ini_parser.get(sess, 'Col'))
                    pix_row = int(ini_parser.get(sess, 'Row'))
                    image_size_col = int(ini_parser.get(sess, 'ImageSizeX'))
                    image_size_row = int(ini_parser.get(sess, 'ImageSizeY'))
                    magnification = float(ini_parser.get(file_name, 'Mag'))
                    break
            # get image offset
            col = float(file_name.split('.')[0])
            row = float(file_name.split('.')[1])

        if image_pix_size_col is None or image_pix_size_row is None:
            raise Exception("PixelSizeX({}) and PixelSizeY({}) must be not None.".format(image_pix_size_col, image_pix_size_row))

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
            row = row,
            magnification = magnification
        )

        return cls(aoi_info)
