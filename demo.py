from lib.changdian import ChangdianAoiInfo
from lib.core.sinf import SinfInfo
import numpy as np

if __name__ == '__main__':
    image_path = 'assets/rodulph/MP2111337A_HJU529-15-G4_UBM_219_2.jpg'
    aoi_info = ChangdianAoiInfo.from_path(image_path)

    print("Product Name:", aoi_info.product)
    print("Initial Location:", aoi_info.location)
    print("Image Resolution (um):", aoi_info.resolution)
    print("Lens Magnification: {:.2f}x".format(aoi_info.mag))
    print('XINDEX, YINDEX: {}, {}'.format(aoi_info.xindex, aoi_info.yindex))
    print()


    #
    # Parse Sinf files
    #
    sinf_path = 'assets/example.sinf'
    sinf_info = SinfInfo.from_sinf_path(sinf_path)

    print("\n")
    print("SetupID:", sinf_info.setup_id)
    print("LotID:", sinf_info.lot_id)
    print("WaferID:", sinf_info.wafer_id)

    print("Bad DIE IDs:")
    print(np.where(sinf_info.label_map > 0))
