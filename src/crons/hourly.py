from flask.views import MethodView

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


def setup_urls(app):
    app.add_url_rule('/crons/buildings/',
                     view_func=BuildingCron.as_view('crons.building'))
