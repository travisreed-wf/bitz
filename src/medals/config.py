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

STANDARD_TOTAL_RESOURCE_TIERS = [
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
STANDARD_TOTAL_EARNED_RESOURCE_TIERS = [
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

STANDARD_EXPLORATION_TIERS = [
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


def _generate_follower_progression_one(
        first_class_name, second_class_name, third_class_name):
    r1 = {
        'reward_type': 'follower',
        'name': first_class_name,
        'description': 'Increase odds of generating %s' % first_class_name
    }
    r2 = {
        'reward_type': 'follower',
        'name': second_class_name,
        'description': 'Increase odds of generating %s' % second_class_name
    }
    r3 = {
        'reward_type': 'follower',
        'name': third_class_name,
        'description': 'Increase odds of generating %s' % third_class_name
    }
    l = []
    l += [[r1]] * 3
    l += [[r1, r2]] * 3
    l += [[r1, r2, r3]] * 3
    return l

DUMMY_REWARD = {
    'reward_type': '',
    'name': 'TBA',
    'description': 'Wait for it... its gonna be awesome!'
}


TOTAL_RESOURCE_MEDAL_DATA = [
    {
        'resource_name': 'Production',
        'tiers': None,
        'class_name': 'TotalResourceMedal',
        'rewards': [[DUMMY_REWARD]] * 15,
    },
    {
        'resource_name': 'Science',
        'tiers': None,
        'class_name': 'TotalResourceMedal',
        'rewards': [[DUMMY_REWARD]] * 15,
    },
    {
        'resource_name': 'Food',
        'tiers': None,
        'class_name': 'TotalResourceMedal',
        'rewards': [[DUMMY_REWARD]] * 15,
    },
    {
        'resource_name': 'Dart',
        'tiers': None,
        'class_name': 'TotalEarnedResourceMedal',
        'rewards': _generate_follower_progression_one(
            'GreatSlinger', 'GreatArcher', 'GreatCompositeBowman'),

    },
    {
        'resource_name': 'PoolBall',
        'tiers': None,
        'class_name': 'TotalEarnedResourceMedal',
        'rewards': _generate_follower_progression_one(
            'GreatSpearman', 'GreatPikeman', 'GreatLancer'),
    },
    {
        'resource_name': 'ClashRoyaleWins',
        'tiers': None,
        'class_name': 'TotalEarnedResourceMedal',
        'rewards': _generate_follower_progression_one(
            'Tactician', 'Strategist', 'Commander'),
    },
    {
        'resource_name': 'LeagueOfLegendsWin',
        'tiers': LEAGUE_TIERS,
        'class_name': 'TotalEarnedResourceMedal',
        'rewards': _generate_follower_progression_one(
            'GreatWarrior', 'GreatSwordsman', 'GreatLongswordsman'),
    }
]
