import requests

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.settings import Settings


class ExternalData(polymodel.PolyModel):

    count = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @property
    def name(self):
        return self._class_name()

    @classmethod
    def get_previous_entity(cls):
        return cls.query().order(-cls.date).get()


class ClashRoyaleData(ExternalData):
    pass


class FitbitData(ExternalData):

    @staticmethod
    def update():
        data = FitbitData._get_data()
        entity = FitbitData()
        entity._calculate_count(data)
        entity.put()
        return entity

    @staticmethod
    def _get_data():
        url = 'https://api.fitbit.com/1/user/-/activities.json'
        token = Settings.get_setting_value('FITBIT_TOKEN')
        headers = {"Authorization": "Bearer %s" % token}

        r = requests.get(url, headers=headers)
        return r.json()

    def _calculate_count(self, data):
        self.count = data['lifetime']['total']['steps']


class LeagueOfLegends(ExternalData):
    HALF_WEIGHTING = ['AramUnranked5x5']
    NORMAL_WEIGHTING = ['Unranked3x3', 'Unranked']
    DOUBLE_WEIGHTING = ['RankedFlexSR', 'RankedSolo5x5', 'RankedFlexTT']

    full_payload = ndb.JsonProperty()

    @staticmethod
    def update():
        data = LeagueOfLegends._get_data()
        entity = LeagueOfLegends(full_payload=data)
        entity._calculate_count()
        entity.put()
        return entity

    @staticmethod
    def _get_data():
        url = 'https://na.api.riotgames.com/api/lol/NA/v1.3/' \
              'stats/by-summoner/25757828/summary?season=SEASON2017' \
              '&api_key=RGAPI-6d075dd7-eaa4-4b38-84b0-e1dd4ab39b65'
        r = requests.get(url)
        return r.json()

    def _calculate_count(self):
        self.count = 0
        for summary in self.full_payload.get('playerStatSummaries', []):
            if summary.get('playerStatSummaryType') in self.HALF_WEIGHTING:
                self.count += int(summary['wins'] * .5)
            elif summary.get('playerStatSummaryType') in self.NORMAL_WEIGHTING:
                self.count += int(summary['wins'])
            elif summary.get('playerStatSummaryType') in self.DOUBLE_WEIGHTING:
                self.count += int(summary['wins'] * 2)


class BGAData(ExternalData):
    DOUBLE_WEIGHTING = ['ThroughTheAges']

    full_payload = ndb.JsonProperty()

    def calculate_count(self):
        self.count = 0
        for game_name, wins in self.full_payload.iteritems():
            if game_name in self.DOUBLE_WEIGHTING:
                self.count += wins * 2
            else:
                self.count += wins

    def determine_new_games_won(self, old_game):
        new_wins = []

        if old_game:
            old_data = old_game.full_payload
        else:
            old_data = {}

        for game_name, wins in self.full_payload.iteritems():
            if not wins:
                continue
            if game_name not in old_data:
                new_wins.append(game_name)
                continue

            if wins > old_data[game_name]:
                new_wins.append(game_name)
        return new_wins
