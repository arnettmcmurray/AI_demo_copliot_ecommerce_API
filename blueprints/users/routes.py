from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models import User
from app.schemas import UserSchema

users_bp = Blueprint("users", __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_bp.route("", methods=["POST"])
def register_user():
    data = request.get_json()
    if not data.get("email") or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400
    hashed_pw = generate_password_hash(data["password"])
    user = User(email=data["email"], username=data["username"], password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()
    if user and check_password_hash(user.password, data.get("password")):
        token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify({"access_token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@users_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    current = get_jwt_identity()
    if current["id"] != id and current["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    user = User.query.get_or_404(id)
    return user_schema.jsonify(user)

@users_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    current = get_jwt_identity()
    if current["id"] != id and current["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    if "password" in data:
        user.password = generate_password_hash(data["password"])
    db.session.commit()
    return jsonify({"message": "User updated"}), 200

@users_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    current = get_jwt_identity()
    if current["id"] != id and current["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 204
