import sys

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.resources.resource import Science
from src.technologies import config


class Technology(polymodel.PolyModel):
    can_research = ndb.BooleanProperty(indexed=True, default=False)
    is_researched = ndb.BooleanProperty(indexed=True, default=False)
    parent_key = ndb.KeyProperty(indexed=True)

    @property
    def children(self):
        return Technology.query(Technology.parent_key == self.key).fetch()

    @property
    def name(self):
        return self._class_name()

    @property
    def cost(self):
        raise NotImplementedError("subclass this")

    @staticmethod
    def get_cls_by_name(cls_name):
        return getattr(sys.modules[__name__], cls_name)

    @staticmethod
    def create_from_config(start, parent_key=None):
        for k, v in start.iteritems():
            _id = 'TravisReed-%s' % k
            cls = Technology.get_cls_by_name(k)
            t = cls.get_or_insert(_id, parent_key=parent_key)
            if k == 'Civilization':
                t.can_research = True
                t.put()
            Technology.create_from_config(v, parent_key=t.key)

    @classmethod
    def get_by_player(cls, player):
        player_name = player.key.id().replace(' ', '')
        return cls.get_by_id('%s-%s' % (player_name, cls.__name__))

    def process_researched(self):
        return  # TODO for all subclasses

    def research(self, player):
        player.add_resources(self.cost, reason='Researching %s' % self.name)
        self.is_researched = True
        self.can_research = False
        for child in self.children:
            child.can_research = True
            child.put()
        self.put()
        self.process_researched()
        return self.cost


class Civilization(Technology):

    @property
    def description(self):
        return "Starting technology to show you the ropes"

    @property
    def cost(self):
        return [Science.create(count=1)]


class GreatLibraryTechnology(Technology):

    @property
    def description(self):
        return "Unlocks building the GreatLibrary"

    @property
    def cost(self):
        return [Science.create(count=15000)]


class Wheel(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=15000)]


class WaterWheel(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=75000)]


class Roads(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=75000)]


class ResourceManagement(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=15000)]


class AnimalHusbandry(Technology):
    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=75000)]


class Trapping(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=250000)]


class StackBonuses(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=75000)]


class Stoneworking(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=15000)]


class Axes(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=75000)]


class PickAxes(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=250000)]


class PyramidTechnology(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=500000)]


class StonehengeTechnology(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=500000)]


class BronzeWorking(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=500000)]


class Archery(Technology):

    @property
    def description(self):
        return "TBD... it will be cool though"

    @property
    def cost(self):
        return [Science.create(count=75000)]
