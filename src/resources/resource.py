from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Resource(polymodel.PolyModel):
    count = ndb.FloatProperty(indexed=False)
    lifespan_count = ndb.FloatProperty(indexed=False, default=0)
    tool_needed = ndb.StringProperty()
    resource_type = ndb.StringProperty()

    @property
    def name(self):
        return self._class_name()

    @property
    def serialize(self):
        d = self.to_dict()
        d['name'] = self.name
        return d

    def clone(self, **extra_args):
        """
        Clones the entity and returns an un-put instance of it.
        The id of the entity being copied is not copied over to clone.
        Usage:
        hook = GithubHook.query(...).get()
        cloned_hook = hook.clone()
        cloned_hook.put()

        Code taken from:
        http://stackoverflow.com/questions/2687724/copy-an-entity-in-
        google-app-engine-datastore-in-python-without-knowing-property
        ?answertab=votes#tab-top
        """
        klass = self.__class__
        properties = {}
        for v in klass._properties.itervalues():
            if type(v) is not ndb.ComputedProperty and \
                    type(v) is not polymodel._ClassKeyProperty:
                properties[v._code_name] = v.__get__(self, klass)
        properties.update(extra_args)
        return klass(**properties)


class ClashRoyaleWins(Resource):

    @staticmethod
    def create(count=0):
        return ClashRoyaleWins(resource_type="earned", count=count)


class BGAWins(Resource):

    @staticmethod
    def create(count=0):
        return BGAWins(resource_type="earned", count=count)


class Dart(Resource):

    @staticmethod
    def create(count=0):
        return Dart(resource_type="earned", count=count)

    @staticmethod
    def create_based_on_results(wins=0, bulls=0, gotchas=0, game_type='301'):
        if game_type == '301':
            count = wins * .75 + gotchas * .25
        elif game_type == 'cricket':
            count = wins + bulls * .25
        else:
            count = wins * .75
        return Dart.create(count)


class Food(Resource):
    freshness = ndb.FloatProperty()

    @staticmethod
    def create(count=0):
        return Food(resource_type="basic", count=count)


class Gold(Resource):

    @staticmethod
    def create(count=0):
        return Gold(resource_type="basic", count=count)


class Health(Resource):

    @staticmethod
    def create(count=0):
        return Health(resource_type="basic", count=count)


class HearthstoneCard(Resource):

    @staticmethod
    def create(count=0):
        return HearthstoneCard(resource_type="earned", count=count)

    @staticmethod
    def create_based_on_results(arean_wins=0, play_mode_wins=0, legendaries=0):
        count = arean_wins * 2 + play_mode_wins * 1 + legendaries * 10
        return HearthstoneCard.create(count)


class LeagueOfLegendsWin(Resource):

    @staticmethod
    def create(count=0):
        return LeagueOfLegendsWin(resource_type="earned", count=count)


class PoolBall(Resource):

    @staticmethod
    def create(count=0):
        return PoolBall(resource_type="earned", count=count)

    @staticmethod
    def create_based_on_results(wins=0, balls=0, lags=0):
        count = wins + (balls * .1 + lags * .2)
        return PoolBall.create(count)


class Production(Resource):

    @staticmethod
    def create(count=0):
        return Production(resource_type='basic', count=count)


class Rocket(Resource):

    @staticmethod
    def create(count=0):
        return Rocket(resource_type='earned', count=count)


class Science(Resource):

    @staticmethod
    def create(count=0):
        return Science(resource_type='basic', count=count)


class Step(Resource):

    @staticmethod
    def create(count=0):
        return Step(resource_type="earned", count=count)
