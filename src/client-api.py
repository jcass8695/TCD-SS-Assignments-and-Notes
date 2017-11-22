import requests
import utils


def run():
    read('test')
    read('loremipsum')
    write('test', 'This is a new test')
    write('loremipsum', 'Brand new lorem ipsum')
    read('test')
    read('loremipsum')


def read(filename):
    machine_id, file_id = utils.get_file_location(filename)
    payload = {'fileid': file_id}
    r = requests.get(
        utils.url_builder(machine_id[0], machine_id[1]),
        params=payload
    )

    # Prints the text currently in the file on the fileserver
    print(r.json()['file'].strip())


def write(filename, changes):
    machine_id, file_id = utils.get_file_location(filename)
    r = requests.post(
        utils.url_builder(machine_id[0], machine_id[1]),
        json={'fileid': file_id, 'data': changes}
    )

    # Prints the number of characters written to the fileserver
    print(r.json()['file'])


if __name__ == '__main__':
    run()
