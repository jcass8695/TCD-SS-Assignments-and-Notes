from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return 'Hello shworld!\n'
    else:
        print('Hello world\n')
        return 'Hello shworld\n'
