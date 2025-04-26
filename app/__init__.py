from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from app.src.utils.config import Config

bootstrap = Bootstrap5()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, )
    app.config.from_object(Config)
    db.init_app(app)
    from .src.routes import main
    app.register_blueprint(main)
    bootstrap.init_app(app)
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = "Journal"
    with app.app_context():
        db.create_all()
    return app



