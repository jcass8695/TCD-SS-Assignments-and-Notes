from flask import Flask
from flask_restful import Resource, Api, abort
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
api = Api(app)
locks_collection = MongoClient().distrib_filesystem.ls_files


class LockServer(Resource):
    def put(self, file_id):
        result = locks_collection.find_one(
            {'_id': ObjectId(file_id)}
        )
        if result:
            if not result['locked']:
                locks_collection.update_one(
                    {'_id': ObjectId(file_id)},
                    {'$set': {'locked': 1}}
                )
                print('{} locked'.format(file_id))
                return {'lock': True}

            return {'lock': False}
        else:
            locks_collection.insert_one(
                {'_id': ObjectId(file_id), 'locked': 1}
            )
            print('{} locked'.format(file_id))
            return {'lock': True}

    def delete(self, file_id):
        result = locks_collection.find_one(
            {'_id': ObjectId(file_id)}
        )
        if result:
            locks_collection.update_one(
                {'_id': ObjectId(file_id)},
                {'$set': {'locked': 0}}
            )
            print('{} unlocked'.format(file_id))
            return '', 200

        abort(404)


api.add_resource(LockServer, '/<string:file_id>')

if __name__ == '__main__':
    app.run(debug=True, port=6000)
