import os
from shutil import rmtree
from re import match
import requests
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config


class Worker:
    '''
    A Worker calculates the average CC for a given commit in a Github repo

    The Master issues each Worker with a repo URL upon instantiation, and a
    commit SHA each time it asks for work. The Worker performs CC analysis on
    every file in the given commit and returns the average value to the Master.
    The Worker asks for work forever until the list of commits has been exhausted
    '''
    master_url = 'http://34.241.97.168:5000/'
    node_setup_url = 'http://34.241.97.168:5000/init'

    cc_path = ['./tmp']
    cc_config = Config(
        exclude='',
        ignore='venv',
        order=SCORE,
        no_assert=True,
        show_closures=False,
        min='A',
        max='F',
    )

    def __init__(self):
        self.token = self.get_token()
        self.finished = False
        self.files_list_url = requests.get(self.node_setup_url).json()['url']

    def do_work(self):
        '''
        Worker continuously asks Master for work until all work has been exhausted

        Worker is told to finish either when the Job Queue on the Masters end is empty
        or this Worker was the last to submit it's work.
        '''

        while not self.finished:
            sha = self.get_work()
            if sha is None:
                continue

            file_tree = self.get_file_tree(sha)
            self.get_files(file_tree)
            avg_cc = self.get_average_cc()
            self.return_work_result(avg_cc)
            print('SHA: {}'.format(sha))
            print(avg_cc)

    def get_token(self):
        '''Opens Github Personal Auth token securely'''

        with open('github-token', 'r') as f:
            return f.read().split()[0]

    def get_work(self):
        '''
        GET a commit SHA from the Master

        Worker asks Master for a commit SHA. Any response code
        other than a 200 means the Job Queue is finished and Worker
        should terminate.
        '''

        resp = requests.get(self.master_url)
        if resp.status_code == 200:
            return resp.json()['sha']

        self.finished = True

    def get_file_tree(self, sha):
        '''
        Recursively GET the file tree for a given commit SHA

        The file tree contains information on all of the directories
        and files (Blobs) in the given commit.
        '''

        payload = {
            'recursive': 'true',
            'access_token': self.token
        }

        resp = requests.get(self.files_list_url.format(sha), params=payload)
        if resp.status_code == 301:
            redirect_url = resp.headers['location'].split('?')[0]
            payload = {'access_token': self.token}
            resp = requests.get(redirect_url, params=payload)

        return resp.json()['tree']

    def get_files(self, file_tree):
        '''
        GET file contents of every Blob in the file tree and write
        to a temporary file
        '''

        os.makedirs('tmp')
        blob_urls = []
        for item in file_tree:
            if item['type'] == 'blob' and self.is_py_file(item['path']):
                blob_urls.append(item['url'])

        payload = {'access_token': self.token}
        headers = {'Accept': 'application/vnd.github.v3.raw'}
        for index, url in enumerate(blob_urls):
            resp = requests.get(url, params=payload, headers=headers)
            with open('./tmp/{}.py'.format(index), 'w') as tmp_file:
                tmp_file.write(resp.text)

    def get_average_cc(self):
        '''
        Calculate the CC of every file in the tmp directory of Blobs

        CCHarvester returns a block of metrics for each function, class and method
        in a given file in dict format. CC is contained in this dict and is totalled
        for the file. Tmp directory is cleaned up afterwards
        '''

        results = CCHarvester(self.cc_path, self.cc_config)._to_dicts()
        if results == {}:
            rmtree('tmp')
            return 0

        total_cc = 0
        for filename in results.values():
            file_cc = 0
            for block in filename:
                file_cc += block['complexity']

            total_cc += file_cc

        rmtree('tmp')
        return total_cc / len(results)

    def return_work_result(self, avg_cc):
        ''' Update Master with CC of latest commit'''

        if requests.put(self.master_url, data={'cc': avg_cc}).status_code == 503:
            self.finished = True

    def is_py_file(self, filename):
        '''
        Used to ensure CC is calculated on Python files only

        Radon only supports evaluation of Python files
        '''
        return True if match('.*\.py', filename) is not None else False


if __name__ == '__main__':
    worker = Worker()
    worker.do_work()
    print('Finished work')
