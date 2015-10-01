from flask import render_template, request
from flask.views import MethodView

from src.locations.location import Location
from src.workers.worker import Player

class ClicksView(MethodView):

    def put(self, location_id, tile_index, action_name):
        location = Location.get_by_id(location_id)
        if not location:
            return "Invalid location", 404

        tile = location.tiles[tile_index]
        try:
            player = Player.get_by_id("Travis Reed")
            resources = player.resources
            action = "tile.%s(resources)" % action_name
            eval(tile.action_name)
            player.put()
        except:
            return "Failed", 500

        return "Success", 200


def setup_urls(app):
    app.add_url_rule('/map/location_id>/<tile_index>/<action_name>/',
                     view_func=ClicksView.as_view('clicks'))
