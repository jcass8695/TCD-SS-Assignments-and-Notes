from time import sleep
import requests
import utils_client_api as utils

# FileID: FileAge
OPEN_FILES = {}


def run():
    # open_file('test2.txt')
    read('test2.txt')
    # write('test', 'This is a new test from client 1')
    # read('test')

    # sleep(15)

    # write('test', 'This is a cache invalidation test')


# Creates file on server if it doesn't already exist
def open_file(filename):
    resp = requests.post(
        'http://127.0.0.1:5000/files',
        json={'filename': filename}
    )

    file_id = utils.get_file_id(filename)
    if resp.status_code == 201:
        machine_address = utils.get_file_location(file_id)
        utils.write_to_node(machine_address, file_id, '')
        print('{} created'.format(filename))

    else:
        print(resp.json()['message'])

    OPEN_FILES[file_id] = utils.get_file_age(file_id)


# Reads file from server
def read(filename):
    if utils.cached_copy_exists(filename):
        with open(filename + '.txt', 'r') as cache_file:
            print('Cache hit')
            print(cache_file.read())

    else:
        print('Cache miss')
        file_id = utils.get_file_id(filename)
        if file_id:
            machine_address = utils.get_file_location(file_id)
            if machine_address:
                text = utils.read_from_node(machine_address, file_id)
                utils.create_cached_copy(filename, text)
                OPEN_FILES[file_id] = utils.get_file_age(file_id)
                print(text)


# Sends text to file on server or cached version. Currently overwrites entire file
def write(filename, changes):
    file_id = utils.get_file_id(filename)
    if file_id:
        remote_age = utils.get_file_age(file_id)
        if remote_age > OPEN_FILES[file_id]:
            print('Cache invalid')
            OPEN_FILES[file_id] = remote_age
            write(filename, utils.update_cache(filename, file_id))

        if utils.get_file_lock(file_id):
            OPEN_FILES[file_id] += 1
            utils.update_file_age(file_id, OPEN_FILES[file_id])
            machine_address = utils.get_file_location(file_id)
            utils.write_to_node(machine_address, file_id, changes)
            utils.release_file_lock(file_id)
        else:
            print('Didn\'t get lock, try again later')


if __name__ == '__main__':
    run()
