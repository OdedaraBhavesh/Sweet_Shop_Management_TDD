from backend.app.main import app
import unittest
import uuid
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


# from ..app.main import app  # Adjust the import based on your project structure
client = TestClient(app)


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.email = f"user_{uuid.uuid4().hex[:8]}@test.com"
        self.password = "TestPass123"

    def test_register_success(self):
        response = client.post("/register", json={
            "email": self.email,
            "password": self.password
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertEqual(
            response.json()["message"], "User registered successfully")

    def test_register_existing_email(self):
        # First register
        client.post("/register", json={
            "email": self.email,
            "password": self.password
        })

        # Try to register again
        response = client.post("/register", json={
            "email": self.email,
            "password": self.password
        })

        self.assertIn(response.status_code, [400, 409])
        self.assertIn("message", response.json())

    def test_login_success(self):
        # First register
        client.post("/register", json={
            "email": self.email,
            "password": self.password
        })

        # Then login
        response = client.post("/login", json={
            "email": self.email,
            "password": self.password
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Login successful")
        self.assertIn("session", response.cookies)

    def test_login_invalid_password(self):
        # Register first
        client.post("/register", json={
            "email": self.email,
            "password": self.password
        })

        # Try wrong password
        response = client.post("/login", json={
            "email": self.email,
            "password": "WrongPass"
        })

        self.assertEqual(response.status_code, 401)
        self.assertIn("message", response.json())

    def test_login_unregistered_email(self):
        response = client.post("/login", json={
            "email": "nonexistent@test.com",
            "password": "AnyPass123"
        })

        self.assertEqual(response.status_code, 401)
        self.assertIn("message", response.json())
