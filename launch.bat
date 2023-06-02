@echo off

:: set DOCKER_COMPOSE_BIN="venv_podman/bin/podman-compose"
set @DOCKER_COMPOSE_BIN="docker-compose"

set @ENV_FILE=".env"

if exist ".env" (
    echo Found env file: %@ENV_FILE%
) else (
    echo Cannot find env file %@ENV_FILE%
    exit
)

%@DOCKER_COMPOSE_BIN% build

python generate_ts.py

echo Updating containers with genesis timestamp, this may take a while...
%@DOCKER_COMPOSE_BIN% build > NUL

%@DOCKER_COMPOSE_BIN% up
