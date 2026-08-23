from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config


db = SQLAlchemy()

login_manager = LoginManager()

login_manager.login_view = "admin.login"


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)

    from app.routes import main
    from app.admin import admin

    app.register_blueprint(main)
    app.register_blueprint(admin)

    with app.app_context():
        from app.models import Admin, Project, Skill, Service
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(
            Admin,
            int(user_id)
        )

    return app