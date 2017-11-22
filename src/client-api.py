import json
import requests
import utils


def run():
    read('test')


def read(filename):
    payload = {'filename': filename}
    r = requests.get('http://127.0.0.1:5000', params=payload)
    r_text = r.json()
    machine_id = r_text['machine_id']
    machine_ip = machine_id[0]
    machine_port = machine_id[1]
    file_id = r_text['file_id']

    r = requests.get(utils.url_builder(machine_ip, machine_port))
    print(r.json()['file'])


if __name__ == '__main__':
    run()
