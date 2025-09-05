from app import create_app
from app.extensions import db
from app.models import User, Product, Cart, CartItem, Order, OrderItem
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Users
    admin = User(
        email="admin@example.com",
        username="admin",
        password_hash=generate_password_hash("Admin123!"),
        address="HQ",
        role="admin",
    )
    customer = User(
        email="customer@example.com",
        username="customer",
        password_hash=generate_password_hash("Password123!"),
        address="123 Main St",
    )
    db.session.add_all([admin, customer])
    db.session.commit()

    # Products
    mouse = Product(
        name="Logitech MX Master 3S",
        description="Performance wireless mouse",
        brand="Logitech",
        sku="LOGI-MX3S-GRAPH",
        upc="097855175746",
        ean="5099206099153",
        price_cents=9999,
        currency="USD",
        stock=50,
        image_url="https://example.com/mx3s.jpg",
        attributes={"color": "graphite", "dpi": 8000},
    )
    db.session.add(mouse)
    db.session.commit()

    # Cart + Item
    cart = Cart(user_id=customer.id)
    db.session.add(cart)
    db.session.commit()

    item = CartItem(cart_id=cart.id, product_id=mouse.id, quantity=1, unit_price_cents=mouse.price_cents)
    db.session.add(item)
    db.session.commit()

    # Order + OrderItem
    order = Order(user_id=customer.id, status="completed", total_cents=mouse.price_cents)
    db.session.add(order)
    db.session.flush()

    order_item = OrderItem(order_id=order.id, product_id=mouse.id, quantity=1, unit_price_cents=mouse.price_cents)
    db.session.add(order_item)
    db.session.commit()

    print("✅ Database seeded with sample admin, customer, product, cart, and order.")
