import unittest
from app import create_app, db

class UserTestCase(unittest.TestCase):
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

    def test_register_and_login_user(self):
        res = self.client.post("/users", json={
            "email": "test@example.com",
            "username": "tester",
            "password": "password"
        })
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/users/login", json={
            "email": "test@example.com",
            "password": "password"
        })
        self.assertEqual(res.status_code, 200)
