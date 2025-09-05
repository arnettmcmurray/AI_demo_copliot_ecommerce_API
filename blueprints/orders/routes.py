from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import bp
from .schemas import order_schema, orders_schema
from app.extensions import db
from app.models import Order, OrderItem, Cart, CartItem


@bp.post("")
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart or not cart.items:
        return jsonify({"status": 400, "message": "cart is empty"}), 400

    total_cents = sum(item.unit_price_cents * item.quantity for item in cart.items)
    order = Order(user_id=user_id, total_cents=total_cents, status="pending")
    db.session.add(order)
    db.session.flush()

    for item in cart.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price_cents=item.unit_price_cents,
        )
        db.session.add(order_item)

    db.session.query(CartItem).filter_by(cart_id=cart.id).delete()
    db.session.commit()
    return jsonify(order_schema.dump(order)), 201


@bp.get("")
@jwt_required()
def list_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify(orders_schema.dump(orders)), 200


@bp.get("/<int:order_id>")
@jwt_required()
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order_schema.dump(order)), 200
