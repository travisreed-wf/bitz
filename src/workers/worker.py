from copy import copy

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

    def add_resource(self, resource):
        for r in self.resources:
            if r.name == resource.name:
                r.count += resource.count
                return

        r_copy = copy(resource)
        self.resources.append(r_copy)
        self.put()

    def remove_resource(self, resource):
        r_copy = copy(resource)
        r_copy.count = resource.count * -1
        self.add_resource(r_copy)



class Player(Worker):

    @staticmethod
    def create():
        health = resource.Health.create(count=10000)
        axe = resource.Axe.create(count=0)
        wood = resource.Wood.create(count=0)
        resources = [health, axe, wood]
        return Player.get_or_insert("Travis Reed", name="Travis Reed", count=1,
                                    resources=resources)

    @property
    def ordered_resources(self):
        return sorted(self.resources, key=lambda resource: resource.type)

    @property
    def organized_resources(self):
        ret = {}
        for resource in self.resources:
            if not ret.get(resource.type):
                ret[resource.type] = []
            ret[resource.type].append(resource)
        return ret
