from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.helpers import LongIntegerProperty

class Resource(polymodel.PolyModel):
    count = LongIntegerProperty(indexed=False)
    tool_needed = ndb.StringProperty()
    resource_type = ndb.StringProperty()

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
    def build(worker, count=0):
        axe = Axe.create(count=count)
        rock = Rock.create(count=count)
        wood = Wood.create(count=count)
        worker.remove_resource(wood)
        worker.remove_resource(rock)
        worker.add_resource(axe)
        return [axe], [rock, wood]

    @staticmethod
    def create(count=0):
        return Axe(resource_type="tool", count=count)

class Dollar(Resource):

    @staticmethod
    def create(count=0):
        return Health(resource_type="financial", count=count)

class Food(Resource):
    freshness = ndb.FloatProperty()

    @staticmethod
    def create(count=0):
        return Food(resource_type="basic", count=count)

class Gold(Resource):

    @staticmethod
    def create(count=0):
        return Gold(resource_type="basic", count=count)

class Health(Resource):

    @staticmethod
    def create(count=0):
        return Health(resource_type="basic", count=count)

class HearthstoneCard(Resource):

    @staticmethod
    def create(count=0):
        return HearthstoneCard(resource_type="earned", count=count)

    @staticmethod
    def create_based_on_results(arean_wins=0, play_mode_wins=0, legendaries=0):
        count = arean_wins * 2 + play_mode_wins * 1 + legendaries * 10
        return HearthstoneCard.create(count)

class Iron(Resource):

    @staticmethod
    def create(count=0):
        return Iron(resource_resource_type="basic", count=count)

class PoolBall(Resource):

    @staticmethod
    def create(count=0):
        return PoolBall(resource_type="earned", count=count)

    @staticmethod
    def create_based_on_results(wins=0, balls=0, lags=0):
        count = wins * 5 + balls * 1 + lags * 1
        return PoolBall.create(count)

class Rock(Resource):

    @staticmethod
    def create(count=0):
        return Rock(resource_type="basic", count=count)

class Step(Resource):

    @staticmethod
    def create(count=0):
        return Step(resource_type="earned", count=count)

class Water(Resource):

    @staticmethod
    def create(count=0):
        return Water(resource_type="basic", count=count)

class Wood(Resource):

    @staticmethod
    def create(count=0):
        return Wood(resource_type="basic", count=count)
