import logging

from random import random
from flask.views import MethodView

from src.external_data import external_data
from src.medals.medal import Medal
from src.resources import resource
from src.resources.follower import Follower
from src.settings import Settings
from src.workers.worker import Worker, Player


class FollowerCron(MethodView):

    def __init__(self):
        self.player = Player.get_by_id("Travis Reed")
        self.possible_followers = []
        self.followers = []
        self.reason = 'it was attracted by your medals.'
        self.is_free = False

    def get(self):
        self.possible_followers = self._determine_possible_followers()
        self.followers = self._determine_followers_to_award()
        for follower_name in self.followers:
            logging.info("Awarding %s" % follower_name)
            follower_cls = Follower.get_class_by_name(follower_name)
            follower = follower_cls.create(count=1)
            self.player.add_follower(follower, self.is_free,
                                     reason=self.reason)
        return "Success"

    def _determine_possible_followers(self):
        medals = Medal.create_medals()
        followers = []
        for medal in medals:
            level, _ = medal.calculate_progress(self.player)
            for achieved_level in xrange(1, level):
                try:
                    rewards = medal.rewards[achieved_level - 1]
                except IndexError:
                    rewards = []
                for reward in rewards:
                    if reward['reward_type'] == 'follower':
                        followers.append(reward['name'])
        return followers

    def _determine_followers_to_award(self):
        raise NotImplementedError("must be implemented by subclass")


class FollowerCronForNewMedals(FollowerCron):

    def __init__(self):
        super(FollowerCronForNewMedals, self).__init__()
        self.reason = "you received a new medal!"
        self.is_free = True

    def _determine_followers_to_award(self):
        followers_to_award = []

        for possible_follower in set(self.possible_followers):
            follower = self.player.get_resource_by_name(
                possible_follower)
            if follower:
                current_free_count = follower.free_count
            else:
                current_free_count = 0
            exp_count = self.possible_followers.count(possible_follower)

            if current_free_count < exp_count:
                followers_to_award.append(possible_follower)

        return followers_to_award


class DailyFollowerCron(FollowerCron):

    def _determine_followers_to_award(self):
        pattern = self._generate_pattern()

        followers_to_award = []

        for possible_follower in set(self.possible_followers):
            follower = self.player.get_resource_by_name(
                possible_follower)
            current_randomly_awarded_count = \
                follower.current_randomly_awarded_count if follower else 0
            odds_index = current_randomly_awarded_count
            follower_points = self.possible_followers.count(possible_follower)
            odds_index -= follower_points

            if odds_index < 0:
                odds_index = 0

            follower_specifc_odd = pattern[int(odds_index)]

            logging.info('Because you have {current_count} {name}s and '
                         'have earned {follower_points} {name} points, '
                         'the odds of attracting a new {name} are {odds}'.
                         format(current_count=current_randomly_awarded_count,
                                name=follower.name,
                                follower_points=follower_points,
                                odds=follower_specifc_odd))

            r = random()
            logging.info('Random number generated: %s' % r)
            if follower_specifc_odd >= r:
                followers_to_award.append(possible_follower)
                logging.info('Congrats on being awarded a %s!' % follower.name)
        return followers_to_award

    def _generate_pattern(self):
        pattern = []
        current_odds = float(.4)
        for x in xrange(0, 100):
            current_odds /= 2
            pattern.append(current_odds)
        return pattern


class WorkerCron(MethodView):

    def get(self):
        WorkerCron._check_basic_needs()

        return 'Success', 200

    @staticmethod
    def _check_basic_needs():
        workers = Worker.query().fetch()
        for worker in workers:
            worker.check_basic_needs()


class BuildingCron(MethodView):

    def get(self):
        player = Player.get_by_id("Travis Reed")
        for building in player.buildings:
            if building.should_produce():
                produced_resources = building.produce()
                player.add_resources(produced_resources,
                                     reason='produced by %s' % building.name)
        return 'Success', 200


class DataRefreshCron(MethodView):

    def get(self):
        self.player = Player.get_by_id('Travis Reed')
        self._update_league_of_legends()
        self._update_fitbit()
        self._update_jira()
        self._update_github()
        return 'success', 200

    def _update_league_of_legends(self):
        current = external_data.LeagueOfLegends.get_previous_entity()
        if current:
            current_count = current.count
        else:
            current_count = 0
        new = external_data.LeagueOfLegends.update()
        r = resource.LeagueOfLegendsWin.create(
            count=(new.count - current_count))
        self.player.add_resource(r)

    def _update_fitbit(self):
        current = external_data.FitbitData.get_previous_entity()
        if current:
            current_count = current.count
        else:
            current_count = 0
        new = external_data.FitbitData.update()
        r = resource.Step.create(
            count=(new.count - current_count))
        self.player.add_resource(r)

    def _update_jira(self):
        current = external_data.JIRA.get_previous_entity()
        if current:
            current_count = current.count or 0
        else:
            current_count = 0
        new = external_data.JIRA.update()
        if new:
            r = resource.JIRAPoint.create(
                count=(new.count - current_count))
            self.player.add_resource(r)

    def _update_github(self):
        current = external_data.GithubData.get_previous_entity()
        if current:
            current_count = current.count
        else:
            current_count = 0
        new = external_data.GithubData.update()
        if new:
            r = resource.GitCommit.create(
                count=(new.count - current_count))
            self.player.add_resource(r)


def setup_urls(app):
    app.add_url_rule('/crons/buildings/',
                     view_func=BuildingCron.as_view('crons.building'))
    app.add_url_rule('/crons/dataRefresh/',
                     view_func=DataRefreshCron.as_view('crons.data'))
    app.add_url_rule('/crons/worker/',
                     view_func=WorkerCron.as_view('crons.worker'))
    app.add_url_rule('/crons/follower/daily/',
                     view_func=DailyFollowerCron.as_view(
                         'crons.follower.daily'))
    app.add_url_rule('/crons/follower/new_medals/',
                     view_func=FollowerCronForNewMedals.as_view(
                         'crons.follower.new_medals'))
