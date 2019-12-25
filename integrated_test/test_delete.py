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
        with open("/RobotApi/data/examples/barrett-hand.zae") as f:
            response = self.client.post("/api/robot", data=dict(file=f))

    def tearDown(self):
        pass
        # self.server.stop()

    def test_delete_success(self):
        response = self.client.delete("/api/robot/barrett-hand")
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        self.assertEqual(res_dict.get("response_code"), 0)

    def test_delete_notfound(self):
        response = self.client.delete("/api/robot/not_exist")
        res_json = response.data
        res_dict = json.loads(res_json)
        self.assertIn("response_code", res_dict)
        self.assertEqual(res_dict.get("response_code"), 1)

if __name__ == '__main__':
    unittest.main()
