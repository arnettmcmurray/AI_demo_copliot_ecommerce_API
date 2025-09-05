from datetime import datetime
from .extensions import db

# === User ===
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime, default=datetime.now)


# === Product ===
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price_cents = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="USD")
    stock = db.Column(db.Integer, nullable=False, default=0)
    brand = db.Column(db.String(120), nullable=True, index=True)
    sku = db.Column(db.String(64), unique=True, index=True)
    serial_number = db.Column(db.String(128), unique=True, index=True)
    upc = db.Column(db.String(32), index=True)
    ean = db.Column(db.String(32), index=True)
    image_url = db.Column(db.String(400), nullable=True)
    attributes = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order_items = db.relationship("OrderItem", backref="product", lazy=True)
    cart_items = db.relationship("CartItem", backref="product", lazy=True)


# === Cart & CartItem ===
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    items = db.relationship("CartItem", backref="cart", lazy=True)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price_cents = db.Column(db.Integer, nullable=False)


# === Order & OrderItem ===
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(20), default="pending")
    total_cents = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("OrderItem", backref="order", lazy=True)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price_cents = db.Column(db.Integer, nullable=False)
