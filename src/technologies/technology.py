import sys

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.technologies import config


class Technology(polymodel.PolyModel):
    can_research = ndb.BooleanProperty(indexed=True, default=False)
    is_researched = ndb.BooleanProperty(indexed=True, default=False)

    @property
    def name(self):
        return self._class_name()

    @staticmethod
    def get_cls_by_name(cls_name):
        return getattr(sys.modules[__name__], cls_name)

    @staticmethod
    def create_from_config(start=None):
        if not start:
            start = config.TECHS

        for k, v in start.iteritems():
            _id = 'TravisReed-%s' % k
            exists = Technology.get_by_id(_id)
            if not exists:
                t = Technology.get_cls_by_name(k).create()
                if k == 'Civilization':
                    t.can_research = True
                    t.put()
            for tree in v:
                Technology.create_from_config(tree)

    @classmethod
    def create(cls):
        return cls()


class Civilization(Technology):
    pass


class GreatLibraryTechnology(Technology):
    pass


class Wheel(Technology):
    pass


class WaterWheel(Technology):
    pass


class Roads(Technology):
    pass


class ResourceManagement(Technology):
    pass


class AnimalHusbandry(Technology):
    pass


class Trapping(Technology):
    pass


class StackBonuses(Technology):
    pass


class Stoneworking(Technology):
    pass


class Axes(Technology):
    pass


class PickAxes(Technology):
    pass


class PyramidTechnology(Technology):
    pass


class StonehengeTechnology(Technology):
    pass


class BronzeWorking(Technology):
    pass


class Archery(Technology):
    pass
