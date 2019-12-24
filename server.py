from flask import Flask, jsonify
from flask_pymongo import PyMongo
from utils.robot_parser import parse_robot

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://N0e1:N0e1970126@ds351455.mlab.com:51455/colladarobots"
mongo = PyMongo(app)

@app.route('/testparser', methods=['GET'])
def test_parser():
    output = []
    res = parse_robot("kawada-hironx.zae")
    #res = parse_robot("barrett-hand.zae")
    return jsonify({'result': res})

@app.route('/test', methods=['GET'])
def test_home():
    users = mongo.db.robots.find({"name": "harold"})
    output = []
    for s in users:
        output.append({'name': s['name'], 'age': s['dof']})
    return jsonify({'result': output})


# GET /api/robot 
# Usage: List all robots in the collection
@app.route('/api/robot')
def get_robots_list():
    # for i in range(len(list_of_robots)):
    pass


# GET /api/robot/filename
# Usage: List one of the robots in the collection
@app.route('/api/robot/<filename>')
def get_robot():
    pass


# PUT /api/robot/filename
# Usage: Modify property of one robot
@app.route('/api/robot/<filename>')
def put_modify_property():
    pass




# POST /api/robot 
# Usage: Upload a robot file to the collection (updating database)
@app.route('/api/robot')
def post_upload_robot():
    pass

# GET /api/robot/filename/download
# Usage: Download one robot file
@app.route('/api/robot')
def get_download_robot():
    pass

# DELETE /api/robot/filename
# Usage: Remove a robot file
@app.route('/api/robot/<filename>')
def delete_remove_robot():
    pass


if __name__ == '__main__':
    app.run()
