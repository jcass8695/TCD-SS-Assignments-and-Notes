from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, request

app = Flask(__name__)
api = Api(app)

# Map fileID to Locked(True/False)
LOCKED_FILES = {}


class LockServer(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('fileid')
        print(LOCKED_FILES)

    def get(self):
        fileid = int(self.parser.parse_args()['fileid'])
        if fileid in LOCKED_FILES.keys():
            locked = LOCKED_FILES[fileid]
            print(locked)
            if not locked:
                locked = True
                LOCKED_FILES[fileid] = True
                print('Lock on {}'.format(fileid))
                return {'lock': True}

            return {'lock': False}
        else:
            print('abort')
            abort(404)

    def post(self):
        fileid = request.get_json()['fileid']
        if fileid not in LOCKED_FILES.keys():
            print('New file added')
            LOCKED_FILES[fileid] = False
        else:
            abort(404)

    def delete(self):
        fileid = request.get_json()['fileid']
        if fileid in LOCKED_FILES.keys():
            locked = LOCKED_FILES[fileid]
            if locked:
                LOCKED_FILES[fileid] = False
                print('Lock on {} released'.format(fileid))
        else:
            abort(404)


api.add_resource(LockServer, '/')

if __name__ == '__main__':
    app.run(debug=True, port=6000)
