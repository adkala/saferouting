class Edge:
    def __init__(self, a, b, value):
        self.edge = (a, b)
        self.value = value


class Edges:
    adj: dict[int, Edge] = {}
    len = 0

    def __init__(self, list_of_edges: list[Edge] = []):
        for e in list_of_edges:
            self.insert(e)

    def __len__(self):
        return self.len

    def __getitem__(self, i: int):
        return self.adj[i]

    def insert(self, e: Edge):
        source, _ = e.edge
        if source not in self.adj:
            self.adj[source] = []
        self.adj[source].append(e)
        self.len += 1

    def get_neighbors(self, id: int):
        return [(e.edge[1], e.value) for e in self.adj[id]]
