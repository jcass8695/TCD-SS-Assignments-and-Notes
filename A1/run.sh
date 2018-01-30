#!/bin/bash

if (( $# <= 1 )); then
    if [[ -z "$1" ]]; then
        python3 src/server.py 0.0.0.0
    else
        python3 src/server.py $1
    fi
else
    echo "Expecting 1 argument, the IP of the server or nothing"
fi
