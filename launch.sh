#! /bin/bash

python3 generate_ts.py

docker-compose build

docker-compose up
