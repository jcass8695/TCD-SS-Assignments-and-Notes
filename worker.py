import os
from shutil import rmtree
from pprint import pprint
from re import match
import requests
from radon.complexity import cc_rank, SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config


def work():
    files_list_url = 'https://api.github.com/repos/JCass45/CS4400-Internet-Applications-Chat-Server/git/trees/{}'
    with open('github-token', 'r') as f:
        token = f.read().split()[0]

    blob_urls = {}
    files = []
    cc = 0
    sha = requests.get('http://127.0.0.1:5000/').json()['sha']
    payload = {
        'recursive': 'true',
        'access_token': token
    }

    # Get file tree for given commit SHA
    resp = requests.get(files_list_url.format(sha), params=payload)
    if resp.status_code == 301:
        redirect_url = resp.headers['location'].split('?')[0]
        payload = {'access_token': token}
        resp = requests.get(redirect_url, params=payload)

    file_tree = resp.json()['tree']

    # Separate Blobs from Directories (Blobs contain only SHA's)
    for item in file_tree:
        if item['type'] == 'blob' and is_py_file(item['path']):
            blob_urls[item['path']] = item['url']

    # Get file contents for each Blob
    payload = {'access_token': token}
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    for url in blob_urls.values():
        resp = requests.get(url, params=payload, headers=headers)
        files.append(resp.text)

    # Write Blob contents out to a python file
    os.makedirs('tmp')
    for index, text in enumerate(files):
        with open('./tmp/{}.py'.format(index), 'w') as tmp_file:
            tmp_file.write(text)

    path = ['./tmp']
    config = Config(
        exclude='',
        ignore='venv',
        order=SCORE,
        no_assert=True,
        show_closures=False,
        min='A',
        max='F',
    )

    h = CCHarvester(path, config)
    # pprint(h._to_dicts())
    print(calc_avg_cc(h._to_dicts()))
    rmtree('tmp')


def is_py_file(filename):
    regex = '.*\.py'
    return True if match(regex, filename) is not None else False


def calc_avg_cc(results):
    total_cc = 0
    for filename in results.values():
        file_cc = 0
        # print(filename)
        for block in filename:
            file_cc += block['complexity']

        total_cc += file_cc

    return total_cc / len(results)


if __name__ == '__main__':
    work()
    print('Done work')
