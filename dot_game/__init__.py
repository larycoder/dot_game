from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from dot_game.setup import config

app = Flask(__name__)

# load setting to app
app.config.update(config)

# load database
db = SQLAlchemy(app)

# load bcrypt
bcrypt = Bcrypt(app)

# load view
from dot_game.controller.view import core_blueprint
app.register_blueprint(core_blueprint)