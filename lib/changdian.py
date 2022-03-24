from .core.klarf import KlarfInfo
import numpy as np

class ChangdianAoiInfo(KlarfInfo):
    @property
    def product_name(self) -> str:
        setup_id = self.aoi_info['setup_id']
        device_id = self.aoi_info['device_id']
        if setup_id.endswith('-'+device_id):
            return setup_id
        else:
            return setup_id + '-' + device_id

    @property
    def pixel_size(self) -> tuple:
        """ Return the camera resolution in pixel size in xy manner (eg: (0.95, 0.95)) """
        # Estimated pixel size of images, assuming the golden image has mag x3 (which in rodulph's case also means pixel_size = 3)
        template2pixelsize = {
            'GF-GST9414R12-UBM': 3.,
            'JM-LA5211STAA-UBM': 3.,
            'MH-XA39AD21B(301)-UBM': 3,
            'MPS-MX3067R22-M1': 3.,
            'MPS-MX3067R22-UBM': 3.,
            'MPS-SM3035AR30-UBM': 3.,
            'MPS-ST2769R19-UBM': 3.,
            'MPS-ST3031R1-UBM': 3.,
            'MPS-ST3405ZR5-M1': 3.,
            'MPS-ST3405ZR5-UBM': 3.,
            'MPS-ST3099R5-UBM': 3.,
            'MPS-ST3620R11-UBM': 3.,
            'MPS-ST9389ZR14-UBM': 3.,
            'MPS-ST9410R9-UBM': 3.,
            'MPS-ST9410R9-M1': 3.,
            'MPS-ST9413R28-UBM': 3.,
            'MPS-ST9414R12-UBM': 3.,
            'MPS-ST9430R18-M1': 3.,
            'MPS-ST9430R18-UBM': 3.,
            'TI-CD3701C0AYCUR(MHC0AECP)-M1': 1.5,
            'TI-CD3722A2YCUR-UBM': 3.,
            'TI-CD3701C0AYCUR(RFC0AECP)-BALLDROP': 3.,
            'TI-CD3701C0AYCUR(MHC0AECP)-BALLDROP': 3.,
            'TI-CD3722A2YCUR-BALLDROP': 3.,

            ## mixed with DF
            'MPS-SM3519ZR8-UBM': 3.,
            'MPS-ST3222ZR6-UBM': 3.,

            ## small die (processing needed)
            'DA-DW9714P-UBM': 3.,
            'IS-9764AM1B-GT9764BA-CLI(BL301)-UBM': 3.,
            'IS-9764AM1B-GT9764BAS-CLI(BL301)-UBM': 3.,
            'IS-9764AM1D-GT9764BE-CLI(BL301)-UBM': 3.,
            'ON-CAT24C08C4ATR(R8)-M1': 1.175,
            'ON-CP74-001-SWF(HD4100)-UBM': 1.52,
            
            # 2022.2.22
            'GF-GST9414R12-M1': 3.,
            'IF-M4867D(802-FULL)-BALLDROP2': 3.,
        }

        assert self.product in template2pixelsize, "No pixel size record found: ".format(self.product)
        pixel_size = template2pixelsize[self.product]

        if isinstance(pixel_size, (tuple, list)):
            return tuple(pixel_size)
        else:
            return (pixel_size, pixel_size)

    @property
    def magnification(self) -> float:
        """
        Lens magnification ratio (eg: 5x, 10x), which is negtively relative to the pixel size.
        Relations of the lens mag and the pixel size differ among different AOI device manufacturers.
        """
        k = 1.5 * 10
        mag = k / np.mean(self.pixel_size)
        return mag