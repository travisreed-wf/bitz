import logging

from google.appengine.ext import ndb, deferred
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

    @ndb.transactional
    def add_resources(self, resources_to_add, reason=''):
        from src.notifications import notification

        fresh_worker = self.key.get()
        for resource_to_add in resources_to_add:
            r = fresh_worker.get_resource_by_name(resource_to_add.name)
            if r:
                if r.count + resource_to_add.count < 0:
                    raise InsufficientResourcesException()
                r.count += resource_to_add.count
                if resource_to_add.count >= 0:
                    r.lifespan_count += resource_to_add.count
            else:
                if resource_to_add.count < 0:
                    raise InsufficientResourcesException()
                r_copy = resource_to_add.clone()
                r_copy.lifespan_count = resource_to_add.count
                fresh_worker.resources.append(r_copy)

        fresh_worker.put()
        self.resources = fresh_worker.resources
        for resource_to_add in resources_to_add:
            deferred.defer(self._add_transaction, resource_to_add, reason)
            if resource_to_add.count > 0 and \
                    resource_to_add.resource_type == 'earned':
                deferred.defer(
                    notification.create_new_earned_resource_notification,
                    self.key, resource_to_add.name, resource_to_add.count,
                    reason=reason, _transactional=True)

    @ndb.transactional
    def add_follower(self, follower, is_free, reason=''):
        from src.notifications import notification

        fresh_worker = self.key.get()
        r = fresh_worker.get_resource_by_name(follower.name)
        if r:
            r.count += follower.count
            if not is_free:
                r.lifespan_count += follower.count
        else:
            r_copy = follower.clone()
            if not is_free:
                r_copy.lifespan_count = follower.count
            fresh_worker.resources.append(r_copy)

        fresh_worker.put()
        self.resources = fresh_worker.resources
        deferred.defer(self._add_transaction, follower, reason)
        deferred.defer(
            notification.create_new_follower_notification,
            self.key, follower.name, reason, _transactional=True)

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

    def percent_of_cost_available(self, cost):
        total_cost_count = 0
        available_count = 0
        for resource_to_remove in cost:
            if resource_to_remove.count <= 0:
                continue
            total_cost_count += resource_to_remove.count
            r = self.get_resource_by_name(resource_to_remove.name)
            if r and r.count:
                if r.count > resource_to_remove.count:
                    available_count += resource_to_remove.count
                else:
                    available_count += r.count

        return int(100 * float(available_count) / total_cost_count)

    def check_basic_needs(self):
        food = resource.Food.create(count=10)
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

        resources = [
            resource.Health.create(count=10000),
            building.Granary.create(),
            resource.PoolBall.create(),
            resource.HearthstoneCard.create(),
            resource.ClashRoyaleWins.create(),
            resource.Rocket.create(),
            resource.LeagueOfLegendsWin.create(),
            building.Capital.create(1),
            resource.Dart.create(),
            building.Library.create(),
            building.Mine.create(),
            resource.Production.create(),
            resource.Science.create(),
            resource.Food.create()
        ]
        return Player.get_or_insert("Travis Reed", name="Travis Reed", count=1,
                                    resources=resources)

    @staticmethod
    def create_god_mode():
        resources = [
            resource.Health.create(count=10000000),
            building.Granary.create(2),
            resource.PoolBall.create(500),
            resource.HearthstoneCard.create(2),
            resource.ClashRoyaleWins.create(633),
            resource.Rocket.create(),
            resource.LeagueOfLegendsWin.create(336),
            building.Capital.create(1),
            resource.Dart.create(5),
            building.Mine.create(2),
            building.Library.create(1),
            resource.Food.create(10000000),
            resource.Science.create(500000),
            resource.Production.create(50000)
        ]

        return Player.get_or_insert("Travis Reed", name="Travis Reed", count=1,
                                    resources=resources)

    @property
    def buildings(self):
        return [r for r in self.resources if r.resource_type == 'building']

    @property
    def discounted_tiles(self):
        tiles = {}
        for r in self.resources:
            if r.resource_type == 'follower' and hasattr(r, "discounted_tile"):
                if r.discounted_tile not in tiles:
                    tiles[r.discounted_tile] = 0
                tiles[r.discounted_tile] += int(r.count)
        return tiles

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
        for r in self.resources:
            if not ret.get(r.resource_type):
                ret[r.resource_type] = []
            ret[r.resource_type].append(r)
        return ret

    def get_recent_notifications(self):
        from src.notifications.notification import Notification
        if hasattr(self, "_recent_notifications"):
            return self._recent_notifications

        self._recent_notifications = \
            Notification.query(Notification.player_key == self.key).order(
                -Notification.time).fetch(limit=10)
        return self._recent_notifications

    def get_recent_unread_notifications(self):
        recent = self.get_recent_notifications()
        return [n for n in recent if not n.is_read]
