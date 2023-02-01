# Massa cloud simulator

## Setup

Install the following packages:

* [Docker](https://www.docker.com)
* [Python3](https://www.python.org)

Create a .env file:

* ```cp -v env.sample .env```
* [Optional] edit and tweak it

## Running the simulator locally (via docker compose)

```commandline
./launch.sh
```

Note: for now, the simulator runs 2 containers:
* node_1_container:
  * **genesis node**
    * start before the genesis timestamp
  * ip: 11.0.0.11
  * api ports are the default ones (33034 & 33035)
* node_2_container: node that bootstrap 
  * bootstrap on node 1
    * start after the genesis timestamp
  * ip: 11.0.0.12
  * api ports -> 34034 & 34035

## Running tests

Setup:

```commandline
python3 -m venv venv_tests
venv_tests/bin/python -m pip install -r requirements_tests.txt
```

Run:

```commandline
venv_tests/bin/python test_1.py
```

## Dev

Usefull docker commands

Open a shell in a running container

```commandline
    docker exec -it CONTAINER_NAME bash
```

View the logs of a container:
```commandline
    docker logs -f CONTAINER_NAME
```

Inspect containers:
```commandline
    docker container inspect CONTAINER_NAME_1 CONTAINER_NAME_2 | grep -i IPAddress
```
