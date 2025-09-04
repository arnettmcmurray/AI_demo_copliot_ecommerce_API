from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Order, OrderItem, CartItem, Cart, Product
from app.schemas import OrderSchema
from app.models import User

orders_bp = Blueprint("orders", __name__)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@orders_bp.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get_or_404(current_user_id)
    data = request.get_json()
    cart = Cart.query.get_or_404(data["cart_id"])

    if cart.user_id != current_user.id and current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    items = CartItem.query.filter_by(cart_id=cart.id).all()
    if not items:
        return jsonify({"error": "Cart is empty"}), 400

    order = Order(user_id=cart.user_id, status="pending", total_price=0.0)
    db.session.add(order)
    db.session.flush()

    total_price = 0
    for item in items:
        product = Product.query.get(item.product_id)
        if not product or product.stock < item.quantity:
            return jsonify({"error": f"Not enough stock for {product.name}"}), 400
        product.stock -= item.quantity
        order_item = OrderItem(order_id=order.id, product_id=product.id,
                               quantity=item.quantity, price=product.price)
        db.session.add(order_item)
        total_price += product.price * item.quantity
        db.session.delete(item)

    order.total_price = total_price
    db.session.commit()
    return order_schema.jsonify(order), 201

@orders_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_order(id):
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get_or_404(current_user_id)
    order = Order.query.get_or_404(id)

    if order.user_id != current_user.id and current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    return order_schema.jsonify(order), 200
