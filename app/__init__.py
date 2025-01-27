import os
from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

from config import Config

main = Blueprint("main", __name__)

bootstrap = Bootstrap5()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.register_blueprint(main)
    from app import routes
    app.config.from_object(Config)

    bootstrap.init_app(app)
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = os.environ.get("BOOTSTRAP_BOOTSWATCH_THEME")

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app



