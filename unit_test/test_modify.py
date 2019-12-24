import unittest
from server import app
import json

class TestGet(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_list_success(self):
        response = self.client.get("/api/robot")
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        self.assertEqual(res_dict.get("response_code"), 0)

    def test_single_success(self):
        response = self.client.get("/api/robot/kawada-hironx")
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        self.assertEqual(res_dict.get("response_code"), 0)

if __name__ == '__main__':
    unittest.main()
