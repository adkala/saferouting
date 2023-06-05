# Safe Routing Package / API

This safe routing package / API was created for LA Hacks 2023. This was created to solve the problem of efficient path finding with point avoidance, as the original project idea catered to finding walkable paths while avoiding areas deemed as dangerous.

The original maps and corresponding graphs are sourced from Open Street Maps. All coordinates are assumed to be in cartesian format.

## Package Info

The package centers around the `Routes` object, which gives a path given a `graph` (of type `Graph`, also in package) and a `level_handler`, which is described in more detail below.

The algorithm is essentially a-star with pruning as defined by a user-given function, passed in through the `level_handler` parameter of the `Routes` object. The `level_handler` takes in four parameters: `neighbor_ids`, `current_point_id`, `source_id`, `destintation_id`, and the `Graph` object. The output of `level_handler` should be a subset of `neighbor_ids`.

The reason for inputting and outputting an entire list rather than checking for whether an individual point is valid is to allow for pruning according to the entire `neighbor_ids` list, as well as the `source_id` and `destination_id`.

To get coordinates from a `node_id`, use the function `Graph.get_coordinate`.

## Using the Package

First, create the graph from an OSM ID (from Open Street Maps). This is done through `graph.util.get_graph_from_osmid`. Then initialize the corresponding `Graph` and pass it into `Routes`. A rough outline can be seen in `runserver.py`.

Call `Routes.get_path` to generate a path and whose output will be of type `Route`. Use `Route.path` to get a list of ordered coordinates.

## Using the API

The REST API can also be used. It is currently setup to only path within the San Francisco region as defined by OSM ID R111968, although this can be changed in `runserver.py`. If you do change this, make sure to change the corresponding `BOUNDS` variable. Otherwise you will receieve an error.

To change the level handler to your custom implementation, replace `dummy_handler` on line 30 in the `runserver.py` file with your function call.

To start it, run the `runserver.py` script. It will start a Django server at `localhost:8000`. To get a path, make a GET request to the path `https://localhost:8000/api/routing/route` with parameters x0, y0, x1, and y1. These are used to define the source and destination coordinates, which are (x0, y0) and (x1, y1) respectively. The response will be in JSON format, converted from a `Route` object.
