#!/usr/bin/env python

# define map area from OSM data
REGION_OSMID = "R111968"
GRAPHML_FILEPATH = "data/sf.graphml"
SERIALIZED_FILEPATH = ".serialized_routes"

# from top-left to bottom-right in cartesian format
BOUNDS = [(-122.5212, 37.8139), (-122.3482, 37.7089)]

# check for serialized file existence. If not, create serialized routes object.
import os
import saferouting
from saferouting import graph

if not os.path.isfile(SERIALIZED_FILEPATH):
    print("Serialized routes not found, creating it")

    # check for graphml file existence. If not, created graphml file.
    if not os.path.isfile(GRAPHML_FILEPATH):
        print("GraphML file not found, creating it from OSMID %s" % REGION_OSMID)
        graph.util.get_graph_from_osmid(REGION_OSMID, GRAPHML_FILEPATH)
    else:
        print("GraphML file %s found" % GRAPHML_FILEPATH)
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
