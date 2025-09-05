from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from werkzeug.security import generate_password_hash, check_password_hash

from . import bp
from .schemas import RegisterSchema, LoginSchema
from app.extensions import db
from app.models import User
from blueprints.users.schemas import user_schema

register_schema = RegisterSchema()
login_schema = LoginSchema()

@bp.post("/register")
def register():
    payload = register_schema.load(request.get_json() or {})
    if User.query.filter_by(email=payload["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(
        email=payload["email"],
        username=payload["username"],
        password_hash=generate_password_hash(payload["password"]),
        address=payload.get("address"),
        role="user",
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201

@bp.post("/login")
def login():
    creds = login_schema.load(request.get_json() or {})
    user = User.query.filter_by(email=creds["email"]).first()
    if not user or not check_password_hash(user.password_hash, creds["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    uid = get_jwt_identity()
    new_access = create_access_token(identity=uid)
    return jsonify({"access_token": new_access}), 200
