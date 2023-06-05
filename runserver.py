#!/usr/bin/env python

import os
import saferouting
from saferouting import graph


# define the level handler
def dummy_handler(
    neighbor_ids: list[int],
    current_id: int,
    source_id: int,
    destination_id: int,
    graph: graph.Graph,
):
    """Dummy level handler, returns all neighbor_ids. Create your own level_handler in the form of this function. Default behavior is to return all neighbors.

    :param1 neighbor_ids: list of neighbor ids')
    :param2 current_id: current node id
    :param3 source_id: source node id
    :param4 destination_id: destination node id
    :param5 graph: Graph object, use it to translate ids to coordinates using Graph.get_coordinate(id) method

    :ret: pruned neighbor ids, should be a subset of neighbor_ids
    """
    return neighbor_ids


LEVEL_HANDLER = (
    dummy_handler  # replace the dummy_handler with your own for custom pruning
)

# define map area from OSM data
REGION_OSMID = "R111968"
GRAPHML_FILEPATH = "data/sf.graphml"
SERIALIZED_FILEPATH = ".serialized_routes"

# from top-left to bottom-right in cartesian format
BOUNDS = [(-122.5212, 37.8139), (-122.3482, 37.7089)]

# check for serialized file existence. If not, create serialized routes object.
if not os.path.isfile(SERIALIZED_FILEPATH):
    print("Serialized routes not found, creating it")

    # check for graphml file existence. If not, created graphml file.
    if not os.path.isfile(GRAPHML_FILEPATH):
        print("GraphML file not found, creating it from OSMID %s" % REGION_OSMID)
        graph.util.get_graph_from_osmid(REGION_OSMID, GRAPHML_FILEPATH)
    else:
        print("GraphML file %s found" % GRAPHML_FILEPATH)

    # to use level handler, change line to include it
    # [saferouting.Routes(graph=graph.Graph(GRAPHML_FILEPATH), bounds=BOUNDS)]
    saferouting.Routes(graph=graph.Graph(GRAPHML_FILEPATH), bounds=BOUNDS).save(
        SERIALIZED_FILEPATH
    )


else:
    print("Serialized routes found in %s" % SERIALIZED_FILEPATH)

os.environ.setdefault("DJANGO_SERIALIZED_ROUTES_FILEPATH", SERIALIZED_FILEPATH)

# run django server
import subprocess

print("Running server from manage.py")
try:
    subprocess.call(["python3", "api/manage.py", "runserver"])
except OSError as e:
    if e.errno == e.errno.ENOENT:
        try:
            subprocess.call(["python", "api/manage.py", "runserver"])
        except OSError as e:
            raise e
    else:
        raise e
