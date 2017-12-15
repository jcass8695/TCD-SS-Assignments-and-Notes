#! /bin/bash
. venv/bin/activate
mongod --quiet --dbpath ./db
echo DB daemon started
