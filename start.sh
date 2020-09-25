#!/bin/bash

echo "[*] Starting microservices-demo..."

# create docker network for communication between services
NETWORK_NAME=microservices-network

# shellcheck disable=SC2046
if [ -z $(docker network ls --filter name=^${NETWORK_NAME}$ --format="{{ .Name }}") ] ;

then
     docker network create ${NETWORK_NAME} ; 
fi

# run monitoring system

docker-compose -f ./monitoring/docker-compose.yml up -d &&
docker-compose -f ./microservices/docker-compose.yml -f ./microservices/docker-compose.logging.yml up -d

echo "[x] Microservices-demo started!"


