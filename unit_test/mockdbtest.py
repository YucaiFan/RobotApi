import sys
sys.path.append('..')
import unittest
from server import app
import json
import os
from mockupdb import MockupDB, go, Command
from pymongo import MongoClient

DOCUMENT = {"response_code":0,"result":[{"manipulators":[{"arm":[1,2,3,4,5,6],"armdof":"6","base":"l-lift-arm","end":"left-hand-base","gripper":[7],"gripperdof":"1","manipulator_name":"leftarm"}],"name":"not_a_robot"},{"manipulators":[{"arm":[3,4,5,6,7,8],"armdof":"6","base":"CHEST_JOINT0_Link","end":"RARM_JOINT5_Link","gripper":[9,10,11,12],"gripperdof":"4","manipulator_name":"rightarm"},{"arm":[0,3,4,5,6,7,8],"armdof":"7","base":"WAIST","end":"RARM_JOINT5_Link","gripper":[9,10,11,12],"gripperdof":"4","manipulator_name":"rightarm_torso"},{"arm":[13,14,15,16,17,18],"armdof":"6","base":"CHEST_JOINT0_Link","end":"LARM_JOINT5_Link","gripper":[19,20,21,22],"gripperdof":"4","manipulator_name":"leftarm"},{"arm":[0,13,14,15,16,17,18],"armdof":"7","base":"WAIST","end":"LARM_JOINT5_Link","gripper":[19,20,21,22],"gripperdof":"4","manipulator_name":"leftarm_torso"},{"arm":[1,2],"armdof":"2","base":"CHEST_JOINT0_Link","end":"HEAD_JOINT1_Link","gripper":[],"gripperdof":"0","manipulator_name":"head"},{"arm":[0,1,2],"armdof":"3","base":"WAIST","end":"HEAD_JOINT1_Link","gripper":[],"gripperdof":"0","manipulator_name":"head_torso"}],"name":"kawada-hironx"}]}

class TestGet(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.server = MockupDB(auto_ismaster=True, verbose=True)
        self.server.run()
        app.testing = True
        app.config['MONGO_URI'] = self.server.uri
        self.client = app.test_client()

    @classmethod
    def tearDown(self):
        self.server.stop()
        # os.close(self.db_fd)
        # os.unlink(app.config['MONGO_URI'])

    @classmethod
    def test_getlist(self):
        document = DOCUMENT
        future = go(self.client.get, '/api/robot')
        request = self.server.receives()
        request.reply(document)

        http_response = future()
        data = http_response.get_data(as_text=True)
        self.assertIn('not_a_robot', data)
        self.assertIn('kawada-hironx', data)

    #def test_single_success(self):
    #    response = self.client.get("/api/robot/kawada-hironx")
    #    res_json = response.data
    #    res_dict = json.loads(res_json)
    #    self.assertIn("response_code", res_dict)
    #    self.assertEqual(res_dict.get("response_code"), 0)

if __name__ == '__main__':
    unittest.main()
