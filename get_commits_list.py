import requests

commits_list = []
resp = requests.get(
    'https://api.github.com/repos/JCass45/CS4400-Internet-Applications-Chat-Server/commits')

while 'next' in resp.links:
    for item in resp.json():
        commits_list.append(item['sha'])

    print(resp.links['next']['url'])
    resp = requests.get(resp.links['next']['url'])

for item in resp.json():
    commits_list.append(item['sha'])

print(len(commits_list))
