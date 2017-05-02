from google.appengine.ext import ndb

from src.resources import resource
from src.resources import skill_point


class Building(resource.Resource):
    production_per_tick = ndb.LocalStructuredProperty(
        resource.Resource, indexed=False, repeated=True)
    ticks_per_day = ndb.IntegerProperty(indexed=True, required=True)

    @property
    def cost(self):
        raise NotImplementedError('subclass must implement')

    @classmethod
    def build(cls, player, count=0):
        building = cls.create(count=count)
        player.remove_resource(building.total_cost)
        player.add_resource(building)

    @staticmethod
    def create(count=0):
        raise NotImplementedError('subclass must implement')

    def total_cost(self):
        total = []
        for r in self.cost:
            r_copy = r.clone()
            r_copy.count *= self.count
            total.append(r_copy)
        return total


class PoolHall(Building):

    @property
    def cost(self):
        return [resource.PoolBall.create(50)]

    @staticmethod
    def create(count=0):
        ppt = [skill_point.PoolSkillPoint.create(count=1)]
        return PoolHall(count=count, resource_type="building",
                        ticks_per_day=6 * 24,
                        production_per_tick=ppt)
