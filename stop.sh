#!/bin/bash

echo "[*] Stopping containers..."
docker-compose -f ./monitoring/docker-compose.yml down  &&
docker-compose -f ./microservices/docker-compose.yml -f ./microservices/docker-compose.logging.yml down 

docker network rm microservices-network

echo "[x] Microservices-demo stopped sucessfully!"