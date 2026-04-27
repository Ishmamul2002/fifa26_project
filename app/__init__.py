from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    # Core Blueprints
    from .routes.main import main_bp
    from .routes.user.dashboard import user_bp
    from .routes.admin.dashboard import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)


    # Cart Route
    try:
        from .routes.user.cart import user_cart_bp
        app.register_blueprint(user_cart_bp)
        print("✅ Cart route registered")
    except ImportError:
        print("⚠️ Cart route not found yet")

    # Upcoming Matches Route
    try:
        from .routes.user.matches import user_matches_bp
        app.register_blueprint(user_matches_bp)
        print("✅ Upcoming Matches route registered")
    except ImportError:
        print("⚠️ Upcoming Matches route not found yet")

    # Ticket Booking Route
    try:
        from .routes.user.tickets import user_tickets_bp
        app.register_blueprint(user_tickets_bp)
        print("✅ Ticket booking route registered")
    except ImportError:
        print("⚠️ Ticket booking route not found yet")

    # Hotel Booking Route
    try:
        from .routes.user.hotel import user_hotels_bp
        app.register_blueprint(user_hotels_bp)
        print("✅ Hotel booking route registered")
    except ImportError:
        print("⚠️ Hotel booking route not found yet")

    with app.app_context():
        db.create_all()

    print("✅ FIFA 2026 App started - Clean mode (Tickets + Hotels)")
    return app