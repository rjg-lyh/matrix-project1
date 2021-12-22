from .core.klarf import KlarfInfo

class ChangdianAoiInfo(KlarfInfo):
    @property
    def product_name(self) -> str:
        return self.aoi_info['setup_id']
