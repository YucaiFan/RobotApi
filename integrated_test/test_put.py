import sys
sys.path.append('..')
import unittest
from server import app
import json
import os
from flask import jsonify

class TestPut(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        with open('/RobotApi/data/examples/barrett-hand.zae', 'rb') as f:
            response = self.client.post("/api/robot", data=dict(file=f))

    def tearDown(self):
        response = self.client.delete("/api/robot/test_success")
        # self.server.stop()

    def test_modify(self):
        response = self.client.put("/api/robot/barrett-hand", data={"name": "test_success"})
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        print(res_dict)
        self.assertEqual(res_dict.get("response_code"), 0)

    def test_modify_duplicatename(self):
        response = self.client.put("/api/robot/kawada-hironx", data={"name": "kawada-hironx"})
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        print(res_dict)
        self.assertEqual(res_dict.get("response_code"), 4)

    def test_modify_notexsist(self):
        response = self.client.put("/api/robot/not_exist", data={"name": "test"})
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        print(res_dict)
        self.assertEqual(res_dict.get("response_code"), 3)

if __name__ == '__main__':
    unittest.main()
