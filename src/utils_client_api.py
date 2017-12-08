from os import remove
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
    resp = requests.get(url_builder(
        machine_address[0],
        machine_address[1],
        file_id
    ))

    # Returns the text currently in the file on the fileserver
    return resp.json()['file'].strip()


def url_builder(ip, port, endpoints=''):
    return 'http://' + ip + ':' + str(port) + '/' + str(endpoints)


def get_file_location(file_id):
    resp = requests.get(
        'http://127.0.0.1:5000/files/{}/locate'.format(file_id)
    )

    if resp.status_code == 200:
        return (resp.json()['machine_ip'], resp.json()['machine_port'])

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


def get_file_age(file_id):
    resp = requests.get('http://127.0.0.1:5000/files/{}/age'.format(file_id))
    return int(resp.json()['file_age'])


def update_file_age(file_id, age):
    payload = {'file_age': age}
    requests.put(
        'http://127.0.0.1:5000/files/{}/age'.format(file_id),
        data=payload
    )


def get_file_lock(file_id):
    resp = requests.put('http://127.0.0.1:6000/{}'.format(file_id))

    if resp.status_code == 200:
        return resp.json()['lock']

    return False


def release_file_lock(file_id):
    requests.delete('http://127.0.0.1:6000/{}'.format(file_id))


def create_cached_copy(filename, data):
    with open(filename + '.txt', 'w') as cache_file:
        cache_file.write(data)


def cached_copy_exists(filename):
    try:
        open(filename + '.txt', 'r')
    except FileNotFoundError:
        return False

    return True


def update_cache(filename, file_id):
    with open(filename + '(remote).txt', 'w') as remote_file:
        # Downloads a local copy of the remote's version of the file
        machine_address = get_file_location(file_id)
        remote_file.write(read_from_node(machine_address, file_id))

        # Manually merge remote and local
        print('Remote version saved as {}(remote).txt'.format(filename))
        print('Press enter after manually merging changes into local copy to write')
        input()
        remove(filename + '(remote).txt')

    # Return merged file
    with open(filename + '.txt', 'r') as local_file:
        return local_file.read()
