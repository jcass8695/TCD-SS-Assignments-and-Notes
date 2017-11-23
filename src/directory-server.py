from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, request
import utils

app = Flask(__name__)
api = Api(app)

MACHINES = {}
MACHINE_LOAD = {}
FILENAMES = {'test': (1, 0), 'loremipsum': (2, 0)}


class DirServer(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('filename')

    # Get location of requested file
    def get(self):
        filename = self.parser.parse_args()['filename']
        if filename in FILENAMES.keys():
            file_id, machine_id = FILENAMES[filename]
            machine_address = MACHINES[machine_id]
            return {'file_id': file_id, 'machine_id': machine_address}
        else:
            abort(404)

    # Create new file mapping on server
    def post(self):
        filename = request.get_json()['filename']
        if filename not in FILENAMES.keys():
            file_id = len(FILENAMES) + 1

            # Put the new file on the server with the least number of files
            target_machine_id = utils.find_least_loaded_server(MACHINE_LOAD)
            FILENAMES[filename] = (file_id, target_machine_id)
            MACHINE_LOAD[target_machine_id] += 1
            return
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


api.add_resource(DirServer, '/')
api.add_resource(NodeSetup, '/init')

if __name__ == '__main__':
    app.run(debug=True)
