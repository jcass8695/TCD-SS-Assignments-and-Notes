def convert_file_id(file_id):
    return str(file_id) + '.txt'


def url_builder(ip, port, endpoints=''):
    return 'http://' + ip + ':' + str(port) + '/' + str(endpoints)


def find_least_loaded_server(machine_load):
    target_machine_id = min(machine_load, key=machine_load.get)
    machine_load[target_machine_id] += 1
    return target_machine_id


def file_missing_error(file_id):
    return {'message': '{} does not exist'.format(file_id)}, 404


def no_servers_error():
    return {'message': 'No server available to facilitate request'}, 503


def file_already_exists_error(file_id):
    return {'message': '{} already exists, try reading from it'.format(file_id)}, 400


def create_file_db_object(file_id, filename, file_age, machine_id):
    return {
        'file_id': file_id,
        'filename': filename,
        'file_age': file_age,
        'machine_id': machine_id
    }


def create_machine_db_object(machine_id, machine_address, machine_load):
    return {
        'machine_id': machine_id,
        'machine_address': machine_address,
        'machine_load': machine_load
    }
