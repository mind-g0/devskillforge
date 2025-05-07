import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    from src.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from src.routes.main import main_bp
    app.register_blueprint(main_bp)

    from src.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from src.routes.challenges import challenges_bp
    app.register_blueprint(challenges_bp)

    from src.routes.admin import admin_bp # Added admin_bp import
    app.register_blueprint(admin_bp) # Registered admin_bp

    with app.app_context():
        db.create_all() # Create tables if they don\"t exist

    return app

