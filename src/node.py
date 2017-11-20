from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class FileServer(Resource):
    def get(self):
        with open('src/test.txt', 'r') as in_file:
            file_str = in_file.read()
        return file_str

    def put(self):
        new_text = request.form['data']
        with open('src/test.txt', 'w') as out_file:
            print(out_file.write(new_text + '\n'))
        return 'write successful'


api.add_resource(FileServer, '/')

if __name__ == '__main__':
    app.run(debug=True)
