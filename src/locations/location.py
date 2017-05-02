import math

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.locations.action import Action
from src.resources import resource


class Tile(polymodel.PolyModel):
    name = ndb.StringProperty(indexed=False)
    type = ndb.StringProperty(indexed=False)
    production = ndb.LocalStructuredProperty(
        resource.Resource, repeated=True, indexed=False)
    resources_available = ndb.LocalStructuredProperty(
        resource.Resource, repeated=True, indexed=False)
    actions = ndb.LocalStructuredProperty(Action, repeated=True, indexed=False)
    building = ndb.StringProperty(indexed=False)
    available_building_names = ndb.StringProperty(repeated=True, indexed=False)

    def build_building(self, building_name):
        print "building %s" % building_name

    def get_resource_production(self, resource_name):
        for resource in self.production:
            if resource.name == resource_name:
                return resource

    def get_resource_available(self, resource_name):
        for resource in self.resources_available:
            if resource.name == resource_name:
                return resource

    def consume_resource(self, resource):
        resource_available = self.get_resource_available(resource.name)
        if not resource_available:
            raise AttributeError

        resource_available.count -= resource.count
        if resource_available.count < 0:
            raise AttributeError
        self.put()

    def perform_action(self, action_name, worker, clicks):
        for action in self.actions:
            if action.name == action_name:
                return action.perform(self, worker, clicks)


class Trees(Tile):

    @staticmethod
    def get_trees_dense():
        gather_wood = Action.get_gather_wood_action()
        actions = [gather_wood]
        wood = resource.Wood.create(count=3)
        wood2 = resource.Wood.create(count=100000)
        return Trees(name="Dense Trees", type="Base", production=[wood],
                     resources_available=[wood2], actions=actions,
                     available_building_names=["Lumberyard"])

    @staticmethod
    def get_trees():
        gather_wood = Action.get_gather_wood_action()
        gather_food = Action.get_gather_food_action()
        actions = [gather_wood, gather_food]
        wood = resource.Wood.create(count=2)
        wood2 = resource.Wood.create(count=10000)
        food = resource.Food.create(count=2)
        food2 = resource.Food.create(count=20000)
        return Trees(name="Trees", type="Base", production=[wood, food],
                     resources_available=[wood2, food2], actions=actions)

    @staticmethod
    def get_trees_sparse():
        gather_wood = Action.get_gather_wood_action()
        gather_food = Action.get_gather_food_action()
        actions = [gather_wood, gather_food]
        wood = resource.Wood.create(count=1)
        wood2 = resource.Wood.create(count=1000)

        return Trees(name="Sparse Trees", type="Base", production=[wood],
                     resources_available=[wood2], actions=actions)


class Plains(Tile):

    @staticmethod
    def get_plains():
        gather_rocks = Action.get_gather_rocks_action()
        actions = [gather_rocks]
        rocks = resource.Rock.create(count=2)
        rocks2 = resource.Rock.create(count=10000)
        return Plains(name="Plains", type="Base", production=[rocks],
                      resources_available=[rocks2], actions=actions)


class River(Tile):

    @staticmethod
    def get_river():
        gather_water = Action.get_gather_water_action()
        actions = [gather_water]
        water = resource.Water.create(count=1)
        water2 = resource.Water.create(count=100000000000000000000)
        return River(name="River", type="Base", production=[water],
                     resources_available=[water2], actions=actions)


class Location(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    type = ndb.StringProperty(indexed=True)
    tiles = ndb.KeyProperty(kind=Tile, repeated=True)
    tiles_per_row = ndb.ComputedProperty(
        lambda self: round(math.sqrt(len(self.tiles))))
