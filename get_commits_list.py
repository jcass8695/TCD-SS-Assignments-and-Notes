import requests


def run():
    commit_list_url = 'https://api.github.com/repos/JCass45/CS4400-Internet-Applications-Chat-Server/commits'

    # Get list of commits
    commits_list = []
    commits_to_file_num = {}
    with open('github-token', 'r') as f:
        token = f.read().split()[0]
        payload = {'access_token': token}

    resp = requests.get(
        'https://api.github.com/repos/JCass45/CS4400-Internet-Applications-Chat-Server/commits', params=payload)
    while 'next' in resp.links:
        for item in resp.json():
            commits_list.append(item['sha'])

        resp = requests.get(resp.links['next']['url'], params=payload)

    for item in resp.json():
        commits_list.append(item['sha'])

    print(commits_list)


if __name__ == '__main__':
    run()
