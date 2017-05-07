import json

from flask import render_template
from flask.views import MethodView
from google.appengine.ext import ndb

from src.exceptions import InsufficientResourcesException
from src.locations.location import Location, Tile
from src.workers.worker import Player


class MapView(MethodView):

    def get(self, map_name, location_id):
        location = Location.get_by_id(location_id)
        if not location:
            return "Invalid location", 404
        tiles = ndb.get_multi(location.tiles)
        player = Player.get_by_id("Travis Reed")
        return render_template('map.html', location=location, player=player,
                               tiles=tiles)


class ExploreView(MethodView):

    def get(self, tile_id):
        tile_id = int(tile_id)
        tile = Tile.get_by_id(tile_id)
        player = Player.get_by_id("Travis Reed")
        discout, reason = tile.get_discounted_cost_to_explore(player)

        data = {
            'discount': discout,
            'reason': reason
        }
        return json.dumps(data)

    def post(self, tile_id):
        tile_id = int(tile_id)
        tile = Tile.get_by_id(tile_id)
        player = Player.get_by_id("Travis Reed")
        try:
            used_resources = tile.explore(player)
        except InsufficientResourcesException as e:
            return e.message, 400
        data = {
            'tile_name': tile.name,
            'gained_resources': {},
            'used_resources': {r.name: r.count for r in used_resources}
        }
        return json.dumps(data)


def setup_urls(app):
    app.add_url_rule('/home/',
                     view_func=MapView.as_view('home'),
                     defaults={
                         'map_name': 'Earth', 'location_id': 'E0000x0000'
                     })
    app.add_url_rule('/',
                     view_func=MapView.as_view('empty_route'),
                     defaults={
                         'map_name': 'Earth', 'location_id': 'E0000x0000'
                     })

    app.add_url_rule('/map/<map_name>/<location_id>/',
                     view_func=MapView.as_view('map'))
    app.add_url_rule('/explore/<tile_id>/',
                     view_func=ExploreView.as_view('explore'))
