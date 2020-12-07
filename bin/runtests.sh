#!/bin/bash

docker-compose up -d
docker exec bookbnb-authserver_web bash -c 'while !</dev/tcp/db/5432; do sleep 1; done;'
docker exec bookbnb-authserver_web pytest --cov=authserver --color=yes

if [ ${1-"none"} == "no-lint" ]; then
	docker-compose down
else
	docker exec bookbnb-authserver_web pylint authserver
	docker-compose down
fi

