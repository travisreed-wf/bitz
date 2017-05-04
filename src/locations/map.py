import random

from google.appengine.ext import ndb

from src.locations.location import Location, Tile


class Map:

    ROOT_ID = None
    AVAILABLE_TILES = []
    LOCATION_SIZE = 81

    @classmethod
    def create(cls):
        location = cls._generate_location(cls.ROOT_ID)
        middle_tile = cls.get_middle_tile()
        middle_tile.is_explored = True
        middle_tile.building = 'Capital'
        middle_tile.put()
        return location

    @classmethod
    def get_locations(cls):
        return Location.query().fetch()

    @classmethod
    def get_location(cls, position=None):
        if position:
            id = cls.ROOT_ID[0] + position
        else:
            id = cls.ROOT_ID
        return Location.get_by_id(id)

    @classmethod
    def get_middle_tile(cls):
        location = cls.get_location()
        total_tiles = len(location.tiles)
        return location.tiles[total_tiles / 2].get()

    @classmethod
    def _generate_location(cls, location_id):
        location = Location.get_or_insert(location_id)
        tiles = []
        for index in xrange(0, cls.LOCATION_SIZE):
            tile = cls._generate_tile()
            coord = location.get_full_coordinate_of_tile(index)
            tile.str_coordinate = '%sx%s' % coord
            tiles.append(tile)

        location.tiles = ndb.put_multi(tiles)
        location.put()
        return location

    @classmethod
    def _generate_tile(cls):
        rand = random.randint(1, 100)
        total = 0
        for tile_type in cls.AVAILABLE_TILES:
            total += tile_type['percent_appearance']
            if total >= rand:
                tile_class = Tile.get_class_by_name(tile_type['name'])
                tile = tile_class.create()
                return tile
        return None


class Earth(Map):

    ROOT_ID = 'E0000x0000'
    AVAILABLE_TILES = [
        {
            'name': 'Trees',
            'percent_appearance': 50
        },
        {
            'name': 'Grassland',
            'percent_appearance': 30
        },
        {
            'name': 'River',
            'percent_appearance': 5
        },
        {
            'name': 'Hills',
            'percent_appearance': 10
        },
        {
            'name': 'Mountain',
            'percent_appearance': 5
        }
    ]
