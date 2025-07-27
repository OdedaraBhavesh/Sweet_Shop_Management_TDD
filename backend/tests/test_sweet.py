import unittest
import json
from backend.app.main import app


class TestSweetAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.sample_sweet = {
            "name": "Rasgulla",
            "category": "Bengali",
            "price": 15,
            "quantity": 20
        }
        cls.sweet_id = None

    def test_add_sweet(self):
        response = self.client.post('/api/sweets', json=self.sample_sweet)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('name', data)
        self.__class__.sweet_id = data.get('_id')

    def test_list_sweets(self):
        response = self.client.get('/api/sweets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_update_sweet(self):
        self.assertIsNotNone(self.__class__.sweet_id)
        updated_sweet = {
            "name": "Gulab Jamun",
            "category": "North Indian",
            "price": 20,
            "quantity": 30
        }
        response = self.client.put(
            f'/api/sweets/{self.__class__.sweet_id}', json=updated_sweet)
        self.assertEqual(response.status_code, 200)
        updated_data = json.loads(response.data)
        self.assertEqual(updated_data['name'], "Gulab Jamun")

    def test_delete_sweet(self):
        self.assertIsNotNone(self.__class__.sweet_id)
        response = self.client.delete(f'/api/sweets/{self.__class__.sweet_id}')
        self.assertIn(response.status_code, [200, 204])


if __name__ == '__main__':
    unittest.main()
