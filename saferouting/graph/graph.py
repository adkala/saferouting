from .util import *
import numpy as np


class Graph:
    def __init__(self, graphmlFile: str):
        """Creates a graph given a graphml file with coordinate data from OSM.

        :param1 graphmlFile: filepath to .graphml file (default creates graph from 'data/sf.graphml')
        """
        self.d = xml_to_dict(graphmlFile)

        self.points = get_points(self.d)
        self.np_points = np.array([list(x) for x in self.points.values()])
        self.np_ids = list(self.points.keys())

        self.edges = get_edges(self.d)

    def closest_node(self, x: float, y: float) -> int:
        """Returns node id given x, y cartesian coordinates."""
        dists = np.sum((self.np_points - np.asarray([[x, y]])) ** 2, axis=1)
        return self.np_ids[np.argmin(dists)]

    def get_coordinate(self, id: int) -> tuple[float, float]:
        """Returns coordinate of node in cartesian format (x, y) given node id."""
        return self.points[id]

    def get_neighbors(self, id: int) -> list[tuple[int, float]]:
        """Returns list of tuples in the format (neighbor_id, value) given node id."""
        return self.edges.get_neighbors(id)
