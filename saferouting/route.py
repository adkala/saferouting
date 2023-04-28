import json


class Route:
    """Convenience class for storing route information.

    :attr1 path: A list of cartesian coordinates in the order of a sequential path.

    :attr2 nodes: A list of node IDs in the order of a sequential path. Only useful if original graph is known.

    :attr3 cost: Cost of traversing this path.

    :attr4 time: Time in ms to query this route. If -1, time is unknown (default -1).
    """

    def __init__(
        self,
        path: list[tuple[float, float]],
        nodes: list[int],
        cost: float,
        time: float = -1,
        **kwargs
    ):
        self.path = path
        self.nodes = nodes
        self.cost = cost
        self.time = time
        self.misc = kwargs

    def __repr__(self):
        return self.json()

    def __len__(self):
        return len(self.nodes)

    def json(self):
        """Returns Route object as a JSON string."""

        _ = {}
        _["path"] = self.path
        _["nodes"] = self.nodes
        _["cost"] = self.cost
        _["length"] = len(self)
        _["time"] = self.time
        for i in self.misc:
            _[i] = self.misc[i]
        return json.dumps(_)
