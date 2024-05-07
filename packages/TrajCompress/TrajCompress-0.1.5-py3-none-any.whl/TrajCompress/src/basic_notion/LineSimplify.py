# import DistFunc
from .Point import Point
import os.path


class LineSimplify:
    def __init__(self):
        self._trace = []

    def add_point(self, x: float, y: float, t: float = None, convert=True):
        """
        :param x: horizontal coordinate, e.g., lon
        :param y: vertical coordinate, e.g., lat
        :param t: time stamp
        :param convert: convert lat-lon to x-y-z Cartesian coordinate system -- needed if calculate distance later
        """
        p = Point(x, y, t)

        if convert:
            p.latlon2cartesian()

        self._trace.append(p)

    def bunch_add_points(self, xs: list, ys: list, ts: list = None, convert=True):
        """
        :param xs: a list of horizontal coordinates, e.g., lon
        :param ys: a list of vertical coordinates, e.g., lat
        :param ts: a list of time stamps
        :param convert: convert lat-lon to x-y-z Cartesian coordinate system -- needed if calculate distance later
        """
        if ts is None:
            ts = [None] * len(xs)

        if min([len(xs), len(ys), len(ts)]) == 0:
            print("Please check the inputs -- some of them is empty")
            exit()

        len_input = len(xs)

        if any(len_input != len(input_l) for input_l in [ys, ts]):
            print("Please check the inputs -- some of them has different length")
            exit()

        for idx in range(len_input):
            p = Point(xs[idx], ys[idx], ts[idx])

            if convert:
                p.latlon2cartesian()

            self._trace.append(p)

    def load_from_txt(self, filepath, time_include=False,delimter=","):
        if not os.path.exists(filepath):
            print("Please check if file exists AT ", filepath)
            exit()

        with open(filepath, "r") as rf:
            lines = rf.readlines()

            for line in lines:
                line = line.rstrip()
                if line and line[0] != '#':
                    if time_include:
                        lat, lon, ts = line.split(delimter)
                        self.add_point(float(lon), float(lat), float(ts))
                    else:
                        lat, lon = line.split(delimter)
                        self.add_point(float(lon), float(lat))

    def get_trace(self):
        return self._trace

    def DouglasPeuckerAlgorithm(self):
        """
        Some Simplification Algorithm
        :return:
        """
        ### NEED TO BE FILLED ###
        pass




