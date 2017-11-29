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

COMMIT_LIST_URL = 'https://api.github.com/repos/JCass45/CS4400-Internet-Applications-Repo-Complexity/commits'
FILES_LIST_URL = 'https://api.github.com/repos/JCass45/CS4400-Internet-Applications-Repo-Complexity/git/trees/{}'

TOTAL_COMMITS = 0


class Master(Resource):
    '''
    Master issues Workers with commit SHA's for a given repo
    and accepts the average CC of a commit from Workers
    '''

    def get(self):
        with JOB_QUEUE_LOCK:
            try:
                return {'sha': JOB_QUEUE.popleft()}

            except IndexError:
                return '', 204

    def put(self):
        new_cc = float(request.form['cc'])
        with CC_LOCK:
            CC.append(new_cc)
            if len(CC) == TOTAL_COMMITS:
                shutdown_server()
                return '', 503

        return '', 204


class NodeSetup(Resource):
    ''' Issues newly instantiated Workers with a URL to access commits '''

    def get(self):
        print('New node joined')
        return {'url': FILES_LIST_URL}


def get_commits():
    '''
    Retrieves SHA's for every commit in the CS4400 Repo Complexity repository by Jack Cassidy,
    and fills the Job Queue
    '''

    with open('github-token', 'r') as f:
        token = f.read().split()[0]
        payload = {'access_token': token}

    resp = requests.get(COMMIT_LIST_URL, params=payload)

    # Repositories with more than 30 commits are pagianated
    # and require additional requests
    while 'next' in resp.links:
        for item in resp.json():
            JOB_QUEUE.append(item['sha'])

        resp = requests.get(resp.links['next']['url'], params=payload)

    for item in resp.json():
        JOB_QUEUE.append(item['sha'])


def calc_avg_cc():
    ''' Calculate and print the average cyclomatic complexity for the repository '''

    print('-----AVG CC: {}-----'.format(sum(CC) / len(CC)))


def shutdown_server():
    ''' Snippet from flask-restful docs to shutdown a flask server '''

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


api.add_resource(Master, '/')
api.add_resource(NodeSetup, '/init')

if __name__ == '__main__':
    get_commits()
    TOTAL_COMMITS = len(JOB_QUEUE)
    app.run(debug=False)
    print('\n-----Shutting Down Server-----')
    calc_avg_cc()
