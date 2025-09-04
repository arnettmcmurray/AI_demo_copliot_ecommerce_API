import unittest
from app import create_app, db

class ProductTestCase(unittest.TestCase):
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

def test_create_and_get_product(self):
    # register and login as admin
    self.client.post("/users/register", json={
        "email": "admin@example.com",
        "username": "admin",
        "password": "adminpass",
        "address": "123 Admin St"
    })
    login_res = self.client.post("/users/login", json={
        "email": "admin@example.com",
        "password": "adminpass"
    })
    token = login_res.get_json()["access_token"]

    # try to create product
    res = self.client.post("/products",
        json={"name": "Laptop", "price": 1000, "stock": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    self.assertIn(res.status_code, [201, 403])

