#!bin/bash
# "$1" - command args 
for ((i = 1; i <= $1; i++))
do
    docker run -d jcass45/worker
done


