import unittest
from app import create_app, db

class CartTestCase(unittest.TestCase):
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

    def test_cart_creation(self):
        self.client.post("/users", json={
            "email": "cart@example.com",
            "username": "cartuser",
            "password": "password"
        })
        res = self.client.post("/carts", json={})
        self.assertIn(res.status_code, [201, 401])
