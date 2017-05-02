from copy import copy
import logging

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.resources import resource
from src.transactions.transaction import Transaction


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
        r = self.get_resource_by_name(resource.name)
        if r:
            if r.count >= 0 and r.count + resource.count < 0:
                raise ValueError
            r.count += resource.count
            self.put()
            return
        else:
            if resource.count < 0:
                raise ValueError
            r_copy = copy(resource)
            self.resources.append(r_copy)
            self.put()

        self._add_transaction(resource)

    def _add_transaction(self, resource):
        if resource.count > 0:
            action = 'Add'
        else:
            action = 'Remove'
        description = "%s %s %s's" % (action, resource.count, resource.name)
        Transaction(count=resource.count, description=description).put()

    def check_basic_needs(self):
        food_check_passed = False
        water_check_passed = False
        health = None
        for resource in self.resources:
            if resource.name == "Food":
                if resource.count >= 1:
                    food_check_passed = True
                    resource.count -= 1
            elif resource.name == "Water":
                if resource.count >= 1:
                    water_check_passed = True
                    resource.count -= 1
            elif resource.name == "Health":
                health = resource
        if not water_check_passed or not food_check_passed:
            health.count -= 1
        if health.count <= 0:
            logging.warning("Your health dropped too low, you should be dead!")
        self.put()

    def get_resource_by_name(self, name):
        for r in self.resources:
            if r.name == name:
                return r
        return None

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
        return sorted(
            self.resources, key=lambda resource: resource.resource_type)

    @property
    def organized_resources(self):
        ret = {}
        for resource in self.resources:
            if not ret.get(resource.resource_type):
                ret[resource.resource_type] = []
            ret[resource.resource_type].append(resource)
        return ret
