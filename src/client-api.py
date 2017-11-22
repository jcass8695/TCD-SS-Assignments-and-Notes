import requests
import utils


def run():
    # read('test')
    # read('loremipsum')
    # write('test', 'This is a new test')
    # write('loremipsum', 'Brand new lorem ipsum')
    read('test')
    read('loremipsum')
    # open_file('open_file_test')
    # read('open_file_test')
    # write('file_that_dont_exist')


# Creates file on server if it doesn't already exist, else nothing
def open_file(filename):
    exists = utils.file_exists(filename)
    if not exists:
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
def write(filename, changes=''):
    machine_address, file_id = utils.get_file_location(filename)
    if machine_address is not None:
        requests.post(
            utils.url_builder(machine_address[0], machine_address[1]),
            json={'fileid': file_id, 'data': changes}
        )
    else:
        print('{} not found'.format(filename))


if __name__ == '__main__':
    run()
