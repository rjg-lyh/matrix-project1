from .core.camtek import CamtekInfo
import re

class HuatianAoiInfo(CamtekInfo):
    @property
    def product_name(self) -> str:
        """ Return the product name (eg: '8-X68E42B-FI23') """
        assert 'image_path' in self.aoi_info
        product_name = self.get_product_name_from_image_path(self.aoi_info['image_path'])
        return product_name

    @staticmethod
    def get_product_name_from_image_path(image_path: str):
        PRODUCT_NAME_PATTERN = r'\d{0,1}\d{1}-[A-Z]{1}\w+-[A-Z]+\d+'
        product_names = re.findall(PRODUCT_NAME_PATTERN, image_path)
        product_names = set(x for x in product_names)
        if len(product_names) == 1:
            return product_names.pop()
        else:
            raise RuntimeError("Can not find a product name for path: {}".format(image_path))


    @property
    def location_in_die(self) -> tuple:
        """
        Return the location of the image center relative to a die, whose top-left corner as the origin (0, 0).
        The location is normalized by the die size (eg: (0.664, 0.23)).
        """
        # check if there're conflicts between different location computation
        die_col = self.aoi_info['die_col']
        die_row = self.aoi_info['die_row']
        pix_col = self.aoi_info['pix_col']
        pix_row = self.aoi_info['pix_row']

        if die_col != pix_col or die_row != pix_row:
            raise RuntimeError("die_col: {} == pix_col: {} and die_row: {} == pix_row: {} asserts error".format(die_col, pix_col, die_row, pix_row))

        return super(HuatianAoiInfo, self).location_in_die
