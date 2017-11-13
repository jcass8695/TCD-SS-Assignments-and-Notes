#!/bin/bash

echo "Enter the IP the servers should listen on, defaults to 0.0.0.0"
read IP
if [[ $# == 1 ]]; then
    if [[ -z "$1" ]]; then
        echo "Default"
        python3 src/server.py 0.0.0.0
    else
        python3 src/server.py $1
    fi
else
    echo "Expecting 1 argument only, the IP of the server"
fi
