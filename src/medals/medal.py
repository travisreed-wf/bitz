from src.locations import location
from src.locations.map import Earth
from src.medals import config


class Medal(object):

    def __init__(self):
        self.tiers = []
        self.rewards = []
        pass

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def class_name(self):
        return self.__class__.__name__

    def calculate_progress(self, player):
        count = self.get_count(player)
        next_tier = self.tiers[0]
        previous_tier = 0
        level = 1
        while count >= next_tier:
            previous_tier = next_tier
            next_tier = self.tiers[level]
            level += 1

        total_in_tier = next_tier - previous_tier
        return level, int(100 * float(count - previous_tier) / total_in_tier)

    def get_count(self, player):
        raise NotImplementedError('must be implemented by subclass')

    def get_reward_description(self, level):
        title = "Rewards Earned:\n"
        try:
            rewards = self.rewards[level-1]
        except IndexError:
            return title + config.DUMMY_REWARD['description']

        title += "\n".join([r['description'] for r in rewards])
        return title

    @staticmethod
    def create_medals():
        medals = []
        for medal_dict in config.TOTAL_RESOURCE_MEDAL_DATA:
            resource_name = medal_dict['resource_name']
            tiers = medal_dict['tiers']
            cls = eval(medal_dict['class_name'])
            rewards = medal_dict['rewards']
            medal = cls(resource_name, tiers=tiers, rewards=rewards)
            medals.append(medal)

        for d in Earth.AVAILABLE_TILES:
            tile_name = d['name']
            medal = ExplorationMedal(tile_name)
            medals.append(medal)
        return medals


class TotalResourceMedal(Medal):

    def __init__(self, resource_name, tiers=None, rewards=None):
        super(TotalResourceMedal, self).__init__()
        self.resource_name = resource_name
        if not tiers:
            tiers = config.STANDARD_TOTAL_RESOURCE_TIERS
        if not rewards:
            rewards = [[config.DUMMY_REWARD]] * 15
        self.tiers = tiers
        self.rewards = rewards

    @property
    def name(self):
        return '%s: %s' % (self.class_name, self.resource_name)

    @property
    def icon_path(self):
        return "resources/%s.png" % self.resource_name

    def get_count(self, player):
        if hasattr(self, "_count"):
            return self._count
        r = player.get_resource_by_name(self.resource_name)
        self._count = r.lifespan_count if r else 0
        return self._count


class TotalEarnedResourceMedal(TotalResourceMedal):

    def __init__(self, resource_name, tiers=None, rewards=None):
        if not tiers:
            tiers = config.STANDARD_TOTAL_EARNED_RESOURCE_TIERS

        super(TotalEarnedResourceMedal, self).__init__(
            resource_name, tiers=tiers, rewards=rewards)


class ExplorationMedal(Medal):

    def __init__(self, tile_name, rewards=None):
        super(ExplorationMedal, self).__init__()
        self.tile_name = tile_name
        self.tiers = config.STANDARD_EXPLORATION_TIERS
        if not rewards:
            reward = 'Great%sScout' % tile_name
            rewards = config.generate_follower_progression_two(reward)
        self.rewards = rewards

    @property
    def icon_path(self):
        return "tiles/%s.png" % self.tile_name

    @property
    def name(self):
        return '%s: %s' % (self.class_name, self.tile_name)

    def get_count(self, player):
        if hasattr(self, "_count"):
            return self._count
        tile_class = eval('location.%s' % self.tile_name)
        self._count = tile_class.query(tile_class.is_explored == True).count()
        return self._count
