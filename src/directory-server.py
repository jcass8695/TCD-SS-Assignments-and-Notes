import requests
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, request
import utils

app = Flask(__name__)
api = Api(app)

# MachineID: (MachineIP, MachinePORT)
MACHINES = {}
# MachineID: Num Files on Machine
MACHINE_LOAD = {}
# FileName: FileID
FILE_NAMES = {}
# FileID: FileAge
# FILE_AGES = {1: 0, 2: 0}
# FileID: MachineID
FILE_LOCATIONS = {}


class DirServer(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('filename')

    # Get location of requested file
    def get(self):
        filename = self.parser.parse_args()['filename']
        if filename in FILE_NAMES.keys():
            file_id = FILE_NAMES[filename]
            machine_id = FILE_LOCATIONS[file_id]
            machine_address = MACHINES[machine_id]
            return {'file_id': file_id, 'machine_id': machine_address}
        else:
            abort(404)

    # Create new file mapping on server
    def post(self):
        filename = request.get_json()['filename']
        if filename not in FILE_NAMES.keys():
            file_id = len(FILE_NAMES) + 1

            # Put the new file on the server with the least number of files
            target_machine_id = utils.find_least_loaded_server(MACHINE_LOAD)
            FILE_NAMES[filename] = file_id
            FILE_LOCATIONS[file_id] = target_machine_id
            # FILE_AGES[file_id] = 0
            MACHINE_LOAD[target_machine_id] += 1

            # Notify Lock Server of this new file
            r = requests.post(
                'http://127.0.0.1:6000/',
                json={'fileid': file_id}
            )

            if r.status_code == 404:
                # TODO Take an action here
                pass
        else:
            abort(404)


class NodeSetup(Resource):
    # Setup newly instantiated node
    def post(self):
        machine_details = request.get_json()
        machine_ip = machine_details['ip']
        machine_port = machine_details['port']
        machine_id = len(MACHINES)
        MACHINES[machine_id] = (machine_ip, machine_port)
        MACHINE_LOAD[machine_id] = 0
        print('New machine added')
        print('ID: {}'.format(machine_id))
        print('IP: {}'.format(machine_ip))
        print('PORT: {}'.format(machine_port))
        print('------------')
        print(MACHINES)
        print(MACHINE_LOAD)


class FileId(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('filename')

    def get(self):
        filename = self.parser.parse_args()['filename']
        if filename in FILE_NAMES.keys():
            return {'fileid': FILE_NAMES[filename]}
        else:
            abort(404)


api.add_resource(DirServer, '/')
api.add_resource(NodeSetup, '/init')
api.add_resource(FileId, '/fileid')

if __name__ == '__main__':
    app.run(debug=True)
