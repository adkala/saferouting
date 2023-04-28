from xml.dom import minidom
from .edge import *

import osmnx as ox
import xmltodict


def get_graph_from_osmid(osmid, filepath):
    """Retrieves data from OSM using OSMID and saves it to filepath in graphml format."""
    polygon = ox.geocoder.geocode_to_gdf(osmid, by_osmid=True).values.tolist()[0][0]
    graph = ox.graph.graph_from_polygon(
        polygon,
        network_type="walk",
        simplify=True,
        retain_all=True,
        truncate_by_edge=True,
        clean_periphery=True,
    )
    ox.save_graphml(graph, filepath)


def xml_to_dict(graphmlFile):
    d = {}
    with open(graphmlFile) as fd:
        d = xmltodict.parse(fd.read())
    return d


def get_points(d: dict) -> dict[int, tuple[float, float]]:
    points = {}
    nodes = d["graphml"]["graph"]["node"]
    for node in nodes:
        id = int(node["@id"])
        x, y = None, None
        for data in node["data"]:
            if data["@key"] == "d5":
                x = float(data["#text"])
            elif data["@key"] == "d4":
                y = float(data["#text"])
        if x == None or y == None:
            print(
                "Warning: Skipping node {0} due to missing {1} coordinate".format(
                    id, "x" if x == None else "" + "y" if y == None else ""
                )
            )
            continue
        points[id] = (x, y)
    return points


def get_edges(d: dict) -> Edges:
    edges = []
    d_edges = d["graphml"]["graph"]["edge"]
    for edge in d_edges:
        source, target = int(edge["@source"]), int(edge["@target"])
        value = None
        reversed = False
        for data in edge["data"]:
            if data["@key"] == "d13":
                value = float(data["#text"])
            if data["@key"] == "d12" and data["#text"] == "True":
                reversed = True
        if value == None:
            print(
                "Warning: Skipping edge ({0}, {1}) due to missing value".format(
                    source, target
                )
            )
            continue
        edges.append(Edge(source, target, value))
        if reversed:
            edges.append(Edge(target, source, value))
    return Edges(edges)
