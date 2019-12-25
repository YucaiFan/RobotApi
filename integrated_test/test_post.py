import sys
sys.path.append('..')
import unittest
from server import app
import json
import os
from mockupdb import MockupDB, go, Command
from pymongo import MongoClient

class TestGet(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        response = self.client.delete('/api/robot/barret-hand')
        # self.server.stop()

    def test_upload_success(self):
        with open('/RobotApi/data/examples/barrett-hand.zae', 'rb') as f:
            response = self.client.post("/api/robot", data=dict(file=f))
            res_json = response.data
            res_dict = json.loads(res_json)
            self.assertIn("response_code", res_dict)
            self.assertEqual(res_dict.get("response_code"), 0)

    def test_upload_format(self):
        with open('/RobotApi/data/examples/cmu-permma.zzz', 'rb') as f:
            response = self.client.post("/api/robot", data=dict(file=f))
            res_json = response.data
            res_dict = json.loads(res_json)
            self.assertIn("response_code", res_dict)
            self.assertEqual(res_dict.get("response_code"), 3)

    def test_upload_dupname(self):
        with open('/RobotApi/data/examples/kawada-hironx.zae', 'rb') as f:
            response = self.client.post("/api/robot", data=dict(file=f))
            res_json = response.data
            res_dict = json.loads(res_json)
            self.assertIn("response_code", res_dict)
            self.assertEqual(res_dict.get("response_code"), 1)

if __name__ == '__main__':
    unittest.main()
