from flask import Flask, jsonify
from flask import request, abort
from flask_pymongo import PyMongo
from utils.robot_parser import parse_robot

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://N0e1:N0e1970126@ds351455.mlab.com:51455/colladarobots"
app.config["UPLOAD_FOLDER"] = "/data/uploads"
mongo = PyMongo(app, retryWrites=False)

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
@app.route('/api/robot', methods=['GET'])
def get_robots_list():
    # for i in range(len(list_of_robots)):
    robots_list = mongo.db.robots.find()
    output = []
    for robot in robots_list:
        output.append({'name': robot['name'], 'manipulators': robot['manipulators']})
    return jsonify({'response_code': 0, 'result': output})

# GET /api/robot/filename
# Usage: List one of the robots in the collection
@app.route('/api/robot/<filename>', methods=['GET'])
def get_robot(filename):
    robot = mongo.db.robots.find_one({'name': filename})
    if robot:
        output = {'name': robot['name'], 'manipulators': robot['manipulators']}
        return jsonify({'response_code': 0, 'result': output})
    else:
        output = "File not found"
        return jsonify({'response_code': 1, 'result': output})


# PUT /api/robot/filename
# Usage: Modify property of one robot
@app.route('/api/robot/<filename>')
def put_modify_property(filename):




# TODO: file transfer. Currently using file path.
# POST /api/robot 
# Usage: Upload a robot file to the collection (updating database)
@app.route('/api/testupload', methods=['POST'])
    filename = secure_filename(filename)

@app.route('/api/robot', methods=['POST'])
def post_upload_robot():
    if not request.json or not 'filename' in request.json:
        abort(400)
    print(">> req:")
    print(request.json)
    filename = request.json['filename']
    
    print(">> Uploading:", filename)
    target_data = parse_robot(filename) 

    exist_robot = mongo.db.robots.find_one({'name': target_data['name']})
    if exist_robot:
        return jsonify({'response_code': 1, 'result': {'name': exist_robot['name'], 'manipulators': exist_robot['manipulators']}})
        abort(400)

    new_id = mongo.db.robots.insert(target_data)
    print(">> Uploaded:", str(new_id))
    # new_robot = mongo.db.robots.find_one({'_id': {'\$oid': str(new_id)}})
    new_robot = mongo.db.robots.find_one({'name': target_data['name']})
    print(new_robot)
    return jsonify({'response_code': 0, 'result': {'name': new_robot['name'], 'manipulators': new_robot['manipulators']}})


# GET /api/robot/filename/download
# Usage: Download one robot file
@app.route('/api/robot/<filename>/download')
def get_download_robot(filename):
    robot = mongo.db.robots.find_one({'name': filename})
    if robot:
        res = mongo.db.robots.delete()
    if not res:
        return jsonify({'response_code': 1, 'msg': 'Deleting failed'})


# DELETE /api/robot/filename
# Usage: Remove a robot file
@app.route('/api/robot/<filename>', methods=['DELETE'])
def delete_remove_robot(filename):
    robot = mongo.db.robots.find_one({'name': filename})
    if robot:
        res = mongo.db.robots.delete()
    if not res:
        return jsonify({'response_code': 1, 'msg': 'Deleting failed'})

    robot_file = mongo.db.filecontents.find_one({'name': filename})
    if robot_file:
        res = mongo.db.filecontents.delete()
    if not res:
        return jsonify({'response_code': 1, 'msg': 'Deleting failed'})
    return jsonify({'response_code': 0, 'msg': 'Deleting success'})



if __name__ == '__main__':
    app.run()
