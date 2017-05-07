import sys

from src.resources import resource


class Follower(resource.Resource):

    @classmethod
    def create(cls, count=0):
        return cls(resource_type='follower', count=count)

    @staticmethod
    def get_class_by_name(cls_name):
        return getattr(sys.modules[__name__], cls_name)


class GreatArcher(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of Archers'


class GreatSlinger(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Slingers'


class GreatCompositeBowman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Composite Bowmen'


class GreatSpearman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Spearmen'


class GreatPikeman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Pikemen'


class GreatLancer(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Lancers'


class Tactician(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of your ' \
               'entire Army'


class Strategist(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of your ' \
               'entire Army'


class Commander(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of your ' \
               'entire Army'


class GreatWarrior(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Warriors'


class GreatSwordsman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'Swordsmen'


class GreatLongSwordsman(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'LongSwordsmen'


class GreatHillsScout(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the tile bonus for 1 tile'


class GreatRiverScout(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the tile bonus for 1 tile'


class GreatMountainScout(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the tile bonus for 1 tile'


class GreatGrasslandScout(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the tile bonus for 1 tile'


class GreatTreesScout(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the tile bonus for 1 tile'


class GreatScout(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the tile bonus for 1 tile'


class GreatScientist(Follower):

    @property
    def description(self):
        return 'Can be spent to research a technology or permanently ' \
               'increase your <b>science output</b>'


class GreatEngineer(Follower):

    @property
    def description(self):
        return 'Can be spent to build a great wonder or permanently ' \
               'increase your <b>production</b>'


class GreatLaborer(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance of ' \
               'your mines'


class GreatFarmer(Follower):

    @property
    def description(self):
        return 'Can be spent to permanently improve the performance ' \
               'of your granaries'
