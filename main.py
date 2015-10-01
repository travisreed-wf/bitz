from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from src.views import clicks, map


app = Flask(__name__)
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.secret_key = "SecretKey"

toolbar = DebugToolbarExtension(app)

clicks.setup_urls(app)
map.setup_urls(app)
