def convert_file_id(file_id):
    return str(file_id) + '.txt'


def url_builder(ip, port, endpoints=''):
    return 'http://' + ip + ':' + str(port) + '/' + str(endpoints)


def find_least_loaded_server(machine_load):
    target_machine_id = min(machine_load, key=machine_load.get)
    machine_load[target_machine_id] += 1
    return target_machine_id
