from lib.huatian import HuatianAoiInfo

if __name__ == '__main__':
    image_path = 'assets/camtek/8-X680F5B-FI23/100977.92500.c.jpeg'
    aoi_info = HuatianAoiInfo.from_path(image_path)

    print("Product Name:", aoi_info.product)
    print("Initial Location:", aoi_info.location)
    print("Image Resolution (um):", aoi_info.resolution)
