from src.locations import location
from src.locations.map import Earth


class Medal(object):

    TIERS = []
    LEAGUE_TIERS = [
        1,
        5,
        10,
        25,
        50,
        75,
        100,
        150,
        200,
        250,
        300,
        350,
        400,
        450,
        500
    ]

    def __init__(self):
        pass

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def class_name(self):
        return self.__class__.__name__

    def calculate_progress(self, player):
        count = self.get_count(player)
        next_tier = self.TIERS[0]
        previous_tier = 0
        level = 1
        while count >= next_tier:
            previous_tier = next_tier
            next_tier = self.TIERS[level]
            level += 1

        total_in_tier = next_tier - previous_tier
        return level, int(100 * float(count - previous_tier) / total_in_tier)

    def get_count(self, player):
        raise NotImplementedError('must be implemented by subclass')

    @staticmethod
    def create_medals():
        medals = []
        for resource_name in ['Production', 'Science', 'Food']:
            medal = TotalResourceMedal(resource_name)
            medals.append(medal)

        earned = ['Dart', 'PoolBall', 'ClashRoyaleWins']
        for resource_name in earned:
            medal = TotalEarnedResourceMedal(resource_name)
            medals.append(medal)

        league_medal = TotalEarnedResourceMedal(
            'LeagueOfLegendsWin', tiers=Medal.LEAGUE_TIERS)
        medals.append(league_medal)

        for d in Earth.AVAILABLE_TILES:
            tile_name = d['name']
            medal = ExplorationMedal(tile_name)
            medals.append(medal)
        return medals


class TotalResourceMedal(Medal):

    def __init__(self, resource_name, tiers=None):
        super(TotalResourceMedal, self).__init__()
        self.resource_name = resource_name
        if not tiers:
            tiers = [
                1500,
                10000,
                50000,
                100000,
                500000,
                1000000,
                5000000,
                10000000,
                50000000,
                100000000,
                500000000,
                1000000000
            ]
        self.tiers = tiers

    @property
    def name(self):
        return '%s: %s' % (self.class_name, self.resource_name)

    def get_count(self, player):
        if hasattr(self, "_count"):
            return self._count

        r = player.get_resource_by_name(self.resource_name)
        self._count = r.count if r else 0
        return self._count


class TotalEarnedResourceMedal(TotalResourceMedal):

    def __init__(self, resource_name, tiers=None):
        if not tiers:
            tiers = [
                1,
                5,
                10,
                25,
                50,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000
            ]

        super(TotalEarnedResourceMedal, self).__init__(
            resource_name, tiers=tiers)


class ExplorationMedal(Medal):

    def __init__(self, tile_name):
        super(ExplorationMedal, self).__init__()
        self.tile_name = tile_name

    @property
    def name(self):
        return '%s: %s' % (self.class_name, self.tile_name)

    TIERS = [
        1,
        5,
        10,
        25,
        50,
        100,
        200,
        300,
        400,
        500,
        600
    ]

    def get_count(self, player):
        if hasattr(self, "_count"):
            return self._count

        tile_class = eval('location.%s' % self.tile_name)
        self._count = tile_class.query(tile_class.is_explored==True).count()
        return self._count
