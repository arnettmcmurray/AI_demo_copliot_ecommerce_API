from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import User
from app.schemas import UserSchema

users_bp = Blueprint("users", __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    if not data.get("email") or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing required fields"}), 400
    
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400
    
    hashed_password = generate_password_hash(data["password"])
    new_user = User(
        email=data["email"],
        username=data["username"],
        password=hashed_password,
        address=data.get("address"),
        role="user"
    )
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

@users_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()

    if not user or not check_password_hash(user.password, data.get("password", "")):
        return jsonify({"error": "Invalid credentials"}), 401

    # Always stringify identity
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200

@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_account():
    current_user_id = int(get_jwt_identity())
    user = User.query.get_or_404(current_user_id)
    return user_schema.jsonify(user), 200

@users_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_account():
    current_user_id = int(get_jwt_identity())
    user = User.query.get_or_404(current_user_id)
    data = request.get_json()
    if "username" in data: user.username = data["username"]
    if "address" in data: user.address = data["address"]
    if "password" in data: user.password = generate_password_hash(data["password"])
    db.session.commit()
    return jsonify({"message": "Account updated"}), 200

@users_bp.route("/me", methods=["DELETE"])
@jwt_required()
def delete_account():
    current_user_id = int(get_jwt_identity())
    user = User.query.get_or_404(current_user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), 204
