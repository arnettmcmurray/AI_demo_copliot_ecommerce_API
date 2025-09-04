from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Product
from app.schemas import ProductSchema

products_bp = Blueprint("products", __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@products_bp.route("", methods=["POST"])
@jwt_required()
def create_product():
    current = get_jwt_identity()
    if current["role"] != "admin":
        return jsonify({"error": "Admins only"}), 403
    data = request.get_json()
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return product_schema.jsonify(product), 201

@products_bp.route("", methods=["GET"])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products)

@products_bp.route("/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)

@products_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_product(id):
    current = get_jwt_identity()
    if current["role"] != "admin":
        return jsonify({"error": "Admins only"}), 403
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)
    db.session.commit()
    return jsonify({"message": "Product updated"}), 200

@products_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product(id):
    current = get_jwt_identity()
    if current["role"] != "admin":
        return jsonify({"error": "Admins only"}), 403
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 204
