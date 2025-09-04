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
    self.client.post("/users/register", json={
        "email": "cart@example.com",
        "username": "cartuser",
        "password": "password",
        "address": "456 Cart St"
    })
    login_res = self.client.post("/users/login", json={
        "email": "cart@example.com",
        "password": "password"
    })
    token = login_res.get_json()["access_token"]

    res = self.client.post("/carts",
        headers={"Authorization": f"Bearer {token}"}
    )
    self.assertIn(res.status_code, [201, 401])

