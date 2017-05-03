import math
import sys

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.resources import resource


class Tile(polymodel.PolyModel):

    DEFAULT_AVAILABLE_BUILDING_NAMES = []
    available_building_names = ndb.StringProperty(repeated=True, indexed=False)
    building = ndb.StringProperty(indexed=True)
    enemies = ndb.LocalStructuredProperty(resource.Resource, repeated=True,
                                          indexed=False)
    is_explored = ndb.BooleanProperty(indexed=False, default=False)
    str_coordinate = ndb.StringProperty(indexed=True)

    def build_building(self, building_name):
        self.building = building_name
        self.put()

    def explore(self, player):
        cost = self.cost_to_explore
        player.remove_resources(cost)
        self.is_explored = True
        self.put()
        return cost

    @property
    def cost_to_explore(self):
        count = 5 * 10 ** self.distance_from_middle
        return [resource.Food.create(int(count))]

    @property
    def distance_from_middle(self):
        middle_coordinate = 4, 4

        x_distance = abs(middle_coordinate[0] - self.coordinate[0])
        y_distance = abs(middle_coordinate[1] - self.coordinate[1])
        return round(math.sqrt(x_distance ** 2 + y_distance ** 2), 2)

    @property
    def name(self):
        return self._class_name()

    @property
    def coordinate(self):
        x, y = self.str_coordinate.split('x')
        return int(x), int(y)

    @property
    def size(self):
        return 50

    @classmethod
    def create(cls):
        available_buildings = cls.DEFAULT_AVAILABLE_BUILDING_NAMES
        return cls(available_building_names=available_buildings)

    @staticmethod
    def get_class_by_name(name):
        return getattr(sys.modules[__name__], name)


class Trees(Tile):
    pass


class DenseTrees(Trees):
    DEFAULT_AVAILABLE_BUILDING_NAMES = ['PoolHall', 'DartShack']
    pass


class SparseTrees(Trees):
    DEFAULT_AVAILABLE_BUILDING_NAMES = ['PoolHall']

    pass


class Plains(Tile):
    DEFAULT_AVAILABLE_BUILDING_NAMES = ['SpearGoblinHut']
    pass


class River(Tile):
    pass


class Location(ndb.Model):
    tiles = ndb.KeyProperty(kind=Tile, repeated=True)
    # tiles_per_row = ndb.ComputedProperty(
    #     lambda self: round(math.sqrt(len(self.tiles))))

    @property
    def name(self):
        return self.key.id()

    @property
    def tiles_per_row(self):
        return 9

    def get_coordinate(self):
        x_coordinate, y_coordinate = self.key.id()[1:].split('x')
        return int(x_coordinate), int(y_coordinate)

    def get_short_coordinate_of_tile(self, index):
        x_coordinate = index % self.tiles_per_row
        y_coordinate = index / self.tiles_per_row
        return int(x_coordinate), int(y_coordinate)

    def get_full_coordinate_of_tile(self, index):
        location_x_coordinate, location_y_coordinate = self.get_coordinate()
        location_x_offset = self.tiles_per_row * location_x_coordinate
        location_y_offset = self.tiles_per_row * location_y_coordinate
        tile_x_coordinate, tile_y_coordinate = \
            self.get_short_coordinate_of_tile(index)
        if location_x_offset < 0:
            total_x_coordinate = location_x_offset - tile_x_coordinate
        else:
            total_x_coordinate = location_x_offset + tile_x_coordinate

        if location_y_offset < 0:
            total_y_coordinate = location_y_offset - tile_y_coordinate
        else:
            total_y_coordinate = location_y_offset + tile_y_coordinate
        return int(total_x_coordinate), int(total_y_coordinate)
