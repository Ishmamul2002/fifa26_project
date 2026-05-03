from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import models first
    with app.app_context():
        from . import models

        # Import Blueprints
        from .routes.main import main_bp
        from .routes.auth import auth_bp
        from .routes.user.dashboard import user_bp
        from .routes.admin.dashboard import admin_bp
        from .routes.user.analytics import analytics_bp
        from .routes.user.teams import teams_bp
        from .routes.user.players import players_bp   # ← New Player Module

        # Register Blueprints
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(user_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(analytics_bp)
        app.register_blueprint(teams_bp)
        app.register_blueprint(players_bp)            # ← Registered here

    # User Loader
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    # Create tables
    with app.app_context():
        db.create_all()

    print("✅ FIFA 2026 App started successfully!")
    return app