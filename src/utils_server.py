def url_builder(ip, port, endpoints=''):
    return 'http://' + ip + ':' + str(port) + '/' + str(endpoints)


def file_missing_error(file_id):
    return {'message': '{} does not exist'.format(file_id)}, 404


def no_servers_error():
    return {'message': 'No server available to facilitate request'}, 503


def file_already_exists_error(file_id):
    return {'message': '{} already exists, try reading from it'.format(file_id)}, 400
