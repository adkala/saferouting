import os

from django.http import HttpResponse
from tastypie.resources import Resource

from saferouting import Routes


class RouteResource(Resource):
    class Meta:
        resource_name = "route"
        allowed_methods = ["get"]

    def __init__(self):
        super().__init__()
        self.routes = Routes(
            serialized_filepath=os.environ.get("DJANGO_SERIALIZED_ROUTES_FILEPATH")
        )

    def get_list(self, request, **kwargs):
        _c = ["x0", "y0", "x1", "y1"]
        c = []

        m = []
        for _ in _c:
            __ = request.GET.get(_)
            if __ == None:
                m.append(_)

            c.append(__)

        if len(m) > 0:
            return HttpResponse("missing parameters %s" % ", ".join(m), status="400")

        source = (float(c[0]), float(c[1]))
        target = (float(c[2]), float(c[3]))

        response = HttpResponse()
        response.write(self.routes.get_path(source, target, verbose=True).json())
        return response
