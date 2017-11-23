import requests


def url_builder(ip, port, endpoints=''):
    return 'http://' + ip + ':' + str(port) + '/' + endpoints


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


def get_file_id(filename):
    payload = {'filename': filename}
    r = requests.get('http://127.0.0.1:5000/fileid', params=payload)
    if r.status_code != 404:
        return r.json()['fileid']
    else:
        print('{} does not exist'.format(filename))
        return None


def get_file_lock(fileid):
    payload = {'fileid': fileid}
    r = requests.get('http://127.0.0.1:6000/', params=payload)
    if r.status_code != 404:
        return r.json()['lock']

    # Returning true here, but should deal with the file
    # not existing on the Lock Server
    return False


def release_file_lock(fileid):
    r = requests.delete(
        'http://127.0.0.1:6000/',
        json={'fileid': fileid}
    )


def convert_fileid(file_id):
    return str(file_id) + '.txt'


# Returns server ID with the smallest number of files on it
def find_least_loaded_server(machine_load):
    return min(machine_load, key=machine_load.get)
