from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.helpers import LongIntegerProperty

class Resource(polymodel.PolyModel):
    count = LongIntegerProperty(indexed=False)
    tool_needed = ndb.StringProperty()
    type = ndb.StringProperty()

    @property
    def name(self):
        return self._class_name()

    @property
    def serialize(self):
        d = self.to_dict()
        d['name'] = self.name
        return d


class Axe(Resource):

    @staticmethod
    def create(count=0):
        return Axe(type="tool", count=count)

class Dollar(Resource):

    @staticmethod
    def create(count=0):
        return Health(type="financial", count=count)

class Food(Resource):
    freshness = ndb.FloatProperty()

    @staticmethod
    def create(count=0):
        return Food(type="basic", count=count)

class Gold(Resource):

    @staticmethod
    def create(count=0):
        return Gold(type="basic", count=count)

class Health(Resource):

    @staticmethod
    def create(count=0):
        return Health(type="basic", count=count)

class Iron(Resource):

    @staticmethod
    def create(count=0):
        return Iron(type="basic", count=count)

class Step(Resource):

    @staticmethod
    def create(count=0):
        return Step(type="earned", count=count)

class Water(Resource):

    @staticmethod
    def create(count=0):
        return Water(type="basic", count=count)

class Wood(Resource):

    @staticmethod
    def create(count=0):
        return Wood(type="basic", count=count)
