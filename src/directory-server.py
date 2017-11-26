from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import utils_server

app = Flask(__name__)
api = Api(app)

# MachineID: (MachineIP, MachinePORT)
MACHINES = {}
# MachineID: Num Files on Machine
MACHINE_LOAD = {}
# FileName: FileID
FILE_NAMES = {}
# FileID: MachineID
FILE_LOCATIONS = {}


# Returns file_id's and creates new File's
class DirServerFile(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('filename')

    # Get file_id of requested file
    def get(self):
        filename = self.parser.parse_args()['filename']
        if filename not in FILE_NAMES:
            return {'message': '{} does not exist, try opening it'.format(filename)}, 404

        return {'file_id': FILE_NAMES[filename]}

    # Create new file listing
    def post(self):
        filename = self.parser.parse_args()['filename']
        if filename in FILE_NAMES:
            return {'message': '{} already exists, try reading from it'.format(filename)}, 400

        else:
            file_id = len(FILE_NAMES)
            FILE_NAMES[filename] = file_id
            target_machine_id = utils_server.find_least_loaded_server(
                MACHINE_LOAD)
            FILE_LOCATIONS[file_id] = target_machine_id
            return '', 201


class DirServerLocate(Resource):
    def get(self, file_id):
        if file_id not in FILE_NAMES.values():
            print('File location not found')
            return {'message': '{} does not exist'.format(file_id)}, 404

        machine_id = FILE_LOCATIONS[file_id]
        return {'machine_address': MACHINES[machine_id]}, 200


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


api.add_resource(DirServerFile, '/files')
api.add_resource(DirServerLocate, '/files/<int:file_id>/locate')
api.add_resource(NodeSetup, '/init')

if __name__ == '__main__':
    app.run(debug=True)
