from flask import Flask, jsonify
from flask import request
from flask_pymongo import PyMongo
from utils.robot_parser import parse_robot

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://N0e1:N0e1970126@ds351455.mlab.com:51455/colladarobots"
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



# TODO: file transfer. Currently using file path.
# POST /api/robot 
# Usage: Upload a robot file to the collection (updating database)
@app.route('/api/robot', methods=['POST'])
def post_upload_robot():
    if not request.json or not 'filename' in request.json:
        print(">> haha")
        #abort(400)
    print(">> req:")
    print(request.json)
    filename = request.json['filename']
    
    print(">> Uploading:", filename)
    target_data = parse_robot(filename) 

    exist_robot = mongo.db.robots.find_one({'name': target_data['name']})
    if exist_robot:
        print(">> ?")
        return jsonify({'response_code': 1, 'result': {'name': exist_robot['name'], 'manipulators': exist_robot['manipulators']}})
        #abort(400)

    new_id = mongo.db.robots.insert(target_data)
    print(">> Uploaded:", str(new_id))
    # new_robot = mongo.db.robots.find_one({'_id': {'\$oid': str(new_id)}})
    new_robot = mongo.db.robots.find_one({'name': target_data['name']})
    print(new_robot)
    return jsonify({'response_code': 0, 'result': {'name': new_robot['name'], 'manipulators': new_robot['manipulators']}})

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
