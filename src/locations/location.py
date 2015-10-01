from google.appengine.ext import ndb

from src.resources import resource

class Tile(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    type = ndb.StringProperty(indexed=False)
    production_when_clicked = ndb.JsonProperty
    resources_available = ndb.KeyProperty(
        kind="Resource", repeated=True, indexed=False)


class Trees(Tile):

    def gather_wood(self, tools=None):
        if not tools:
            health = resource.Health()
            return self.production_when_clicked,



    def click(self, resources_provided={}, click_count=1):
        """Returns resources, and cost"""
        production = ndb.get_multi(self.production_when_clicked)
        cost = ndb.get_multi(self.cost_when_clicked)
        for c in cost:
            for r in resources_provided:
                if r.name == c.name:

            c.count = c.count * click_count
        available = ndb.get_multi(self.resources_available)
        for p in production:
            p.count = p.count * click_count
            found = False
            for r in available:
                if r.name == p.name:
                    r.count -= p.count
                    found = True
                    break
            if not found:
                raise AttributeError()

        ndb.put_multi(available)
        return production


    @staticmethod
    def get_plains():
        water = resource.Water(count=2).put()
        return Tile(name="River", type="Base", production=water)

    @staticmethod
    def get_river():
        water = resource.Water(count=2).put()
        return Tile(name="River", type="Base", production=water)

    @staticmethod
    def get_trees_dense():
        wood = resource.Wood(count=3).put()
        return Tile(name="Dense Trees", type="Base", production=wood)

    @staticmethod
    def get_trees():
        wood = resource.Wood(count=2).put()
        return Tile(name="Trees", type="Base", production=wood)

    @staticmethod
    def get_trees_sparse():
        wood = resource.Wood(count=1).put()
        return Tile(name="Sparse Trees", type="Base", production=wood)


class Location(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    type = ndb.StringProperty(indexed=True)
    tiles = ndb.LocalStructuredProperty(Tile, repeated=True)
