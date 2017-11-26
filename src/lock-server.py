from flask import Flask
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

# Map fileID to Locked(True/False)
LOCKED_FILES = {}


class LockServer(Resource):
    def put(self, file_id):
        if file_id in LOCKED_FILES:
            if not LOCKED_FILES[file_id]:
                LOCKED_FILES[file_id] = True
                print('Lock on {} taken'.format(file_id))
                return {'lock': True}

            return {'lock': False}
        else:
            LOCKED_FILES[file_id] = True
            return {'lock': True}

    def delete(self, file_id):
        if file_id in LOCKED_FILES:
            if LOCKED_FILES[file_id]:
                LOCKED_FILES[file_id] = False
                print('Lock on {} released'.format(file_id))
        else:
            abort(404)


api.add_resource(LockServer, '/<int:file_id>')

if __name__ == '__main__':
    app.run(debug=True, port=6000)
