from flask import Flask
from .config import Config
from flask_migrate import Migrate
from .models import db as root_db, login_manager
from flask_cors import CORS
from .site.routes import site
from .authentication.routes import auth
from .game.routes import game
from .api.routes import api

app = Flask(__name__)
CORS(app)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(game)
app.register_blueprint(api)

app.config.from_object(Config)
login_manager.init_app(app)
root_db.init_app(app)
migrate = Migrate(app, root_db)