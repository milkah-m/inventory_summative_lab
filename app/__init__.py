

from flask import Flask

app = Flask(__name__)
app.json.sort_keys = False

from . import routes


