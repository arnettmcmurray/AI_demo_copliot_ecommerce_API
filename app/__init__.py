from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate, ma, jwt

# Import blueprints here
from blueprints.auth import bp as auth_bp
from blueprints.users import bp as users_bp
from blueprints.products import bp as products_bp
from blueprints.carts import bp as carts_bp
from blueprints.orders import bp as orders_bp
from util.error_handlers import register_error_handlers

def create_app(config_object="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(carts_bp, url_prefix="/carts")
    app.register_blueprint(orders_bp, url_prefix="/orders")

    # Error handlers
    register_error_handlers(app)

    return app
