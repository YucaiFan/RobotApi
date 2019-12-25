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
        #with open('/RobotApi/data/examples/barrett-hand.zae', 'rb') as f:
        #    response = self.client.post("/api/robot", data=dict(file=f))

    def tearDown(self):
        response = self.client.put("/api/robot/test", data='{"name": "cmu-permma"}', content_type="application/json")
        # self.server.stop()

    def test_modify(self):
        response = self.client.put("/api/robot/cmu-permma", data='{"name": "test"}', content_type="application/json")
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        self.assertEqual(res_dict.get("response_code"), 0)

    def test_modify_duplicatename(self):
        response = self.client.put("/api/robot/kawada-hironx", data='{"name": "kawada-hironx"}', content_type="application/json")
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        print(res_dict)
        self.assertEqual(res_dict.get("response_code"), 4)

    def test_modify_notexsist(self):
        response = self.client.put("/api/robot/not_exist", data='{"name": "test"}', content_type="application/json")
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        print(res_dict)
        self.assertEqual(res_dict.get("response_code"), 3)

if __name__ == '__main__':
    unittest.main()
