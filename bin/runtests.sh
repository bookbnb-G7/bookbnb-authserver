#!/bin/bash

docker-compose up -d

echo "controlando inicio servidor";

until curl -o /dev/null -s --connect-timeout 1 'http://localhost:3000';
do
    echo "Esperando 1 seg(s) a que el servidor se inicie";
    sleep 1;
done;

docker exec bookbnb-authserver_web pytest --cov=authserver --color=yes
docker-compose down

