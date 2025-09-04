from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db
from app.models import User
from app.config import Config

auth_bp = Blueprint("auth", __name__)

# ---------- Register ----------
@auth_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "username", "password", "address")):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(
        email=data["email"],
        username=data["username"],
        password=generate_password_hash(data["password"]),
        address=data["address"],
        role="customer"
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# ---------- Login ----------
@auth_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()

    if not user or not check_password_hash(user.password, data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=Config.JWT_ACCESS_TOKEN_EXPIRES
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        expires_delta=Config.JWT_REFRESH_TOKEN_EXPIRES
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200


# ---------- Refresh ----------
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_user():
    current_user = get_jwt_identity()
    new_access = create_access_token(
        identity=current_user,
        expires_delta=Config.JWT_ACCESS_TOKEN_EXPIRES
    )
    return jsonify({"access_token": new_access}), 200


# ---------- Protected ----------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    current_user = int(get_jwt_identity())
    user = User.query.get_or_404(current_user)
    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "address": user.address,
        "role": user.role
    }), 200
