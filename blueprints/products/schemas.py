from app.extensions import ma
from app.models import CartItem

class CartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartItem
        load_instance = True

cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)
