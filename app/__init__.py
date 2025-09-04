from flask import Flask
from .extensions import db, ma, migrate, jwt, swagger
from .config import Config
from .blueprints.users import users_bp
from .blueprints.products import products_bp
from .blueprints.carts import carts_bp
from .blueprints.orders import orders_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)

    # register blueprints
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(carts_bp, url_prefix="/carts")
    app.register_blueprint(orders_bp, url_prefix="/orders")

    return app
