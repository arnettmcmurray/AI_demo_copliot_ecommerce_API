from marshmallow import EXCLUDE
from app.extensions import ma
from app.models import User, Product, Cart, CartItem, Order, OrderItem


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)
        ordered = True
        unknown = EXCLUDE

    id = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = True
        ordered = True
        unknown = EXCLUDE

    id = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)


class CartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        load_instance = True
        include_relationships = True
        ordered = True
        unknown = EXCLUDE


class CartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartItem
        load_instance = True
        include_fk = True
        ordered = True
        unknown = EXCLUDE


class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem
        load_instance = True
        include_fk = True
        ordered = True
        unknown = EXCLUDE


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        include_fk = True
        ordered = True
        unknown = EXCLUDE

    items = ma.Nested(OrderItemSchema, many=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
cart_schema = CartSchema()
carts_schema = CartSchema(many=True)
cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
