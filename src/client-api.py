import json
import requests
import utils


def run():
    read('test')
    write('test', 'This is a new test')
    read('test')


def read(filename):
    machine_id, file_id = utils.get_file_location(filename)
    r = requests.get(utils.url_builder(machine_id[0], machine_id[1]))
    print(r.json()['file'])


def write(filename, changes):
    machine_id, file_id = utils.get_file_location(filename)
    r = requests.post(
        utils.url_builder(machine_id[0], machine_id[1]),
        data={'data': changes}
    )

    print(r.json()['file'])


if __name__ == '__main__':
    run()
