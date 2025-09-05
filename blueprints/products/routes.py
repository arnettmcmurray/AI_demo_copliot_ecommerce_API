from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_

from . import bp
from .schemas import product_schema, products_schema
from app.extensions import db
from app.models import Product, User


@bp.post("")
@jwt_required()
def create_product():
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    if current_user.role != "admin":
        return jsonify({"error": "Admins only"}), 403

    data = request.get_json() or {}
    product = product_schema.load(data, session=db.session)
    db.session.add(product)
    db.session.commit()
    return jsonify(product_schema.dump(product)), 201


@bp.get("")
def list_products():
    q = request.args.get("q")
    brand = request.args.get("brand")
    code = request.args.get("code")
    page = max(int(request.args.get("page", 1)), 1)
    per_page = min(int(request.args.get("per_page", 20)), 100)

    query = Product.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Product.name.ilike(like), Product.description.ilike(like)))
    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))
    if code:
        query = query.filter(or_(
            Product.sku == code,
            Product.serial_number == code,
            Product.upc == code,
            Product.ean == code
        ))

    page_obj = query.order_by(Product.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "status": 200,
        "message": "ok",
        "data": products_schema.dump(page_obj.items),
        "meta": {"page": page, "per_page": per_page, "total": page_obj.total}
    }), 200


@bp.get("/<int:product_id>")
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product_schema.dump(product)), 200


@bp.put("/<int:product_id>")
@jwt_required()
def update_product(product_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    if current_user.role != "admin":
        return jsonify({"error": "Admins only"}), 403

    product = Product.query.get_or_404(product_id)
    data = request.get_json() or {}
    for field, value in data.items():
        if hasattr(product, field):
            setattr(product, field, value)
    db.session.commit()
    return jsonify(product_schema.dump(product)), 200


@bp.delete("/<int:product_id>")
@jwt_required()
def delete_product(product_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    if current_user.role != "admin":
        return jsonify({"error": "Admins only"}), 403

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"status": 200, "message": "deleted"}), 200


@bp.post("/scan")
def scan_lookup():
    payload = request.get_json(silent=True) or {}
    code = payload.get("serial_number") or payload.get("upc") or payload.get("ean") or payload.get("code") or payload.get("sku")
    if not code:
        return jsonify({"status": 400, "message": "code required", "errors": {"code": "missing"}}), 400

    product = Product.query.filter(
        or_(Product.serial_number == code, Product.upc == code, Product.ean == code, Product.sku == code)
    ).first()

    if not product:
        return jsonify({"status": 404, "message": "product not found"}), 404

    return jsonify(product_schema.dump(product)), 200
