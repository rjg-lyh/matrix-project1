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
            'TI-CD3701C0AYCUR(MHC0AECP)-BALLDROP': 3.,
            'TI-CD3701C0AYCUR(MHC0AECP)-UBM': 6.,
            
            'TI-CD3701C0AYCUR(RFC0AECP)-BALLDROP': 3.,
            'TI-CD3701C0AYCUR(RFC0AECP)-M1': 3.,
            'TI-CD3701C0AYCUR(RFC0AECP)-UBM': 3.,
            
            'TI-CD3722A2YCUR-BALLDROP': 3.,
            'TI-CD3722A2YCUR-M1':3.,
            'TI-CD3722A2YCUR-UBM': 3.,

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

            # 2022.6.15
            'TI-G4LP5907AM2925-WP2-UBM': 2.972972972972973,
            'TI-G4LP5918A0-WP2(8K)-UBM': 2.972972972972973,
            'JM-LA5314TAA-M1': 2.972972972972973,
            'GF-GH3692R3-UBM': 2.972972972972973,
            'MPS-ST2997R8-UBM': 2.972972972972973,
            'MPS-ST2812ZR7-M1': 3.009009009009009,
            'MPS-ST3241R6-UBM': 2.981981981981982,
            'MPS-ST3565ZR3-UBM': 2.981981981981982,
            'MPS-ST9387R30-UBM': 2.963963963963964,
            'MPS-ST3251ZR5-M1': 2.990990990990991,
            'TI-LTPS564208A1(B2)-UBM': 2.981981981981982,
            'MPS-ST3555R1-UBM': 2.963963963963964,
            'MPS-ST9342R24-M1': 2.972972972972973,
            'MPS-ST9418R9-UBM': 3.009009009009009,
            'MPS-ST3257ZR8-UBM': 2.981981981981982,
            'MPS-ST3127R2-UBM': 2.981981981981982,
            'MPS-ST9419R26-M1': 2.990990990990991,
            'TI-G45907AMKG2825-WP2-UBM': 2.981981981981982,
            'TI-LTPS54202A2(B2)-UBM': 2.990990990990991,
            'MPS-ST9502R15-UBM': 2.990990990990991,
            'MPS-ST9502R15-M1': 2.954954954954955,
            'MPS-ST3475ZR4-UBM': 3.0,
            'TI-G4LP5918A0-WP2(8K)-INCOMING': 1.5045045045045045,
            'GF-GMX3222ZR7-UBM': 2.963963963963964,

            # 22.6.16
            'TI-G2TPS54J060A1-WUP(B2)-M1': 2.991,
            'TI-G2TPS6280YA1(BUMP)-UBM': 2.982,
            'JM-LA5314TAA-UBM': 3.045,
            'TI-G2TMCS1100AB-UBM': 2.955,
            'TI-87C7037CSPB0HT-WP2(B2N)-UBM': 3,
            'TI-G2TPS563202B0(B2)-UBM': 2.982,
            'TI-G2TPS61280AXA2(CA)-M1': 2.991,
            'TI-G2LV62569NAA12(B2)': 2.982,
            'TI-G2TPS61280AXA2(CA)-UBM': 2.982,
            'TI-G2AFE4500SA1-WUP-M1': 2.982,
            'TI-NTPS56C230A1-WUP-M1': 3.009,
            'TI-G2TPS61023A0(B2)-M1': 2.991,
            'ON-CP74-001-SWF(HD4100)-M2': 1.505,
            'TX-A20S-M12': 1.486,
            'TX-A20S-UBM-UBM2': 2.982,
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