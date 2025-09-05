from marshmallow import EXCLUDE
from app.extensions import ma
from app.models import Product


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


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
