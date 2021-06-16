from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import app_config

db = SQLAlchemy()

def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    db.init_app(app)

    @app.get("/ping")
    def pong():
        return "pong"

    from app.route import init_route
    init_route(app)

    migrate = Migrate(app, db)

    return app
