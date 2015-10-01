from src.locations.location import Location, Tile

class Map:
    pass

class Earth(Map):

    @staticmethod
    def create():
        tile1 = Tile.get_dense_trees()
        tile2 = Tile.get_dense_trees()
        tile3 = Tile.get_dense_trees()
        tile4 = Tile.get_trees()
        tile5 = Tile.get_trees()
        tile6 = Tile.get_trees()
        tile7 = Tile.get_sparse_trees()
        tile8 = Tile.get_river()
        tile9 = Tile.get_plain()
        location1 = Location.get_or_insert("0000x0000",type="Woods")
