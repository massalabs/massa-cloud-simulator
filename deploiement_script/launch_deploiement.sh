#!/bin/bash

python3 generate_ts.py -f ./deploiement/nodes.configmap.yaml
kubectl apply -f ./deploiement/
