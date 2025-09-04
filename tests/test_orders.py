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
        self.client.post("/users", json={
            "email": "order@example.com",
            "username": "orderuser",
            "password": "password"
        })
        res = self.client.post("/orders/checkout", json={"cart_id": 1})
        self.assertIn(res.status_code, [400, 401])
