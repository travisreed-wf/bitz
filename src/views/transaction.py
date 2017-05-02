from flask import render_template
from flask.views import MethodView

from src.transactions.transaction import Transaction
from src.workers.worker import Player


class TransactionView(MethodView):

    def get(self):
        transactions = Transaction.query().fetch()
        player = Player.get_by_id("Travis Reed")

        return render_template('transactions.html', transactions=transactions,
                               player=player)


def setup_urls(app):
    app.add_url_rule('/transactions/',
                     view_func=TransactionView.as_view('transactions'))
