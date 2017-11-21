from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class FileServer(Resource):
    def get(self):
        with open('test.txt', 'r') as in_file:
            file_text = in_file.read()
        return {'file': file_text}

    def post(self):
        new_text = request.form['data']
        with open('test.txt', 'w') as out_file:
            chars_written = out_file.write(new_text)
        return {'file': chars_written}


api.add_resource(FileServer, '/')

if __name__ == '__main__':
    app.run(debug=True)
