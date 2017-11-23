import requests
import utils


def run():
    open_file('test')
    write('test', 'This is a new test')


# Creates file on server if it doesn't already exist
def open_file(filename):
    resp = requests.post('http://127.0.0.1:5000/', json={'filename': filename})
    if resp.status_code == 200:
        machine_address, file_id = utils.get_file_location(filename)
        requests.post(
            utils.url_builder(machine_address[0], machine_address[1]),
            json={'fileid': file_id, 'data': ''}
        )

        print('{} created'.format(filename))
    else:
        print('{} already exists'.format(filename))


# Reads file from server
def read(filename):
    machine_address, file_id = utils.get_file_location(filename)
    if machine_address is not None:
        payload = {'fileid': file_id}
        r = requests.get(
            utils.url_builder(machine_address[0], machine_address[1]),
            params=payload
        )

        # Prints the text currently in the file on the fileserver
        print(r.json()['file'].strip())
    else:
        print('{} not found'.format(filename))


# Sends text to file on server. Currently overwrites entire file
def write(filename, changes):
    file_id = utils.get_file_id(filename)
    if file_id is not None:
        if utils.get_file_lock(file_id):
            print('Got lock')
            machine_address, _ = utils.get_file_location(filename)
            if machine_address is not None:
                requests.post(
                    utils.url_builder(machine_address[0], machine_address[1]),
                    json={'fileid': file_id, 'data': changes}
                )

                utils.release_file_lock(file_id)
            else:
                print('{} not found'.format(filename))
        else:
            print('Didn\'t get lock')


if __name__ == '__main__':
    run()
