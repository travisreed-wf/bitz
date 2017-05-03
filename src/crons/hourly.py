from flask.views import MethodView

from src.external_data import external_data
from src.resources import resource
from src.workers.worker import Worker, Player


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
        self._update_clash_royale()
        self._update_league_of_legends()
        return 'success', 200

    def _update_clash_royale(self):
        current = external_data.ClashRoyaleData.get_previous_entity()
        if current:
            current_count = current.count
        else:
            current_count = 0
        new = external_data.ClashRoyaleData.update()
        r = resource.ClashRoyaleWins.create(count=(new.count - current_count))
        self.player.add_resource(r)

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
