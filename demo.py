from lib.changdian import ChangdianAoiInfo

if __name__ == '__main__':
    image_path = 'assets/rodulph/MP2111337A_HJU529-15-G4_UBM_219_2.jpg'
    aoi_info = ChangdianAoiInfo.from_path(image_path)

    print("Product Name:", aoi_info.product)
    print("Initial Location:", aoi_info.location)
    print("Image Resolution (um):", aoi_info.resolution)
    print("Lens Magnification: {:.2f}x".format(aoi_info.mag))
