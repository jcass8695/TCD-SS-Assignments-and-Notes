import requests


def write_to_node(machine_address, file_id, data):
    if machine_address is not None:
        requests.post(
            url_builder(
                machine_address[0],
                machine_address[1],
                file_id
            ),
            json={'data': data}
        )


def read_from_node(machine_address, file_id):
    if machine_address is not None:
        resp = requests.get(url_builder(
            machine_address[0],
            machine_address[1],
            file_id
        ))

        # Prints the text currently in the file on the fileserver
        print(resp.json()['file'].strip())


def url_builder(ip, port, endpoints=''):
    return 'http://' + ip + ':' + str(port) + '/' + str(endpoints)


def get_file_location(file_id):
    resp = requests.get(
        'http://127.0.0.1:5000/files/{}/locate'.format(file_id)
    )

    if resp.status_code == 200:
        return resp.json()['machine_address']

    else:
        print(resp.json()['message'])
        return None


def get_file_id(filename):
    payload = {'filename': filename}
    resp = requests.get('http://127.0.0.1:5000/files', params=payload)

    if resp.status_code == 200:
        return resp.json()['file_id']

    else:
        print(resp.json()['message'])
        return None


def get_file_lock(file_id):
    resp = requests.put('http://127.0.0.1:6000/{}'.format(file_id))

    if resp.status_code == 200:
        return resp.json()['lock']

    return False


def release_file_lock(file_id):
    requests.delete('http://127.0.0.1:6000/{}'.format(file_id))
