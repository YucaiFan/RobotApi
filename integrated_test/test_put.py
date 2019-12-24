import sys
sys.path.append('..')
import unittest
from server import app
import json
import os

class TestPut(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass
        # self.server.stop()

    def test_modify(self):
        response = self.client.put("/api/robot/kawada-hironx", data={"name": "test_success"})
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        self.assertEqual(res_dict.get("response_code"), 0)

    def test_modify_duplicatename(self):
        response = self.client.put("/api/robot/kawada-hironx", data={"name": "kawada-hironx"})
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        self.assertEqual(res_dict.get("response_code"), 4)

    def test_modify_notexsist(self):
        response = self.client.put("/api/robot/not_exist", data={"name": "test"})
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        self.assertEqual(res_dict.get("response_code"), 3)

if __name__ == '__main__':
    unittest.main()
