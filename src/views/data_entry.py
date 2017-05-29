from flask import request, render_template
from flask.views import MethodView

from src.resources import resource
from src.workers.worker import Player


class AddDartsView(MethodView):

    def get(self):
        player = Player.get_by_id("Travis Reed")
        return render_template('add_darts.html', player=player)

    def post(self):
        data = request.form
        wins = int(data.get('wins') or 0)
        bulls = int(data.get('bulls') or 0)
        game_type = data.get('game_type')
        gotchas = int(data.get('gotchas') or 0)
        r = resource.Dart.create_based_on_results(
            wins=wins, bulls=bulls, gotchas=gotchas, game_type=game_type)
        player = Player.get_by_id("Travis Reed")
        player.add_resource(r, reason='Played Darts')
        return "Congrats! You earned %s points" % r.count, 200


class AddPoolView(MethodView):

    def get(self):
        player = Player.get_by_id("Travis Reed")
        return render_template('add_pool.html', player=player)

    def post(self):
        data = request.form
        wins = int(data.get('wins') or 0)
        balls = int(data.get('balls') or 0)
        lags = int(data.get('lags') or 0)
        r = resource.PoolBall.create_based_on_results(
            wins=wins, balls=balls, lags=lags)
        player = Player.get_by_id("Travis Reed")
        player.add_resource(r, reason='Played Pool')
        return "Congrats! You earned %s points" % r.count, 200


def setup_urls(app):
    app.add_url_rule('/data_entry/darts/',
                     view_func=AddDartsView.as_view('add_darts'))
    app.add_url_rule('/data_entry/pool/',
                     view_func=AddPoolView.as_view('add_pool'))
