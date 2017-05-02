import math
import sys

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Tile(polymodel.PolyModel):

    DEFAULT_AVAILABLE_BUILDING_NAMES = []

    building = ndb.StringProperty(indexed=False)
    available_building_names = ndb.StringProperty(repeated=True, indexed=False)

    def build_building(self, building_name):
        print "building %s" % building_name

    @property
    def name(self):
        return self._class_name()

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
    pass


class SparseTrees(Trees):
    pass


class Plains(Tile):
    pass


class River(Tile):
    pass


class Location(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    tiles = ndb.KeyProperty(kind=Tile, repeated=True)
    tiles_per_row = ndb.ComputedProperty(
        lambda self: round(math.sqrt(len(self.tiles))))
