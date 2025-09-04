from flask import Flask
from app.config import Config
from app.extensions import db, ma
from flask_jwt_extended import JWTManager

# Blueprints
from blueprints.auth.routes import auth_bp
from blueprints.users.routes import users_bp
from blueprints.products.routes import products_bp
from blueprints.carts.routes import carts_bp
from blueprints.orders.routes import orders_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    ma.init_app(app)
    JWTManager(app)

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(carts_bp, url_prefix="/carts")
    app.register_blueprint(orders_bp, url_prefix="/orders")

    return app
