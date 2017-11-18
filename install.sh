#!/bin/bash

echo "The only requirement for this server is python3"
if python3 & > /dev/null; then
    echo "Python 3 is installed"
else
    echo "Python 3 is not installed"
    echo "use sudo apt-get install python3 to install Python 3"
fi

echo "Run ./run.sh to start server"
