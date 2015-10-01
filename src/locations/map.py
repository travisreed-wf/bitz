from src.locations.location import Location, Trees, River, Plains

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
        tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8, tile9]
        Location.get_or_insert("E0000x0000",type="Woods", tiles=tiles)

    @staticmethod
    def get():
        location1 = Location.get_by_id("E0000x0000")
        return [
            [
                location1
            ]
        ]
