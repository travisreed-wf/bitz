from flask import request, render_template
from flask.views import MethodView

from src.resources import resource
from src.workers.worker import Player


class AddDartsView(MethodView):

    def get(self):
        player = Player.get_by_id("Travis Reed")
        return render_template('add_darts.html', player=player)

    def post(self):
        print request.form
        return "Success", 200


def setup_urls(app):
    app.add_url_rule('/data_entry/darts/',
                     view_func=AddDartsView.as_view('add_darts'))
