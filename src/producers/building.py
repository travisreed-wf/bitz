from datetime import datetime
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
        cost = building.total_cost
        player.remove_resources(cost)
        player.add_resource(building)
        return cost

    @staticmethod
    def create(count=0):
        raise NotImplementedError('subclass must implement')

    @property
    def total_cost(self):
        total = []
        for r in self.cost:
            r_copy = r.clone()
            r_copy.count *= self.count
            total.append(r_copy)
        return total

    def produce(self):
        production = []
        for r in self.production_per_tick:
            r_copy = r.clone()
            r_copy.count *= self.count
            production.append(r_copy)
        return production

    def should_produce(self):
        ten_minute_sections_per_day = 24 * 6
        ten_minute_sections_between_ticks = (
            ten_minute_sections_per_day / self.ticks_per_day)
        now = datetime.now().replace(second=0, microsecond=0)
        seconds_passed_today = now - now.replace(hour=0, minute=0)
        ten_minute_sections_passed_today = seconds_passed_today / 600
        return (ten_minute_sections_passed_today %
                ten_minute_sections_between_ticks == 0)


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
