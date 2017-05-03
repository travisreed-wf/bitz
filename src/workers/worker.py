import logging

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.exceptions import InsufficientResourcesException
from src.producers import building
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

    def add_resource(self, resource_to_add, reason=''):
        self.add_resources([resource_to_add], reason=reason)

    def add_resources(self, resources_to_add, reason=''):
        for resource_to_add in resources_to_add:
            r = self.get_resource_by_name(resource_to_add.name)
            if r:
                if r.count + resource_to_add.count < 0:
                    raise InsufficientResourcesException()
                r.count += resource_to_add.count
            else:
                if resource_to_add.count < 0:
                    raise InsufficientResourcesException()
                r_copy = resource_to_add.clone()
                self.resources.append(r_copy)

        self.put()
        for resource_to_add in resources_to_add:
            self._add_transaction(resource_to_add, reason)

    def _add_transaction(self, resource_to_add, reason):
        if resource_to_add.count == 0:
            return
        if resource_to_add.count > 0:
            action = 'Add'
        else:
            action = 'Remove'
        description = "%s %s %s" % (
            action, abs(resource_to_add.count), resource_to_add.name)
        if reason:
            description += ' because %s' % reason
        Transaction(
            count=resource_to_add.count, description=description,).put()

    def check_basic_needs(self):
        food = resource.Food.create(count=1)
        try:
            self.remove_resource(food)
        except InsufficientResourcesException:
            health = resource.Health(count=-1)
            try:
                reason = 'not enough resources to meet basic needs'
                self.add_resource(health, reason=reason)
            except InsufficientResourcesException:
                logging.warning(
                    "Your health dropped too low, you should be dead!")
        self.put()

    def get_resource_by_name(self, name):
        for r in self.resources:
            if r.name == name:
                return r
        return None

    def remove_resources(self, resources_to_remove):
        copies = []
        for resource_to_remove in resources_to_remove:
            r_copy = resource_to_remove.clone()
            r_copy.count = resource_to_remove.count * -1
            copies.append(r_copy)

        self.add_resources(copies)

    def remove_resource(self, resource_to_remove):
        self.remove_resources([resource_to_remove])


class Player(Worker):

    @staticmethod
    def create():
        health = resource.Health.create(count=10000)
        pool_hall = building.PoolHall.create()
        pool_ball = resource.PoolBall.create()
        hearth = resource.HearthstoneCard.create()
        clash = resource.ClashRoyaleWins.create()
        rockets = resource.Rocket.create()
        lol = resource.LeagueOfLegendsWin.create()
        capital = building.Capital.create(1)
        resources = [
            health, pool_hall, pool_ball, hearth, clash, rockets, lol, capital
        ]
        return Player.get_or_insert("Travis Reed", name="Travis Reed", count=1,
                                    resources=resources)

    @staticmethod
    def create_god_mode():
        health = resource.Health.create(count=1000000)
        pool_hall = building.PoolHall.create(2)
        pool_ball = resource.PoolBall.create(500)
        hearth = resource.HearthstoneCard.create(5)
        clash = resource.ClashRoyaleWins.create(600)
        rockets = resource.Rocket.create(1)
        lol = resource.LeagueOfLegendsWin.create(1000)
        capital = building.Capital.create(1)
        food = resource.Food().create(10000000)
        resources = [
            health, pool_hall, pool_ball, hearth, clash, rockets, lol, capital,
            food
        ]
        return Player.get_or_insert("Travis Reed", name="Travis Reed", count=1,
                                    resources=resources)

    @property
    def buildings(self):
        return [r for r in self.resources if r.resource_type == 'building']

    @property
    def ordered_buildings(self):
        return sorted(self.buildings, key=lambda b: b.name)

    @property
    def ordered_resources(self):
        return sorted(
            self.resources, key=lambda r: r.resource_type)

    @property
    def organized_resources(self):
        ret = {}
        for resource in self.resources:
            if not ret.get(resource.resource_type):
                ret[resource.resource_type] = []
            ret[resource.resource_type].append(resource)
        return ret
