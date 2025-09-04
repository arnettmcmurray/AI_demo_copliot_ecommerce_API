from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current = get_jwt_identity()
            if current["role"] != role:
                return jsonify({"error": "Forbidden"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def admin_required(fn):
    return role_required("admin")(fn)
