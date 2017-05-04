from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from src.views import build, clicks, extension_connectors, factorio, map, \
    transaction
from src.crons import hourly


app = Flask(__name__)
app.debug = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.secret_key = "SecretKey"

toolbar = DebugToolbarExtension(app)

clicks.setup_urls(app)
map.setup_urls(app)
hourly.setup_urls(app)
build.setup_urls(app)
factorio.setup_urls(app)
transaction.setup_urls(app)
extension_connectors.setup_urls(app)
