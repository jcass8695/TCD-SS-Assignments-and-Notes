from pymongo import MongoClient
from bson import ObjectId
import requests
import utils_client_api as utils

cache_collection = MongoClient().distrib_filesystem.api_files
# FileID: FileAge
OPEN_FILES = {}


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


# Reads file from server
def read(filename):
    # Check for cache
    try:
        cache = cache_collection.find_one(
            {'file_name': filename}
        )['cached_text']
        print('Cache Hit!', cache, sep='\n')

    except (TypeError, KeyError):
        print('Cache Miss...')
        file_id = utils.get_file_id(filename)
        if file_id:
            machine_address = utils.get_file_location(file_id)
            if machine_address:
                age = utils.get_file_age(file_id)
                text = utils.read_from_node(machine_address, file_id)
                cache_collection.insert_one({
                    'file_name': filename,
                    'cached_text': text,
                    'cache_age': age
                })
                print(text)


# Sends text to file on server
def write(filename, changes):
    file_id = utils.get_file_id(filename)
    if file_id:
        try:
            # Check if file being written to is cached
            remote_age = utils.get_file_age(file_id)
            cache_age = cache_collection.find_one(
                {'file_name': filename}
            )['cache_age']

            if remote_age > cache_age:
                print('Cache invalid')
                new_text = utils.update_cache(file_id)
                cache_collection.update_one(
                    {'file_name': filename},
                    {'$set': {'cached_text': new_text, 'cache_age': remote_age + 1}}
                )

                print('Cache revalidated')
                return write(filename, new_text)

        except TypeError:
            # File being written to is not cached
            pass

        if utils.get_file_lock(file_id):
            utils.update_file_age(file_id)
            machine_address = utils.get_file_location(file_id)
            utils.write_to_node(machine_address, file_id, changes)
            utils.release_file_lock(file_id)
        else:
            print('Didn\'t get lock, try again later')
