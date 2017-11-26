import sys
import os
import requests

from flask import Flask, request
from flask_restful import Resource, Api
import utils_server

app = Flask(__name__)
api = Api(app)

DS_ADDRESS = ('127.0.0.1', 5000)


class FileServer(Resource):
    def get(self, file_id):
        filename = utils_server.convert_file_id(file_id)
        with open(filename, 'r') as in_file:
            file_text = in_file.read()

        return {'file': file_text}, 200

    def post(self, file_id):
        new_text = request.get_json()['data']
        filename = utils_server.convert_file_id(file_id)
        with open(filename, 'w') as out_file:
            out_file.write(new_text)

        return '', 204


api.add_resource(FileServer, '/<int:file_id>')

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
