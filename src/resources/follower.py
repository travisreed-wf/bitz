import sys

from src.resources import resource


class Follower(resource.Resource):

    @classmethod
    def create(cls, count=0):
        return cls(resource_type='follower', count=count)

    @staticmethod
    def get_class_by_name(cls_name):
        return getattr(sys.modules[__name__], cls_name)

    @property
    def action_names(self):
        return [d['name'] for d in self.actions]

    @property
    def actions(self):
        return []


class GreatArcher(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of Archers'

    @property
    def actions(self):
        return [{
            'name': 'Improve Archers',
            'info_needed': {}
        }]


class GreatSlinger(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Slingers'

    @property
    def actions(self):
        return [{
            'name': 'Improve Slingers',
            'info_needed': {}
        }]


class GreatCompositeBowman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Composite Bowmen'

    @property
    def actions(self):
        return [{
            'name': 'Improve CompositeBowmen',
            'info_needed': {}
        }]


class GreatSpearman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Spearmen'

    @property
    def actions(self):
        return [{
            'name': 'Improve Spearmen',
            'info_needed': {}
        }]


class GreatPikeman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Pikemen'

    @property
    def actions(self):
        return [{
            'name': 'Improve Pikemen',
            'info_needed': {}
        }]


class GreatLancer(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Lancers'

    @property
    def actions(self):
        return [{
            'name': 'Improve Lancers',
            'info_needed': {}
        }]


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
        }]


class GreatSwordsman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Swordsmen'

    @property
    def actions(self):
        return [{
            'name': 'Improve Swordsmen',
            'info_needed': {}
        }]


class GreatLongSwordsman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'LongSwordsmen'

    @property
    def actions(self):
        return [{
            'name': 'Improve LongSwordsmen',
            'info_needed': {}
        }]


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
                }
            },
            {
                'name': 'Improve Science Building',
                'info_needed': {
                    'name': 'Science Building Name',
                    'options': ['Library']
                }
            }
        ]


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
                }
            },
            {
                'name': 'Improve Industrial Building',
                'info_needed': {
                    'name': 'Building Name',
                    'options': ['Mine']
                }
            }
        ]


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
                'info_needed': {}
            }
        ]


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
                'info_needed': {}
            }
        ]
