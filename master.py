from collections import deque
from threading import Lock
import requests
from flask import Flask
from flask_restful import Resource, Api, request

app = Flask(__name__)
api = Api(app)

JOB_QUEUE = deque()
JOB_QUEUE_LOCK = Lock()
CC = []
CC_LOCK = Lock()


class Master(Resource):
    def get(self):
        with JOB_QUEUE_LOCK:
            return {'sha': JOB_QUEUE.popleft()}

    def put(self):
        new_cc = int(request.form['cc'])
        with CC_LOCK:
            CC.append(new_cc)
            if len(CC) == TOTAL_COMMITS:
                shutdown_server()

        return '', 204


def get_commits():
    '''
    Retrieves SHA's for every commit in the CS4400 Chat Server repository by Jack Cassidy
    and fills the Job Queue
    '''

    commit_list_url = 'https://api.github.com/repos/JCass45/TCD-JS-Assignments-and-Notes/commits'
    with open('github-token', 'r') as f:
        token = f.read().split()[0]
        payload = {'access_token': token}

    resp = requests.get(commit_list_url, params=payload)

    # Repositories with more than 30 commits are pagianated
    # and require additional requests
    while 'next' in resp.links:
        for item in resp.json():
            JOB_QUEUE.append(item['sha'])

        resp = requests.get(resp.links['next']['url'], params=payload)

    for item in resp.json():
        JOB_QUEUE.append(item['sha'])


def calc_avg_cc():
    print('-----AVG CC: {}-----'.format(sum(CC) / len(CC)))


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


api.add_resource(Master, '/')

if __name__ == '__main__':
    get_commits()
    global TOTAL_COMMITS
    TOTAL_COMMITS = len(JOB_QUEUE)
    app.run(debug=False)
    print('-----Shutting Down Server-----')
    calc_avg_cc()
