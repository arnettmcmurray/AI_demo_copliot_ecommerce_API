from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_

from . import bp
from .schemas import cart_item_schema, cart_items_schema
from app.extensions import db
from app.models import Cart, CartItem, Product


def get_or_create_cart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    return cart


@bp.get("")
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart = get_or_create_cart(user_id)
    return jsonify(cart_items_schema.dump(cart.items)), 200


@bp.post("/items")
@jwt_required()
def add_item():
    user_id = get_jwt_identity()
    cart = get_or_create_cart(user_id)
    data = request.get_json() or {}
    qty = int(data.get("quantity", 1))
    if qty <= 0:
        return jsonify({"status": 400, "message": "quantity must be > 0"}), 400

    product = None
    if "product_id" in data:
        product = Product.query.get(data["product_id"])
    elif "code" in data:
        code = data["code"]
        product = Product.query.filter(
            or_(
                Product.sku == code,
                Product.serial_number == code,
                Product.upc == code,
                Product.ean == code,
            )
        ).first()

    if not product:
        return jsonify({"status": 404, "message": "product not found"}), 404
    if product.stock < qty:
        return jsonify({"status": 409, "message": "insufficient stock"}), 409

    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
    if item:
        item.quantity += qty
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=qty,
            unit_price_cents=product.price_cents,
        )
        db.session.add(item)

    db.session.commit()
    return jsonify(cart_item_schema.dump(item)), 201


@bp.delete("/items/<int:item_id>")
@jwt_required()
def remove_item(item_id):
    user_id = get_jwt_identity()
    cart = get_or_create_cart(user_id)
    item = CartItem.query.filter_by(cart_id=cart.id, id=item_id).first()
    if not item:
        return jsonify({"status": 404, "message": "item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"status": 200, "message": "removed"}), 200
