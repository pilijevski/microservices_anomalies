#!/bin/bash

docker start $(docker ps -aq --filter "name=microservices_user-sim_1")
