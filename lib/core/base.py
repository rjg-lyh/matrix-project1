class AoiInfo(object):
    @property
    def product_name(self) -> str:
        """ Return the product name (eg: '8-X68E42B-FI23') """
        raise NotImplementedError

    @property
    def pixel_size(self) -> tuple:
        """ Return the camera resolution in pixel size in xy manner (eg: (0.95, 0.95)) """
        raise NotImplementedError

    @property
    def location_in_die(self) -> tuple:
        """
        Return the location of the image center relative to a die, whose top-left corner as the origin (0, 0).
        The location is normalized by the die size (eg: (0.664, 0.23)).
        """
        raise NotImplementedError
        
    @property
    def magnification(self) -> float:
        """
        Lens magnification ratio (eg: 5x, 10x), which is negtively relative to the pixel size.
        Relations of the lens mag and the pixel size differ among different AOI device manufacturers.
        """
        raise NotImplementedError



    ## Alias
    @property
    def product(self):
        return self.product_name

    @property
    def image_resolution(self):
        return self.pixel_size

    @property
    def image_pixel_size(self):
        return self.pixel_size

    @property
    def resolution(self):
        return self.pixel_size

    @property
    def location(self):
        return self.location_in_die

    @property
    def image_center_location(self):
        return self.location_in_die

    @property
    def image_location(self):
        return self.location_in_die

    @property
    def initial_location(self):
        return self.location_in_die

    @property
    def mag(self):
        return self.magnification

    @property
    def lens_mag(self):
        return self.magnification

    @property
    def lens_magnification(self):
        return self.magnification