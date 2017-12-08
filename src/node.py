import sys
import os
import requests

from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson import ObjectId
import utils_server

app = Flask(__name__)
api = Api(app)
files_collection = MongoClient().distrib_filesystem.node_files

DS_ADDRESS = ('127.0.0.1', 5000)


class FileServer(Resource):
    def get(self, file_id):
        file_text = files_collection.find_one(
            {'_id': ObjectId(file_id)}
        )['file_text']

        return {'file': file_text}, 200

    def post(self, file_id):
        new_text = request.get_json()['data']
        files_collection.update_one(
            {'_id': ObjectId(file_id)},
            {'$set': {'_id': ObjectId(file_id), 'file_text': new_text}},
            upsert=True
        )
        return '', 204


api.add_resource(FileServer, '/<string:file_id>')

if __name__ == '__main__':
    if len(sys.argv) == 3:
        # Flask runs twice in debug mode, this prevents setting the node up twice
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            print('Initing node')
            requests.post(
                utils_server.url_builder(DS_ADDRESS[0], DS_ADDRESS[1], 'init'),
                json={'ip': sys.argv[1], 'port': sys.argv[2]}
            )

        app.run(debug=True, host=sys.argv[1], port=int(sys.argv[2]))
    else:
        print('Please supply an IP and Port')
