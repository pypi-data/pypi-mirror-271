import math


class Point:
    def __init__(self, x:  float, y:  float, t:  float = None):
        """
        :param x: horizontal coordinate, e.g., lon
        :param y: vertical coordinate, e.g., lat
        :param t: time stamp
        """
        self._x = x
        self._y = y
        self._t = t
        self._cx = None
        self._cy = None
        self._cz = None

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_time(self) -> float:
        return self._t

    def get_cx(self) -> float:
        return self._cx

    def get_cy(self) -> float:
        return self._cy

    def get_cz(self) -> float:
        return self._cz

    def latlon2cartesian(self):
        """
        !! Only needed if self._x and self._y are lon and lat
        Convert lat-lon to x-y-z Cartesian coordinate system for distance computation
        Ref; https://en.wikipedia.org/wiki/Earth-centered,_Earth-fixed_coordinate_system
        """
        earth_r = 6371010  # unit: meter
        degree2radian = math.pi / 180  # Input lat/lon is decimal degree, while cos/sin requires radian

        self._cx = earth_r * math.cos(self._y * degree2radian) * math.cos(self._x * degree2radian)
        self._cy = earth_r * math.cos(self._y * degree2radian) * math.sin(self._x * degree2radian)
        self._cz = earth_r * math.sin(self._y * degree2radian)