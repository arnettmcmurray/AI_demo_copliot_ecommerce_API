from marshmallow import EXCLUDE
from app.extensions import ma
from app.models import CartItem, Cart


class CartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartItem
        load_instance = True
        include_fk = True
        ordered = True
        unknown = EXCLUDE

    id = ma.auto_field(dump_only=True)


class CartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        load_instance = True
        include_relationships = True
        ordered = True
        unknown = EXCLUDE

    id = ma.auto_field(dump_only=True)


cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)
cart_schema = CartSchema()
carts_schema = CartSchema(many=True)
