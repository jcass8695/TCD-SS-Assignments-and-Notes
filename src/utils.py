import requests


def url_builder(ip, port):
    return 'http://' + ip + ':' + str(port)


def get_file_location(filename):
    payload = {'filename': filename}
    r = requests.get('http://127.0.0.1:5000', params=payload)
    r_text = r.json()
    machine_id = r_text['machine_id']
    file_id = r_text['file_id']

    return machine_id, file_id
