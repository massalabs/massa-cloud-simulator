#!/bin/bash

set -e

DOCKER_COMPOSE_BIN="../massa-cloud-simulator/venv_podman/bin/podman-compose"
# DOCKER_COMPOSE_BIN="docker-compose"

ENV_FILE=".env"
if [ ! -e "$ENV_FILE" ]
then
    echo "Cannot find env file ${ENV_FILE}" >&2
    exit 1
else
    echo "Found env file: $ENV_FILE"
fi

$DOCKER_COMPOSE_BIN build

python3 generate_ts.py

echo "Updating containers with genesis timestamp, this may take a while..."
$DOCKER_COMPOSE_BIN build &> /dev/null

$DOCKER_COMPOSE_BIN up
