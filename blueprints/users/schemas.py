from marshmallow import EXCLUDE
from app.extensions import ma
from app.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        ordered = True
        unknown = EXCLUDE

    id = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
