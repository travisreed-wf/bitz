import sys

from google.appengine.ext import ndb

from src.exceptions import InsufficientResourcesException
from src.locations.map import Earth
from src.producers import building
from src.resources import resource


class Follower(resource.Resource):

    free_count = ndb.IntegerProperty(default=0)

    @classmethod
    def create(cls, count=0):
        return cls(resource_type='follower', count=count)

    @property
    def current_randomly_awarded_count(self):
        return self.lifespan_count - self.free_count

    @staticmethod
    def get_class_by_name(cls_name):
        return getattr(sys.modules[__name__], cls_name)

    @property
    def action_names(self):
        return [d['name'] for d in self.actions]

    @property
    def actions(self):
        return []

    def improve_building(self, player, building):
        player.improve_building(building)
        cls = Follower.get_class_by_name(self.name)
        f = cls.create(count=-1)
        player.add_resource(f, reason='Spent to improve %s' % building)
        return

    def improve_unit(self, player, unit):
        # TODO
        raise NotImplementedError("coming soon!")


class GreatArcher(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of Archers'

    @property
    def actions(self):
        return [{
            'name': 'Improve Archers',
            'info_needed': {},
            'function_name': 'improve_archers'
        }]

    def improve_archers(self, player):
        self.improve_unit(player, 'Archer')


class GreatSlinger(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Slingers'

    @property
    def actions(self):
        return [{
            'name': 'Improve Slingers',
            'info_needed': {},
            'function_name': 'improve_slingers'
        }]

    def improve_slingers(self, player):
        self.improve_unit(player, 'Slinger')


class GreatCompositeBowman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Composite Bowmen'

    @property
    def actions(self):
        return [{
            'name': 'Improve CompositeBowmen',
            'info_needed': {},
            'function_name': 'improve_composite_bowmen'
        }]

    def improve_composite_bowmen(self, player):
        self.improve_unit(player, 'CompositeBowman')


class GreatSpearman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Spearmen'

    @property
    def actions(self):
        return [{
            'name': 'Improve Spearmen',
            'info_needed': {},
            'function_name': 'improve_spearmen'
        }]

    def improve_spearmen(self, player):
        self.improve_unit(player, 'Spearman')


class GreatPikeman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Pikemen'

    @property
    def actions(self):
        return [{
            'name': 'Improve Pikemen',
            'info_needed': {},
            'function_name': 'improve_pikemen'
        }]

    def improve_pikemen(self, player):
        self.improve_unit(player, 'Pikeman')


class GreatLancer(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Lancers'

    @property
    def actions(self):
        return [{
            'name': 'Improve Lancers',
            'info_needed': {},
            'function_name': 'improve_lancers'
        }]

    def improve_lancers(self, player):
        self.improve_unit(player, 'Lancer')


class Tactician(Follower):

    @property
    def description(self):
        return 'Permanently improves the performance of your ' \
               'entire Army'


class Strategist(Follower):

    @property
    def description(self):
        return 'Permanently improves the performance of your ' \
               'entire Army'


class Commander(Follower):

    @property
    def description(self):
        return 'Permanently improves the performance of your ' \
               'entire Army'


class GreatWarrior(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Warriors'

    @property
    def actions(self):
        return [{
            'name': 'Improve Warriors',
            'info_needed': {},
            'function_name': 'improve_warriors'
        }]

    def improve_warriors(self, player):
        self.improve_unit(player, 'Warrior')


class GreatSwordsman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Swordsmen'

    @property
    def actions(self):
        return [{
            'name': 'Improve Swordsmen',
            'info_needed': {},
            'function_name': 'improve_swordsmen'
        }]

    def improve_swordsmen(self, player):
        self.improve_unit(player, 'Swordsman')


class GreatLongSwordsman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'LongSwordsmen'

    @property
    def actions(self):
        return [{
            'name': 'Improve LongSwordsmen',
            'info_needed': {},
            'function_name': 'improve_longswordmen'
        }]

    def improve_longswordsmen(self, player):
        self.improve_unit(player, 'Longswordsmen')


class GreatHillsScout(Follower):

    @property
    def description(self):
        return 'Reduces the exploration cost when passing through Hills'

    @property
    def discounted_tile(self):
        return 'Hills'


class GreatRiverScout(Follower):

    @property
    def description(self):
        return 'Reduces the exploration cost when passing through River'

    @property
    def discounted_tile(self):
        return 'River'


class GreatMountainScout(Follower):

    @property
    def description(self):
        return 'Reduces the exploration cost when passing through Mountain'

    @property
    def discounted_tile(self):
        return 'Mountain'


class GreatGrasslandScout(Follower):

    @property
    def description(self):
        return 'Reduces the exploration cost when passing through Grassland'

    @property
    def discounted_tile(self):
        return 'Grassland'


class GreatTreesScout(Follower):

    @property
    def description(self):
        return 'Reduces the exploration cost when passing through Trees'

    @property
    def discounted_tile(self):
        return 'Trees'


class GreatScout(Follower):

    @property
    def description(self):
        return ''


class GreatScientist(Follower):

    @property
    def description(self):
        return 'Can be spent to research a technology or permanently ' \
               'increase your science output'

    @property
    def actions(self):
        return [
            {
                'name': 'Research Technology',
                'info_needed': {
                    'name': 'Technology Name',
                    'options': []
                },
                'function_name': 'research_technology'
            },
            {
                'name': 'Improve Science Building',
                'info_needed': {
                    'name': 'Science Building Name',
                    'options': ['Library']
                },
                'function_name': 'improve_building'
            }
        ]

    def research_technology(self, player, technology):
        # TODO
        raise NotImplementedError("coming soon!")


class GreatEngineer(Follower):

    @property
    def description(self):
        return 'Can be spent to build a great wonder or permanently ' \
               'increase your production'

    @property
    def actions(self):
        return [
            {
                'name': 'Build Wonder',
                'info_needed': {
                    'name': 'Wonder Name',
                    'options': ['Great Library']
                },
                'function_name': 'build_wonder'
            },
            {
                'name': 'Improve Industrial Building',
                'info_needed': {
                    'name': 'Building Name',
                    'options': ['Mine']
                },
                'function_name': 'improve_building'
            }
        ]

    def build_wonder(self, player, wonder_name):
        map = Earth
        wonder = building.Building.get_class_by_name(wonder_name).create(
            count=1)
        if wonder.get_max_discounted_buildings(map) < 1:
            raise InsufficientResourcesException(
                "You havent assigned any space for this wonder")

        player.add_resource(
            wonder, reason='Used great engineer to build %s' % wonder_name)
        return


class GreatLaborer(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'your mines'

    @property
    def actions(self):
        return [
            {
                'name': 'Improve Mines',
                'info_needed': {},
                'function_name': 'improve_mines'
            }
        ]

    def improve_mines(self, player):
        return self.improve_building(player, 'Mine')


class GreatFarmer(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance ' \
               'of your granaries'

    @property
    def actions(self):
        return [
            {
                'name': 'Improve Granary',
                'info_needed': {},
                'function_name': 'improve_granary'
            }
        ]

    def improve_granary(self, player):
        self.improve_building(player, 'Granary')
