import os
import json
from bson import ObjectId
from flask import Flask, jsonify
from flask import request, abort, url_for, send_from_directory
from flask_pymongo import PyMongo
from werkzeug import secure_filename
from utils.robot_parser import parse_robot

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://N0e1:N0e1970126@ds351455.mlab.com:51455/colladarobots"
app.config["UPLOAD_FOLDER"] = "/RobotApi/data/uploads"
mongo = PyMongo(app, retryWrites=False)

@app.route('/testupload', methods=['POST'])
def upload_file():
    f = request.files['file']
    if f and f.filename.split('.')[-1] == 'zae':
        # todo: check file header
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = url_for('uploaded_file', filename=filename)
    print(">> url")
    print(file_url)
    if file_url:
        return jsonify({"response_code": 0, "msg": "success", "url": str(file_url)})
    else:
        return jsonify({"response_code": 1, "msg": "failed"})

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
@app.route('/api/robot/<robotname>', methods=['GET'])
def get_robot(robotname):
    robot = mongo.db.robots.find_one({'name': robotname})
    if robot:
        output = {'name': robot['name'], 'manipulators': robot['manipulators']}
        return jsonify({'response_code': 0, 'msg': 'Found', 'result': output})
    else:
        output = "File not found"
        return jsonify({'response_code': 1, 'msg': output})

# PUT /api/robot/filename
# Usage: Modify property of one robot
@app.route('/api/robot/<robotname>', methods=['PUT'])
def put_modify_property(robotname):
    try:
        update_filter = {'name': robotname}
        json_data = json.loads(request.get_data())
        info = json_data

        if mongo.db.robots.find_one({'name': robotname}) is None:
            return jsonify({'response_code': 3, 'msg': 'robot not found'})
        
        if mongo.db.robots.find_one({'name': info['name']}):
            return jsonify({'response_code': 4, 'msg': 'duplicate name'})

        # todo: make consistent
        res = mongo.db.robots.update(update_filter, {'$set': info}) 
        print(res)
        if res['ok']:
            if info.has_key('name'):
                filename = robotname + ".zae"
                targetname = info['name'] + ".zae"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                targetpath = os.path.join(app.config['UPLOAD_FOLDER'], targetname)
                if os.path.exists(filepath):
                    os.rename(filepath, targetpath) 
                    return jsonify({'response_code': 0, 'msg': 'success'})
                else:
                    return jsonify({'response_code': 2, 'msg': 'file not found'})
        return jsonify({'response_code': 1, 'msg': 'failed'})
    except Exception as e:
        return jsonify({'response_code': -1, 'msg': str(e)})

# POST /api/robot 
# Usage: Upload a robot file to the collection (updating database)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/robot', methods=['POST'])
def post_upload_robot():
    try:
        f = request.files['file']
        if f and f.filename.split('.')[-1] == 'zae':
            # todo: check file header
            filename = secure_filename(f.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(filepath)
            file_url = url_for('uploaded_file', filename=filename)
            print(">> Uploaded:", filename)
            print(">> Url: ")
            print(file_url)

            print(">> path:", str(filepath))
            target_data = parse_robot(filepath) 
            exist_robot = mongo.db.robots.find_one({'name': target_data['name']})
            if exist_robot:
                return jsonify({'response_code': 1, 'msg': 'duplicate name', 'result': {'name': exist_robot['name'], 'manipulators': exist_robot['manipulators']}})
            new_id = mongo.db.robots.insert(target_data)
            print(">> Uploaded:", str(new_id))
            # new_robot = mongo.db.robots.find_one({'_id': {'\$oid': str(new_id)}})
            new_robot = mongo.db.robots.find_one({'_id': ObjectId(str(new_id))})
            if new_robot: 
                return jsonify({'response_code': 0, 'msg':'success', 'url': file_url, 'result': {'name': new_robot['name'], 'manipulators': new_robot['manipulators']}})
            else:
                return jsonify({'response_code': 2, 'msg': 'insert failed'})
        return jsonify({'response_code': 3, 'msg': 'file format'})
    except Exception as e:
        return jsonify({'response_code': -1, 'msg': str(e)})

# GET /api/robot/filename/download
# Usage: Download one robot file
@app.route('/api/robot/<robotname>/download', methods=['GET'])
def get_download_robot(robotname):
    filename = robotname + ".zae"
    print(">> name: ", robotname)
    robot = mongo.db.robots.find_one({'name': robotname})
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(">> filepath: ", str(filepath))
    if robot and os.path.exists(filepath):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    return jsonify({'response_code': 1, 'msg': 'Downloading failed'})

# DELETE /api/robot/filename
# Usage: Remove a robot file
@app.route('/api/robot/<robotname>', methods=['DELETE'])
def delete_remove_robot(robotname):
    filename = robotname + ".zae"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    res = mongo.db.robots.find_one({'name': robotname})
    if res:
        mongo.db.robots.delete_one({'name': robotname})
        if filename.split('.')[-1] == 'zae' and os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'response_code': 0, 'msg': 'success', 'filename': filename})
    return jsonify({'response_code': 1, 'msg': 'failed', 'filename': filename})


if __name__ == '__main__':
    app.run()
