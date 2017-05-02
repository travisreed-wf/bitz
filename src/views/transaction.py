from flask import render_template
from flask.views import MethodView

from src.transactions.transaction import Transaction


class TransactionView(MethodView):

    def get(self):
        transactions = Transaction.query().fetch()

        return render_template('transactions.html', transactions=transactions)


def setup_urls(app):
    app.add_url_rule('/factorio/rockets/',
                     view_func=TransactionView.as_view('transactions'))
