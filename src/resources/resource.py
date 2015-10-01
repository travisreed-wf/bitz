from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

class Resource(polymodel.PolyModel):

    @property
    def name(self):
        return self._class_name()


class Dollar(Resource):
    pass

class Food(Resource):
    freshness = ndb.FloatProperty()
    pass

class Gold(Resource):
    pass

class Health(Resource):
    pass

class Iron(Resource):
    pass

class Water(Resource):
    pass

class Wood(Resource):
    pass
