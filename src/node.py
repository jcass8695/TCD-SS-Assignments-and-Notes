from flask import Flask
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

class FileServer(Resource):
    def get(self):
        with open('test.txt', 'r') as file:
            file_str = file.read()
        
        return file_str

api.add_resource(FileServer, '/')

if __name__ == '__main__':
    app.run(debug=True)      
