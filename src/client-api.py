import requests
import utils_client_api


def run():
    open_file('test')
    read('test')
    write('test', 'This is a new test from client 1')
    read('test')


# Creates file on server if it doesn't already exist
def open_file(filename):
    resp = requests.post(
        'http://127.0.0.1:5000/files',
        json={'filename': filename}
    )

    if resp.status_code == 201:
        file_id = utils_client_api.get_file_id(filename)
        machine_address = utils_client_api.get_file_location(file_id)
        utils_client_api.write_to_node(machine_address, file_id, '')
        print('{} created'.format(filename))
    else:
        print(resp.json()['message'])


# Reads file from server
def read(filename):
    file_id = utils_client_api.get_file_id(filename)
    machine_address = utils_client_api.get_file_location(file_id)
    utils_client_api.read_from_node(machine_address, file_id)


# Sends text to file on server. Currently overwrites entire file
def write(filename, changes):
    file_id = utils_client_api.get_file_id(filename)
    if file_id is not None:
        if utils_client_api.get_file_lock(file_id):
            machine_address = utils_client_api.get_file_location(file_id)
            utils_client_api.write_to_node(machine_address, file_id, changes)
            utils_client_api.release_file_lock(file_id)
        else:
            print('Didn\'t get lock')


if __name__ == '__main__':
    run()
