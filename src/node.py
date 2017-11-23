import sys
import os
import requests

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import utils

app = Flask(__name__)
api = Api(app)

DS_ADDRESS = ('127.0.0.1', 5000)


class FileServer(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('fileid')

    def get(self):
        file_id = self.parser.parse_args()['fileid']
        filename = utils.convert_fileid(file_id)
        with open(filename, 'r') as in_file:
            file_text = in_file.read()

        return {'file': file_text}

    def post(self):
        file_id = request.get_json()['fileid']
        new_text = request.get_json()['data']
        filename = utils.convert_fileid(file_id)
        with open(filename, 'w') as out_file:
            chars_written = out_file.write(new_text)

        return {'file': chars_written}


api.add_resource(FileServer, '/')

if __name__ == '__main__':
    if len(sys.argv) == 3:
        # Flask runs twice in debug mode, this prevents setting the node up twice
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            print('Initing node')
            requests.post(
                utils.url_builder(DS_ADDRESS[0], DS_ADDRESS[1], 'init'),
                json={'ip': sys.argv[1], 'port': sys.argv[2]}
            )

        app.run(debug=True, host=sys.argv[1], port=int(sys.argv[2]))
    else:
        print('Please supply an IP and Port')
