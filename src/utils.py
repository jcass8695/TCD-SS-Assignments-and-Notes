import requests


def url_builder(ip, port):
    return 'http://' + ip + ':' + str(port)


def get_file_location(filename):
    payload = {'filename': filename}
    r = requests.get('http://127.0.0.1:5000', params=payload)
    if r.status_code != 404:
        r_text = r.json()
        machine_id = r_text['machine_id']
        file_id = r_text['file_id']
    else:
        machine_id = None
        file_id = None

    return machine_id, file_id


def file_exists(filename):
    payload = {'filename': filename}
    r = requests.get('http://127.0.0.1:5000/create', params=payload)
    return r.json()['exists']


def convert_fileid(file_id):
    return str(file_id) + '.txt'


# Returns server ID with the smallest number of files on it
def find_least_loaded_server(machine_load):
    return min(machine_load, key=machine_load.get)
