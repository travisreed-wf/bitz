from flask import render_template, request
from flask.views import MethodView
from google.appengine.ext import ndb


from src.locations import map
from src.locations.location import Location
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


def setup_urls(app):
    app.add_url_rule('/map/<map_name>/<location_id>/',
                     view_func=MapView.as_view('map'))
