from flask import request
from flask.views import MethodView
import traceback

from src.resources import resource
from src.workers.worker import Player


class FactorioRocketsView(MethodView):

    def put(self):
        rocket_count = int(request.args.get('rockets'))

        try:
            player = Player.get_by_id("Travis Reed")
            rocket = resource.Rocket.create(rocket_count)
            player.add_resource(rocket)
            player.put()
        except:
            print traceback.format_exc()
            return "Failed", 500

        return str(player.get_resource_by_name('Rocket').count), 200


def setup_urls(app):
    app.add_url_rule('/factorio/rockets/',
                     view_func=FactorioRocketsView.as_view('factorio_rockets'))
