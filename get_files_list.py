from re import match
from pprint import pprint
import requests


files_list_url = 'https://api.github.com/repos/JCass45/CS4400-Internet-Applications-Chat-Server/git/trees/{}'

with open('github-token', 'r') as f:
    token = f.read().split()[0]

# For a given sha return a list of file text


def get_files_for_sha(sha):
    blob_urls = {}
    files = []
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

    pprint(blob_urls)
    payload = {'access_token': token}
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    for url in blob_urls.values():
        resp = requests.get(url, params=payload, headers=headers)
        files.append(resp.text)

    print(files[0])


def is_code_file(filename):
    regex = '.*\.py|.*\.sh|.*\.c|.*\.cpp|.*\.h|.*\.txt|.*\.hs|.*\.rb|.*\.java|.*\.class|.*\.js|.*\.css|.*\.html'
    return True if match(regex, filename) is not None else False


if __name__ == '__main__':
    get_files_for_sha('23d29b5bd28a40bc6724a4b035bf427a9df45401')
