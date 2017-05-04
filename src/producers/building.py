from datetime import datetime
import sys

from google.appengine.ext import ndb

from src.exceptions import InsufficientResourcesException
from src.locations.location import Tile
from src.resources import resource
from src.resources import skill_point


class Building(resource.Resource):
    production_per_tick = ndb.LocalStructuredProperty(
        resource.Resource, indexed=False, repeated=True)
    ticks_per_day = ndb.IntegerProperty(indexed=True, required=True)
    size_per_building = ndb.IntegerProperty(default=1, indexed=True)

    def get_cost(self, map_class):
        raise NotImplementedError('subclass must implement')

    @classmethod
    def build(cls, player, map_class, count=0):
        building = cls.create(count=count)
        cost = building.get_total_cost(map_class)
        player.remove_resources(cost)
        player.add_resource(building)
        return cost

    @staticmethod
    def create(count=0):
        raise NotImplementedError('subclass must implement')

    @property
    def total_space_in_use(self):
        return self.size_per_building * self.count

    @property
    def minutes_between_ticks(self):
        minutes_per_day = 1440
        return minutes_per_day / self.ticks_per_day

    def get_max_discounted_buildings(self, map_class):
        available_space = self.get_total_designated_space(map_class) - \
            self.total_space_in_use
        return available_space / self.size_per_building

    def get_total_cost(self, map_class):
        available_spaces = self.get_max_discounted_buildings(map_class)
        if available_spaces and available_spaces < self.count:
            raise InsufficientResourcesException(
                "Trying to buy too many buildings at a discounted price")

        total = []
        for r in self.get_cost(map_class):
            r_copy = r.clone()
            r_copy.count *= self.count
            total.append(r_copy)
        return total

    def get_total_designated_space(self, map_class):
        locations = map_class.get_locations()
        map_tile_keys = []
        for location in locations:
            map_tile_keys += location.tiles

        building_tiles = Tile.query(Tile.building == self.name).fetch()
        return sum([t.size for t in building_tiles if t.key in map_tile_keys])

    def produce(self):
        production = []
        for r in self.production_per_tick:
            r_copy = r.clone()
            r_copy.count *= self.count
            production.append(r_copy)
        return production

    def should_produce(self):
        now = datetime.now().replace(second=0, microsecond=0)
        seconds_passed_today = (now - now.replace(hour=0, minute=0)).seconds
        minutes_passed_today = seconds_passed_today / 60
        return (minutes_passed_today % self.minutes_between_ticks == 0)


class Library(Building):

    @staticmethod
    def create(count=0):
        ppt = [resource.Science.create(count=25)]
        return Library(count=count, resource_type="building",
                       ticks_per_day=24,
                       production_per_tick=ppt)

    def get_cost(self, map_class):
        if self.get_max_discounted_buildings(map_class) > 0:
            return [resource.Production.create(72)]
        else:
            return [resource.Production.create(144)]


class Mine(Building):

    @staticmethod
    def create(count=0):
        ppt = [resource.Production.create(count=1)]
        return Mine(count=count, resource_type='building',
                    ticks_per_day=6 * 24,
                    production_per_tick=ppt)

    def get_cost(self, map_class):
        if self.get_max_discounted_buildings(map_class) > 0:
            return [resource.Production.create(72)]
        else:
            return [resource.Production.create(500)]


class Granary(Building):

    @staticmethod
    def create(count=0):
        ppt = [resource.Food.create(count=1)]
        return Granary(count=count, resource_type='building',
                       ticks_per_day=6 * 24,
                       production_per_tick=ppt)

    def get_cost(self, map_class):
        if self.get_max_discounted_buildings(map_class) > 0:
            return [resource.Production.create(50)]
        else:
            return [resource.Production.create(100)]


class Capital(Building):

    def get_cost(self, map_class):
        return [resource.Gold.create(sys.maxint)]

    @staticmethod
    def create(count=0):
        ppt = [
            resource.Food.create(count=1),
            resource.Production.create(count=1),
            resource.Science.create(count=1)
        ]
        return Capital(count=count, resource_type="building",
                       ticks_per_day=60 * 24,
                       production_per_tick=ppt,
                       size_per_building=50)
