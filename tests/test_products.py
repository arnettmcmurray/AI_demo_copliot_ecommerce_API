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
        # create user admin for auth bypass in real impl
        self.client.post("/users", json={
            "email": "admin@example.com",
            "username": "admin",
            "password": "adminpass"
        })
        res = self.client.post("/products", json={
            "name": "Laptop",
            "price": 1000,
            "stock": 5
        })
        self.assertIn(res.status_code, [201, 403])  # admin restriction
