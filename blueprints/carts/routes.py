from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Cart, CartItem, Product
from app.schemas import CartSchema, CartItemSchema

carts_bp = Blueprint("carts", __name__)

# Schemas
cart_schema = CartSchema()
carts_schema = CartSchema(many=True)
cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)

# Create a cart for the current user
@carts_bp.route("", methods=["POST"])
@jwt_required()
def create_cart():
    current_user_id = int(get_jwt_identity())   # this is your user_id
    cart = Cart(user_id=current_user_id)
    db.session.add(cart)
    db.session.commit()
    return jsonify({"id": cart.id, "user_id": cart.user_id}), 201


# Add item to a cart
@carts_bp.route("/<int:cart_id>/items", methods=["POST"])
@jwt_required()
def add_item(cart_id):
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        return jsonify({"error": "Not enough stock"}), 400

    item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
    db.session.add(item)
    db.session.commit()

    return cart_item_schema.jsonify(item), 201


# View all carts (admin/debug)
@carts_bp.route("", methods=["GET"])
@jwt_required()
def get_carts():
    carts = Cart.query.all()
    return carts_schema.jsonify(carts), 200

# View a single cart’s items
@carts_bp.route("/<int:cart_id>", methods=["GET"])
@jwt_required()
def view_cart(cart_id):
    items = CartItem.query.filter_by(cart_id=cart_id).all()
    return cart_items_schema.jsonify(items), 200

# Remove item from cart
@carts_bp.route("/<int:cart_id>/items/<int:item_id>", methods=["DELETE"])
@jwt_required()
def remove_item(cart_id, item_id):
    item = CartItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item removed"}), 200
