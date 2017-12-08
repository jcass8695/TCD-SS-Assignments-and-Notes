from flask import Flask
from flask_restful import Resource, Api, reqparse, request
from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
from bson.errors import InvalidId
import utils_server

app = Flask(__name__)
api = Api(app)
files_collection = MongoClient().distrib_filesystem.ds_files
machines_collection = MongoClient().distrib_filesystem.ds_machines


class DirServerFile(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('filename')

    # Get file_id of requested file
    def get(self):
        filename = self.parser.parse_args()['filename']
        try:
            file_id = str(files_collection.find_one(
                {'file_name': filename}
            )['_id'])

        except TypeError:
            return utils_server.file_missing_error(filename)

        return {'file_id': file_id}

    # Create new file listing
    def post(self):
        filename = self.parser.parse_args()['filename']
        result = files_collection.find_one({'file_name': filename})
        if result:
            return utils_server.file_already_exists_error(str(result['_id']))

        else:
            try:
                target_machine_id = str(machines_collection.find_one(
                    sort=[('machine_load', ASCENDING)]
                )['_id'])

                files_collection.insert_one({
                    'file_name': filename,
                    'file_age': 1,
                    'machine_id': target_machine_id
                })

                return '', 201

            except TypeError:
                return utils_server.no_servers_error()


class DirServerLocate(Resource):
    def get(self, file_id):
        try:
            machine_id = files_collection.find_one(
                {'_id': ObjectId(file_id)}
            )['machine_id']

            machine_address = machines_collection.find_one(
                {'_id': ObjectId(machine_id)}
            )

            return {
                'machine_ip': machine_address['machine_ip'],
                'machine_port': int(machine_address['machine_port'])
            }, 200

        except (TypeError, InvalidId):
            return utils_server.file_missing_error(file_id), 404


class DirServerAge(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('new_age')

    def get(self, file_id):
        try:
            file_age = files_collection.find_one(
                {'_id': ObjectId(file_id)}
            )['file_age']

            return {'file_age': file_age}, 200

        except (TypeError, InvalidId):
            return utils_server.file_missing_error(file_id)

    def put(self, file_id):
        new_age = self.parser.parse_args()['new_age']
        if files_collection.update_one({'_id': ObjectId(file_id)}, {'$set': {'file_age': new_age}}):
            return '', 204

        return utils_server.file_missing_error(file_id)


class NodeSetup(Resource):
    # Setup newly instantiated node
    def post(self):
        machine_details = request.get_json()
        machine_ip = machine_details['ip']
        machine_port = machine_details['port']
        result = machines_collection.insert_one({
            'machine_load': 0,
            'machine_ip': machine_ip,
            'machine_port': machine_port
        })
        print('New machine added')
        print('ID: {}'.format(str(result.inserted_id)))
        print('IP: {}'.format(machine_ip))
        print('PORT: {}'.format(machine_port))
        print('------------')


api.add_resource(DirServerFile, '/files')
api.add_resource(DirServerLocate, '/files/<string:file_id>/locate')
api.add_resource(DirServerAge, '/files/<string:file_id>/age')
api.add_resource(NodeSetup, '/init')

if __name__ == '__main__':
    app.run(debug=True)
