import math
import sys

from bresenham import bresenham
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.resources import resource


class Tile(polymodel.PolyModel):

    DEFAULT_AVAILABLE_BUILDING_NAMES = []
    available_building_names = ndb.StringProperty(repeated=True, indexed=False)
    building = ndb.StringProperty(indexed=True)
    enemies = ndb.LocalStructuredProperty(resource.Resource, repeated=True,
                                          indexed=False)
    is_explored = ndb.BooleanProperty(indexed=True, default=False)
    str_coordinate = ndb.StringProperty(indexed=True)

    def build_building(self, building_name):
        self.building = building_name
        self.put()

    def explore(self, player):
        cost = self.cost_to_explore
        discount, _ = self.get_discounted_cost_to_explore(player)
        for c in cost:
            c.count = int(c.count * discount)
        player.remove_resources(cost)
        self.is_explored = True
        self.put()
        return cost

    @property
    def cost_to_explore(self):
        RADIUS_OF_FIRST_TILE = 4
        TILES_PER_LOCATION = 9

        dst = self.distance_from_middle
        if dst <= 5:
            count = 5 * 10 ** self.distance_from_middle
        else:
            dst_into_tile = (dst - RADIUS_OF_FIRST_TILE) % TILES_PER_LOCATION
            locations_from_middle = 1 + ((dst - RADIUS_OF_FIRST_TILE) / 9)
            location_cost = (50000 * 10 ** locations_from_middle)
            adj_dst_into_tile = int(dst_into_tile * 100)
            count = location_cost * float('1.%s' % adj_dst_into_tile)

        return [resource.Food.create(int(count))]

    @property
    def bresenham_coordinate(self):
        # TODO make work across locations
        return self.coordinate

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

    def get_discounted_cost_to_explore(self, player):
        discounted_tiles = player.discounted_tiles
        tiles = self.get_path_from_origin()
        tiles = [t.name for t in tiles if t.key != self.key]
        discount = 1.0

        for tile in tiles:
            if tile in discounted_tiles:
                for x in xrange(0, discounted_tiles[tile]):
                    discount *= .9

        reason = ""
        for tile, count in discounted_tiles.iteritems():
            if tile in tiles:
                reason += "<br>%s x%s" % (tile, count)

        if reason:
            reason = "because you have earned discounts on the following " \
                     "tiles" + reason

        return discount, reason

    def get_path_from_origin(self):
        origin = Tile.query(Tile.str_coordinate == "4x4").get()
        origin_coords = origin.bresenham_coordinate
        self_coords = self.bresenham_coordinate

        path = list(bresenham(
            origin_coords[0],
            origin_coords[1],
            self_coords[0],
            self_coords[1]))
        tiles = []
        for coord in path:
            tiles.append(Tile.get_by_bresenham_coordinate(coord))
        return tiles

    @classmethod
    def create(cls):
        available_buildings = cls.DEFAULT_AVAILABLE_BUILDING_NAMES
        return cls(available_building_names=available_buildings)

    @staticmethod
    def get_class_by_name(name):
        return getattr(sys.modules[__name__], name)

    @staticmethod
    def get_by_bresenham_coordinate(bresenham_coordinate):
        x, y = bresenham_coordinate
        str_coord = "%sx%s" % (x, y)
        return Tile.query(Tile.str_coordinate == str_coord).get()


class Trees(Tile):
    DEFAULT_AVAILABLE_BUILDING_NAMES = ['Library']

    pass


class Hills(Tile):
    DEFAULT_AVAILABLE_BUILDING_NAMES = ['Mine']
    pass


class Grassland(Tile):
    DEFAULT_AVAILABLE_BUILDING_NAMES = ['Granary']
    pass


class Mountain(Tile):
    DEFAULT_AVAILABLE_BUILDING_NAMES = []
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
