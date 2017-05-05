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
    pass


class GreatSlinger(Follower):
    pass


class GreatCompositeBowman(Follower):
    pass


class GreatSpearman(Follower):
    pass


class GreatPikeman(Follower):
    pass


class GreatLancer(Follower):
    pass


class Tactician(Follower):
    pass


class Strategist(Follower):
    pass


class Commander(Follower):
    pass


class GreatWarrior(Follower):
    pass


class GreatSwordsman(Follower):
    pass


class GreatLongSwordsman(Follower):
    pass
