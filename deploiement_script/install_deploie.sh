#!/bin/bash

# Install Kubectl
# Source : https://kubernetes.io/fr/docs/tasks/tools/install-kubectl/
sudo apt-get update && sudo apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl

# Install Minikube
# Source : https://kubernetes.io/fr/docs/tasks/tools/install-minikube/
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube
sudo mkdir -p /usr/local/bin/
sudo install minikube /usr/local/bin/
minikube start
minikube status

# Install Kompose
# Source : https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/
curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.0/kompose-linux-amd64 -o kompose
chmod +x kompose
sudo mv ./kompose /usr/local/bin/kompose


# # Convert the docker-compose file to files that we can use with kubectl
# kompose convert
# kubectl apply -f node-1-service.yaml, node-2-service.yaml, node-1-deployment.yaml, massa-cloud-network-networkpolicy.yaml, node-2-deployment.yaml
