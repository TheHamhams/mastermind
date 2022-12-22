from flask import Flask
from config import Config
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS
from .site.routes import site


app = Flask(__name__)
CORS(app)

app.register_blueprint(site)

app.config.from_object(Config)
login_manager.init_app(app)
root_db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)