import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class AuthTests(unittest.TestCase):

    def test_register_user(self):
        response = client.post("/auth/register", json={
            "email": "testuser@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        # Ensure the user is registered before login
        client.post("/auth/register", json={
            "email": "testlogin@example.com",
            "password": "password123"
        })
        response = client.post("/auth/login", json={
            "email": "testlogin@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())


if __name__ == "__main__":
    unittest.main()
