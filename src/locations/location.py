from copy import copy

from google.appengine.ext import ndb

from src.resources import resource


class Tile(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    type = ndb.StringProperty(indexed=False)
    production = ndb.LocalStructuredProperty(
        kind="Resource", repeated=True, indexed=False)
    resources_available = ndb.LocalStructuredProperty(
        kind="Resource", repeated=True, indexed=False)

    def get_resource_production(self, resource_name):
        for resource in self.production:
            if resource.name == resource_name:
                return resource

    def get_resource_available(self, resource_name):
        for resource in self.resources_available:
            if resource.name == resource_name:
                return resource

    def consume_resource(self, resource):
        resource_available = self.get_resource_available(self, resource.name)
        if not resource_available:
            raise AttributeError

        resource_available.count -= resource.count
        if resource_available.count < 0:
            raise AttributeError
        self.put()


class Trees(Tile):
    def gather(self, resource_name, resources_used):
        resources_used = [r.name for r in resources_used]
        resource = None
        if resource_name == "Wood":
            resource = self.gather_wood(resources_used)

        self.consume_resource(resource)

    def gather_wood(self, resources_used):
        resource = copy(self.get_resource_production("Wood"))

        if "Axe" in resources_used:
            resource.count = resource.count * 3

        return resource

    @staticmethod
    def get_trees_dense():
        wood = resource.Wood(count=1).put()
        wood2 = resource.Wood(count=100000)
        return Trees(name="Dense Trees", type="Base", production=[wood],
                     resources_available=[wood2])

    @staticmethod
    def get_trees():
        wood = resource.Wood(count=1).put()
        wood2 = resource.Wood(count=10000)
        return Trees(name="Trees", type="Base", production=[wood],
                     resources_available=[wood2])

    @staticmethod
    def get_trees_sparse():
        wood = resource.Wood(count=1).put()
        wood2 = resource.Wood(count=1000)
        return Trees(name="Sparse Trees", type="Base", production=[wood],
                     resources_available=[wood2])

class Plains(Tile):

    @staticmethod
    def get_plains():
        return Plains(name="Plains", type="Base", production=[])


class River(Tile):

    @staticmethod
    def get_river():
        water = resource.Water(count=1)
        water2 = resource.Water(count=100000000000000000000)
        return River(name="River", type="Base", production=[water],
                     resources_available=[water2])


class Location(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    type = ndb.StringProperty(indexed=True)
    tiles = ndb.LocalStructuredProperty(Tile, repeated=True)
