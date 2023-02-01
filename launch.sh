#!/bin/bash

# DOCKER_COMPOSE_BIN="venv_podman/bin/podman-compose"
DOCKER_COMPOSE_BIN="docker-compose"

$DOCKER_COMPOSE_BIN build

python3 generate_ts.py

echo "Updating containers with genesis timestamp, this may take a while..."
$DOCKER_COMPOSE_BIN build &> /dev/null

$DOCKER_COMPOSE_BIN up
