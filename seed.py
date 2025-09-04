# seed.py

from app import create_app
from app.extensions import db
from app.models import User, Product, Cart, Order, CartItem, OrderItem
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Users
    user1 = User(email="customer1@example.com", username="customer1", password=generate_password_hash("pass123"), address="123 Main St")
    user2 = User(email="customer2@example.com", username="customer2", password=generate_password_hash("pass456"), address="456 Oak St")

    db.session.add_all([user1, user2])
    db.session.commit()

    # Products
    product1 = Product(name="Laptop", description="High performance laptop", price=1200.00, stock=10, brand="TechBrand")
    product2 = Product(name="Headphones", description="Noise cancelling", price=200.00, stock=25, brand="SoundBrand")
    product3 = Product(name="Keyboard", description="Mechanical keyboard", price=80.00, stock=40, brand="KeyCo")

    db.session.add_all([product1, product2, product3])
    db.session.commit()

    # Carts
    cart1 = Cart(user_id=user1.id)
    cart2 = Cart(user_id=user2.id)

    db.session.add_all([cart1, cart2])
    db.session.commit()

    # CartItems
    cart_item1 = CartItem(cart_id=cart1.id, product_id=product1.id, quantity=1)
    cart_item2 = CartItem(cart_id=cart1.id, product_id=product2.id, quantity=2)

    db.session.add_all([cart_item1, cart_item2])
    db.session.commit()

    # Orders
    order1 = Order(user_id=user1.id, status="completed", total_price=1600.00)
    order2 = Order(user_id=user2.id, status="pending", total_price=80.00)

    db.session.add_all([order1, order2])
    db.session.commit()

    # OrderItems
    order_item1 = OrderItem(order_id=order1.id, product_id=product1.id, quantity=1, price=1200.00)
    order_item2 = OrderItem(order_id=order1.id, product_id=product2.id, quantity=2, price=200.00)
    order_item3 = OrderItem(order_id=order2.id, product_id=product3.id, quantity=1, price=80.00)

    db.session.add_all([order_item1, order_item2, order_item3])
    db.session.commit()

    print("✅ Database seeded with users, products, carts, orders, cart items, and order items.")
