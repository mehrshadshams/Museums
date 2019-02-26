#! /usr/bin/env sh
docker exec -it $(docker ps | grep museums_service | awk '/ / {print $1}') tail -f /app/logs/error.log