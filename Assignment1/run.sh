#!/bin/bash

echo "Enter the IP the servers should listen on, defaults to 0.0.0.0"
read IP

if [[ -z "$IP" ]]; then
    echo "Default"
    python3 src/server.py 0.0.0.0
else
    python3 src/server.py $IP
fi
