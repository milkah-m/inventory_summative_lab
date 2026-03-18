# Import Flask
# Create the app instance
# Set a secret key (pulling it from .env — but for now you can just hardcode a placeholder string, we'll move it to .env properly later)
# Import routes at the bottom

from flask import Flask

app = Flask(__name__)
app.secret_key = "dev_secret_key"
app.json.sort_keys = False

from . import routes


