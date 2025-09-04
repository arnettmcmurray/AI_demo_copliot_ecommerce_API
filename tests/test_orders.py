import unittest
from app import create_app, db

class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

def test_checkout_empty_cart(self):
    self.client.post("/users/register", json={
        "email": "order@example.com",
        "username": "orderuser",
        "password": "password",
        "address": "789 Order St"
    })
    login_res = self.client.post("/users/login", json={
        "email": "order@example.com",
        "password": "password"
    })
    token = login_res.get_json()["access_token"]

    res = self.client.post("/orders/checkout",
        json={"cart_id": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    self.assertIn(res.status_code, [400, 401])
