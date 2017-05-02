import logging
import requests

from bs4 import BeautifulSoup
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from src.exceptions import InsufficientResourcesException
from src.resources import resource
from src.transactions.transaction import Transaction


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

    @staticmethod
    def update():
        count = ClashRoyaleData._get_count()
        entity = ClashRoyaleData(count=count)
        entity.put()
        return entity

    @staticmethod
    def _get_count():
        url = 'https://starfi.re/user/id/5f15e80d-6eab-4752-91f6-86f0c55c98b9'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        return int(soup.find_all(class_='value')[0].text)


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
