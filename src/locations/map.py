from src.locations.location import Location, Trees, River, Plains

class Map:
    pass

class Earth(Map):

    @staticmethod
    def create():
        tile1 = Trees.get_trees_dense().put()
        tile2 = Trees.get_trees_dense().put()
        tile3 = Trees.get_trees_dense().put()
        tile4 = Trees.get_trees().put()
        tile5 = Trees.get_trees().put()
        tile6 = Trees.get_trees().put()
        tile7 = Trees.get_trees_sparse().put()
        tile8 = River.get_river().put()
        tile9 = Plains.get_plains().put()
        tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8, tile9]
        location = Location.get_or_insert("E0000x0000",type="Woods", tiles=tiles)
        location.put()

    @staticmethod
    def get():
        location1 = Location.get_by_id("E0000x0000")
        return [
            [
                location1
            ]
        ]
