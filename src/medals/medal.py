from src.locations import location
from src.locations.map import Earth


class Medal(object):

    TIERS = []

    def __init__(self):
        pass

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def class_name(self):
        return self.__class__.__name__

    def calculate_progress(self, player):
        raise NotImplementedError('must be implemented by subclass')

    def _calculate_progress_from_count(self, count):
        next_tier = self.TIERS[0]
        previous_tier = 0
        level = 1
        while count >= next_tier:
            previous_tier = next_tier
            next_tier = self.TIERS[level]
            level += 1

        total_in_tier = next_tier - previous_tier
        return level, int(100 * float(count - previous_tier) / total_in_tier)

    @staticmethod
    def create_medals():
        medals = []
        for resource_name in ['Production', 'Science', 'Food']:
            medal = TotalResourceMedal(resource_name)
            medals.append(medal)

        earned = ['Dart', 'PoolBall', 'LeagueOfLegendsWin', 'ClashRoyaleWins']
        for resource_name in earned:
            medal = TotalEarnedResourceMedal(resource_name)
            medals.append(medal)

        for d in Earth.AVAILABLE_TILES:
            tile_name = d['name']
            medal = ExplorationMedal(tile_name)
            medals.append(medal)
        return medals


class TotalResourceMedal(Medal):

    def __init__(self, resource_name):
        super(TotalResourceMedal, self).__init__()
        self.resource_name = resource_name

    @property
    def name(self):
        return '%s: %s' % (self.class_name, self.resource_name)

    TIERS = [
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

    def calculate_progress(self, player):
        r = player.get_resource_by_name(self.resource_name)
        count = r.count if r else 0
        return super(TotalResourceMedal, self)._calculate_progress_from_count(
            count)


class TotalEarnedResourceMedal(TotalResourceMedal):

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
        600,
        700,
        800,
        900,
        1000
    ]


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

    def calculate_progress(self, player):
        tile_class = eval('location.%s' % self.tile_name)
        count = tile_class.query(tile_class.is_explored==True).count()
        return super(ExplorationMedal, self)._calculate_progress_from_count(
            count)
