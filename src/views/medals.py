import math

from flask import render_template
from flask.views import MethodView

from src.medals.medal import Medal
from src.workers.worker import Player


class MedalsView(MethodView):

    def get(self):
        medals = Medal.create_medals()

        player = Player.get_by_id("Travis Reed")
        mpr = math.ceil(math.sqrt(len(medals)))
        return render_template(
            'medals.html', player=player, medals=medals, medals_per_row=mpr)


def setup_urls(app):

    app.add_url_rule('/medals/', view_func=MedalsView.as_view('medals'))
