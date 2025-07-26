from .base_test import BaseMongoTestCase


class TestAuthEndpoints(BaseMongoTestCase):
    async def test_login_valid(self):
        response = await self.client.post("/auth/token", data={
            "username": "test@example.com",
            "password": "test123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    async def test_login_invalid(self):
        response = await self.client.post("/auth/token", data={
            "username": "wrong@example.com",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 401)
