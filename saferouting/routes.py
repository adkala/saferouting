from .map import Map
from .util import FHeap
from .route import Route
from .graph import Graph
from . import serialize
from haversine import haversine

from typing import Callable

import time
import math
import types


class Routes(Map):
    def __init__(
        self,
        graph: Graph = None,
        serialized_filepath: str = None,
        bounds: tuple[tuple[float, float], tuple[float, float]] = None,
        level_handler: Callable[
            [
                list[float, float],
                tuple[float, float],
                tuple[float, float],
                tuple[float, float],
                Graph,
            ],
            list[float, float],
        ] = None,
    ):
        """Initializes routes object. Requires either graph or serialized_filepath to create base map. Given both, it defaults to serialized routes object.

        :param1 graph: Graph to create map from (Optional given serialized_filepath).
        :param2 serialized_filepath: Filepath containing serialized routes, used to retrieve object via deserialization (Optional given graph).
        :param3 bounds: Bounds for map given points from top-left to bottom-right in cartesian format (optional).
        :param4 level_handler: Function outputting set of valid points given (neighbor_ids, current_id, source_id, destination_id, graph) for point avoidance. Use Graph.get_coordinate function to get (x, y) tuple (optional). **Warning: Don't make this a lambda, it won't be saved on serialization.**
        """
        if not graph and not serialized_filepath:
            raise Exception("Need to pass graph or serialized_filepath argument.")
        elif serialized_filepath:
            self.__setstate__(serialize.load(serialized_filepath).__getstate__())

        else:
            super().__init__(graph, bounds=bounds)
            self.level_handler = level_handler if level_handler != None else lambda _: _
            self._cached_routes: dict[int, dict[int, Route]] = {}

    def __getstate__(self):
        if (
            isinstance(self.level_handler, types.LambdaType)
            and self.level_handler.__name__ == "<lambda>"
        ):
            self.level_handler = None
        map_state = Map.__getstate__(self)
        routes_state = self.__dict__
        return (map_state, routes_state)

    def __setstate__(self, state):
        map_state, routes_state = state
        self.__dict__ = routes_state
        if self.level_handler == None:
            self.level_handler = lambda _: _
        Map.__setstate__ = map_state

    def get_path(
        self,
        source: tuple[float, float],
        destination: tuple[float, float],
        verbose=False,
    ) -> Route:
        """Given two coordinates, finds best route between them.

        :param1 source: Source coordinate in cartesian format (x, y).
        :param2 destination: Destination coordinate in cartesian format (x, y).
        :param3 verbose: If True, prints debug info (default False).
        """
        out_of_bounds = {}
        if not (self.check_bounds(*source) and self.check_bounds(*destination)):
            error = "Query is out of bounds."
            if verbose:
                print(error)
            out_of_bounds["error"] = error

        s = time.time()
        source_id = self.graph.closest_node(*source)
        destination_id = self.graph.closest_node(*destination)

        route = Route(
            **out_of_bounds,
            **self._modified_a_star(source_id, destination_id, verbose=verbose),
            time=(time.time() - s)
        )

        if verbose:
            print(
                "Query took {:.3f} ms, returns a path traversing {} nodes".format(
                    route.time, len(route)
                )
            )

        self._cache_route(route)
        return route

    def _modified_a_star(self, source_id, destination_id, **kwargs) -> Route:
        open = FHeap()
        closed = set()
        g = {}

        paths: dict[
            int, tuple[int, float]
        ] = {}  # target_id[source_id, cost] (if cost < 0, cached)

        g[source_id] = 0
        h = self._calculate_heuristic(source_id, destination_id)

        open.insert(source_id, h)

        nodes_traversed = 0
        reached = False
        while len(open) > 0:
            curr_id = open.pop()
            if (
                kwargs["verbose"]
                and nodes_traversed
                % (
                    10
                    if nodes_traversed < 100
                    else (10 ** int(math.log(nodes_traversed, 10)))
                )
                == 0
            ):
                print(
                    "Current node: {}, nodes traversed: {}".format(
                        curr_id, nodes_traversed
                    )
                )
            closed.add(curr_id)
            nodes_traversed += 1

            if curr_id == destination_id:
                reached = True
                break

            neighbors = self._get_neighbors(curr_id)
            for n in self.level_handler(
                neighbors, curr_id, source_id, destination_id, self.graph
            ):
                n_id, cost = n
                if n_id in closed:
                    continue

                g[n_id] = g[curr_id] + cost
                h = self._calculate_heuristic(n_id, destination_id)
                f = g[n_id] + h

                open.insert(n_id, f)
                paths[n_id] = (curr_id, cost)  # id, cost

            open.heapify()

        r = {}
        if not reached:
            paths[destination_id] = (curr_id, float("inf"))
            r[
                "error"
            ] = "A-star did not find a valid path from node {} to node {}. Arbitrarily appended destination to end.".format(
                source_id, destination_id
            )
            if kwargs["verbose"]:
                print("Error: " + r["error"])

        r |= self._get_path_from_paths(source_id, destination_id, paths, **kwargs)

        return r

    def _calculate_heuristic(self, source_id, destination_id):
        source = self.graph.get_coordinate(source_id)
        destination = self.graph.get_coordinate(destination_id)
        return haversine(
            source[::-1], destination[::-1]
        )  # coordinates stored in (x, y) [cartesian], haversine requires (lon, lat) [geographic]

    def _get_neighbors(self, id: int):
        """Returns list of tuples in the format (neighbor_id, value) given node id. Cached routes have a value of -1."""
        n = self.graph.get_neighbors(id)
        if id in self._cached_routes:
            for target_id in self._cached_routes[id].keys():
                n.append((target_id, -1))
        return n

    def _get_path_from_paths(
        self,
        source_id: int,
        destination_id: int,
        paths: dict[int, tuple[int, float]],
        **kwargs
    ):
        """:param3 paths: target_id[source_id, cost]"""
        r = {}
        r["cost"] = 0

        _nodes_r = [destination_id]
        _path_r = [self.graph.get_coordinate(_nodes_r[0])]

        curr_id = _nodes_r[0]
        count = 0
        while curr_id != source_id:
            _curr_id, cost = paths[curr_id]
            if cost == -1:
                route = self._cached_routes[_curr_id][curr_id]
                _nodes_r += route.nodes[:-1][::-1]
                _path_r += route.path[:-1][::-1]
                r["cost"] += route.cost

                if kwargs["verbose"]:
                    print(
                        "Using cached route from node {} to node {} with cost {:.2f}".format(
                            _curr_id, curr_id, route.cost
                        )
                    )
            else:
                _nodes_r.append(_curr_id)
                _path_r.append(self.graph.get_coordinate(_curr_id))
                r["cost"] += cost

            curr_id = _curr_id

            count += 1
            if count > len(paths):
                error = "Path not found in under length of edges in paths."
                if kwargs["verbose"]:
                    print("Error: {}".format(error))
                r["error"] = error

        return {"path": _path_r[::-1], "nodes": _nodes_r[::-1]} | r

    def _cache_route(self, route: Route):
        source_id = route.nodes[0]
        destination_id = route.nodes[-1]

        if source_id not in self._cached_routes:
            self._cached_routes[source_id] = {}

        self._cached_routes[source_id][destination_id] = route

    def save(self, filepath=None):
        if filepath:
            serialize.save(self, filepath)
        else:
            serialize.save(self)
