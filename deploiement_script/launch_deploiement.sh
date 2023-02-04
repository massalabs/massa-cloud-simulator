#!/bin/bash

python3 generate_ts.py -f nodes.configmap.yaml
kubectl apply -f .