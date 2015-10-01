from src.locations.location import Location, Tile, Trees, River, Plains

class Map:
    pass

class Earth(Map):

    @staticmethod
    def create():
        tile1 = Trees.get_trees_dense()
        tile2 = Trees.get_trees_dense()
        tile3 = Trees.get_trees_dense()
        tile4 = Trees.get_trees()
        tile5 = Trees.get_trees()
        tile6 = Trees.get_trees()
        tile7 = Trees.get_trees_sparse()
        tile8 = River.get_river()
        tile9 = Plains.get_plains()
        tiles = [
            tile1.key,
            tile2.key,
            tile3.key,
            tile4.key,
            tile5.key,
            tile6.key,
            tile7.key,
            tile8.key,
            tile9.key
        ]
        Location.get_or_insert("0000x0000",type="Woods", tiles=tiles)
