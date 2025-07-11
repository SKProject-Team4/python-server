#!/bin/bash 

# echo log server deploy
# docker compose up -f docker-compose-log.yaml -d

# 
export MYSQL_VOLUME_PATH="C:\Users\ender\Desktop\langchainServer\infra\mysql"
export MYSQL_USER="test"
export MYSQL_PASSWORD="test"
export MYSQL_ROOT_PASSWORD="test"
export MYSQL_DATABASE="planner_db"


echo main server deploy 
docker compose build --no-cache
docker compose up -d 