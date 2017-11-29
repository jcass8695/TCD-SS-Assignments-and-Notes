import os
from shutil import rmtree
from pprint import pprint
from re import match
import requests
from radon.complexity import cc_rank, SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config


class Worker:
    files_list_url = 'https://api.github.com/repos/JCass45/CS4400-Internet-Applications-Chat-Server/git/trees/{}'
    master_url = 'http://127.0.0.1:5000/'
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

    def do_work(self):
        # while True:
        sha = self.get_work()
        file_tree = self.get_file_tree(sha)
        self.get_files(file_tree)
        print('SHA: {}'.format(sha))
        print(self.get_average_cc())

    def get_token(self):
        with open('github-token', 'r') as f:
            return f.read().split()[0]

    def get_work(self):
        return requests.get(self.master_url).json()['sha']

    def get_file_tree(self, sha):
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
        results = CCHarvester(self.cc_path, self.cc_config)._to_dicts()
        total_cc = 0
        for filename in results.values():
            file_cc = 0
            for block in filename:
                file_cc += block['complexity']

            total_cc += file_cc

        rmtree('tmp')
        return total_cc / len(results)

    def is_py_file(self, filename):
        return True if match('.*\.py', filename) is not None else False


if __name__ == '__main__':
    worker = Worker()
    worker.do_work()
