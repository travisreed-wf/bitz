from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.helpers import LongIntegerProperty

class Resource(polymodel.PolyModel):
    count = LongIntegerProperty(indexed=False)
    tool_needed = ndb.StringProperty()

    @property
    def name(self):
        return self._class_name()

    @property
    def serialize(self):
        d = self.to_dict()
        d['name'] = self.name
        return d


class Axe(Resource):
    pass

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
