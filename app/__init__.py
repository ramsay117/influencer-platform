from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "main.login"
    login_manager.login_message = "Please log in to access this page."

    from . import routes

    app.register_blueprint(routes.bp)

    from . import models

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app
