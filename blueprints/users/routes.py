from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from . import bp
from .schemas import user_schema
from app.extensions import db
from app.models import User


@bp.post("/register")
def register():
    data = request.get_json() or {}
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_pw = generate_password_hash(data["password"])
    user = User(
        email=data["email"],
        username=data.get("username"),
        password_hash=hashed_pw,
        address=data.get("address"),
        role="user",
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201


@bp.post("/login")
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not check_password_hash(user.password_hash, data.get("password", "")):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200


@bp.get("/me")
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user)), 200


@bp.put("/me")
@jwt_required()
def update_account():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}

    if "username" in data:
        user.username = data["username"]
    if "address" in data:
        user.address = data["address"]
    if "password" in data:
        user.password_hash = generate_password_hash(data["password"])

    db.session.commit()
    return jsonify({"message": "Account updated"}), 200


@bp.delete("/me")
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), 204
