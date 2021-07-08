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
