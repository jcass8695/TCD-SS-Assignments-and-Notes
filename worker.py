from pprint import pprint
from re import match
import requests
from radon.complexity import cc_visit


def work():
    files_list_url = 'https://api.github.com/repos/JCass45/CS4400-Internet-Applications-Chat-Server/git/trees/{}'
    with open('github-token', 'r') as f:
        token = f.read().split()[0]

    blob_urls = {}
    files = []
    sha = requests.get('http://127.0.0.1:5000/').json()['sha']
    payload = {
        'recursive': 'true',
        'access_token': token
    }

    resp = requests.get(files_list_url.format(sha), params=payload)
    if resp.status_code == 301:
        redirect_url = resp.headers['location'].split('?')[0]
        payload = {'access_token': token}
        resp = requests.get(redirect_url, params=payload)

    file_tree = resp.json()['tree']
    for item in file_tree:
        if item['type'] == 'blob' and is_code_file(item['path']):
            blob_urls[item['path']] = item['url']

    payload = {'access_token': token}
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    for url in blob_urls.values():
        resp = requests.get(url, params=payload, headers=headers)
        files.append(resp.text)


def is_code_file(filename):
    regex = '.*\.py|.*\.sh|.*\.c|.*\.cpp|.*\.h|.*\.txt|.*\.hs|.*\.rb|.*\.java|.*\.class|.*\.js|.*\.css|.*\.html'
    return True if match(regex, filename) is not None else False


if __name__ == '__main__':
    work()
    print('Done work')
