from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import utils

app = Flask(__name__)
api = Api(app)

MACHINES = {1: ('127.0.0.1', 5001)}
MACHINE_LOAD = {1: 2}
FILENAMES = {'test': (1, 1), 'loremipsum': (2, 1)}


class DirectoryServerReadWrite(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('filename')

    def get(self):
        filename = self.parser.parse_args()['filename']
        if filename in FILENAMES.keys():
            file_id, machine_id = FILENAMES[filename]
            machine_address = MACHINES[machine_id]
            return {'file_id': file_id, 'machine_id': machine_address}
        else:
            abort(404)


class DirectoryServerCreate(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('filename')
        self.file_id_count = 2

    def get(self):
        filename = self.parser.parse_args()['filename']
        if filename not in FILENAMES.keys():
            self.file_id_count += 1
            file_id = self.file_id_count

            # Put the new file on the server with the least number of files
            target_machine_id = utils.find_least_loaded_server(MACHINE_LOAD)
            FILENAMES[filename] = (file_id, target_machine_id)
            print(MACHINE_LOAD)
            MACHINE_LOAD[target_machine_id] += 1
            print(MACHINE_LOAD)
            exists = False
        else:
            exists = True

        return {'exists': exists}


api.add_resource(DirectoryServerReadWrite, '/')
api.add_resource(DirectoryServerCreate, '/create')

if __name__ == '__main__':
    app.run(debug=True)
