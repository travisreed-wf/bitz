import sys

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.resources.resource import Science
from src.producers import wonder


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

    def process_researched(self, player):
        return  # TODO for all subclasses

    def research(self, player):
        player.add_resources(self.cost, reason='Researching %s' % self.name)
        self.is_researched = True
        self.can_research = False
        for child in self.children:
            child.can_research = True
            child.put()
        self.put()
        self.process_researched(player)
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
        return "Unlocks building the 'GreatLibrary' which provides a " \
               "free 'GreatScientist'"

    @property
    def cost(self):
        return [Science.create(count=15000)]

    def process_researched(self, player):
        r = wonder.GreatLibrary.create(count=0)
        player.add_resource(r)




class Wheel(Technology):

    @property
    def description(self):
        return "Reveals 'grain' and allows the production of a 'mill' " \
               "which provides food"

    @property
    def cost(self):
        return [Science.create(count=15000)]


class WaterWheel(Technology):

    @property
    def description(self):
        return "Allow you to build watermills on river tiles, which " \
               "generate production and food"

    @property
    def cost(self):
        return [Science.create(count=150000)]


class Roads(Technology):

    @property
    def description(self):
        return "Allow you to build roads on tiles to reduce " \
               "the movement cost through them"

    @property
    def cost(self):
        return [Science.create(count=150000)]


class ResourceManagement(Technology):

    @property
    def description(self):
        return "Reveal 'horses' on some grassland tiles"

    @property
    def cost(self):
        return [Science.create(count=15000)]


class AnimalHusbandry(Technology):
    @property
    def description(self):
        return "Allows the creation of pastures on horse tiles. " \
               "Pastures generate production"

    @property
    def cost(self):
        return [Science.create(count=150000)]


class Trapping(Technology):

    @property
    def description(self):
        return "Reveals rabbits on the map, which can be hunted for Food"

    @property
    def cost(self):
        return [Science.create(count=1000000)]


class StackBonuses(Technology):

    @property
    def description(self):
        return "Adds stack bonuses if a tile is completely full of buildings"

    @property
    def cost(self):
        return [Science.create(count=150000)]


class Stoneworking(Technology):

    @property
    def description(self):
        return "Reveals 'Stone' on your map if you have also researched " \
               "'ResourceManagement'. Stone automatically reduces " \
               "the production cost of buildings on that tile by 30%. " \
               "Certain buildings can only be built on stone."

    @property
    def cost(self):
        return [Science.create(count=15000)]


class Axes(Technology):

    @property
    def description(self):
        return "Allows you to chop down trees to make grassland or plains"

    @property
    def cost(self):
        return [Science.create(count=150000)]


class PickAxes(Technology):

    @property
    def description(self):
        return "Improves each of your mines to double their production"

    @property
    def cost(self):
        return [Science.create(count=1000000)]


class PyramidTechnology(Technology):

    @property
    def description(self):
        return "Unlocks the wonder 'Pyramids' for production. " \
               "Pyramids provide a free GreatLaborer"

    @property
    def cost(self):
        return [Science.create(count=5000000)]


class StonehengeTechnology(Technology):

    @property
    def description(self):
        return "Unlocks the wonder Stonehenge for production. " \
               "Stonehenge provides the ability to research alien technology"

    @property
    def cost(self):
        return [Science.create(count=5000000)]


class BronzeWorking(Technology):

    @property
    def description(self):
        return "Reveals 'bronze' on your map if you have also researched " \
               "'ResourceManagement' Bronze improves the production of " \
               "your mines significantly"

    @property
    def cost(self):
        return [Science.create(count=5000000)]


class Archery(Technology):

    @property
    def description(self):
        return "Unlocks archers and hunter camps"

    @property
    def cost(self):
        return [Science.create(count=150000)]
