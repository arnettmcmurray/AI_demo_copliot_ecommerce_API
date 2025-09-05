from marshmallow import EXCLUDE
from app.extensions import ma
from app.models import Order, OrderItem


class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem
        load_instance = True
        include_fk = True
        ordered = True
        unknown = EXCLUDE


order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        include_fk = True
        ordered = True
        unknown = EXCLUDE

    items = ma.Nested(OrderItemSchema, many=True)


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
