from flask.views import MethodView

from src.external_data import external_data
from src.medals.medal import Medal
from src.resources import resource
from src.workers.worker import Worker, Player


class FollowerCron(MethodView):

    def get(self):
        self.player = Player.get_by_id("Travis Reed")
        self.possible_followers = self._determine_possible_followers()
        self.followers = self._determine_followers_to_award()

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
        pattern = [float(100)]
        current_odds = float(40)
        for x in xrange(0, 100):
            current_odds = current_odds / 2
            pattern.append(current_odds)

        for possible_follower in self.possible_followers:
            current_count = self.player.get_resource_by_name(
                possible_follower)





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


def setup_urls(app):
    app.add_url_rule('/crons/buildings/',
                     view_func=BuildingCron.as_view('crons.building'))
    app.add_url_rule('/crons/dataRefresh/',
                     view_func=DataRefreshCron.as_view('crons.data'))
    app.add_url_rule('/crons/worker/',
                     view_func=WorkerCron.as_view('crons.worker'))
