from .graph import *


class Map:
    # bounds defined in cartesian from top-left -> bottom-right
    # default map is for SF region, as defined on OSM by ID R111968
    def __init__(self, graph, bounds=None):
        self.graph: Graph = graph

        self.bounds = bounds
        self.points = []

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__ = state

    def add_points(self, point):
        self.addPoints([point])

    def add_points(self, points):
        self.points += points

    def check_bounds(self, x, y):
        if self.bounds == None or (
            self.bounds[0][0] <= x <= self.bounds[1][0]
            or self.bounds[0][1] <= y <= self.bounds[1][1]
        ):
            return True
        return False
