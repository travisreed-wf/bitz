import random
from src.locations.location import Location, Tile


class Map:

    ROOT_ID = None
    AVAILABLE_TILES = []

    @classmethod
    def create(cls):
        location = cls._generate_location(cls.ROOT_ID)
        return location

    @classmethod
    def get(cls, position=None):
        if position:
            id = cls.ROOT_ID[0] + position
        else:
            id = cls.ROOT_ID
        return Location.get_by_id(id)

    @classmethod
    def _generate_location(cls, location_id):
        tiles = []
        while len(tiles) < 100:
            tiles.append(cls._generate_tile().key)
        location = Location.get_or_insert(location_id, tiles=tiles)
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
                tile.put()
                return tile
        return None


class Earth(Map):

    ROOT_ID = 'E0000x0000'
    AVAILABLE_TILES = [
        {
            'name': 'DenseTrees',
            'percent_appearance': 10
        },
        {
            'name': 'SparseTrees',
            'percent_appearance': 30
        },
        {
            'name': 'Trees',
            'percent_appearance': 30
        },
        {
            'name': 'River',
            'percent_appearance': 5
        },
        {
            'name': 'Plains',
            'percent_appearance': 25
        }
    ]
