from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.resources import resource


class Worker(polymodel.PolyModel):
    name = ndb.StringProperty()
    count = ndb.IntegerProperty(indexed=False)
    daily_cost = ndb.LocalStructuredProperty(resource.Resource, repeated=True,
                                             indexed=False)
    production = ndb.LocalStructuredProperty(resource.Resource, repeated=True,
                                             indexed=False)
    production_rate = ndb.IntegerProperty(indexed=False)
    resources = ndb.LocalStructuredProperty(resource.Resource, repeated=True,
                                            indexed=False)


class Player(Worker):

    @staticmethod
    def create():
        health = resource.Health(count=10000)
        axe = resource.Axe(count=0)
        wood = resource.Wood(count=0)
        resources = [health, axe, wood]
        return Player.get_or_insert("Travis Reed", name="Travis Reed", count=1,
                                    resources=resources)

