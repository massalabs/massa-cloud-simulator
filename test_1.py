import json
import argparse
import requests


def get_env_data_as_dict(env_path: str) -> dict:
    env_dict = {}
    with open(env_path) as f:
        lines = f.read().splitlines()  # Removes \n from lines
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if "#" in line:
            line = line.split("#")[0].strip()
        key, value = line.split("=", maxsplit=1)
        env_dict[key] = value
    return env_dict


def get_address_from_env(env_dict: dict) -> str:
    node_1_address = env_dict["NODE_1_ADDRESS"]
    node_2_address = env_dict["NODE_2_ADDRESS"]
    print("node_1_address = ", node_1_address)
    print("node_2_address = ", node_2_address)
    return node_1_address, node_2_address


def stop_node(url_public: str):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "stop_node",
        "id": 0
    })
    response = requests.post(url_public, data=payload, headers=headers)
    return response.json()


def get_status(url_public: str):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_status",
        "id": 0,
        "params": []
    })
    response = requests.post(url_public, data=payload, headers=headers)
    return response.json()


def check_peers_ban(url_public: str) -> int:
    get_status_value = get_status(url_public)
    peers_ban = get_status_value["result"]["network_stats"]["banned_peer_count"]
    if peers_ban == 0:
        print("No node banned")
    else:
        print("Number of node banned:", peers_ban)
    return peers_ban


def get_cliques(url_public: str):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_cliques",
        "id": 0,
        "params": []
    })
    response = requests.post(url_public, data=payload, headers=headers)
    return response.json()


def get_addresses(url_public: str, node_1_addr: str, node_2_addr: str):
    print(f"node_2_addr = @{node_2_addr}@")
    print(type(node_2_addr))

    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_addresses",
        "id": 0,
        "params": [["A12La217C4BvwcndCmy1yPVo2eSvwV4Zw7R2feGX5MqLopBKipJY"]]
    })
    response = requests.post(url_public, data=payload, headers=headers)
    return response.json()


def node_peers_whitelist(url_public: str):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "node_peers_whitelist",
        "id": 0,
        "params": []
    })
    response = requests.post(url_public, data=payload, headers=headers)
    return response.json()


def main():
    url_public = "http://127.0.0.1:33035"
    url_private = "http://127.0.0.1:33034"
    #env_dict = get_env_data_as_dict(".env")
    #node_1_addr, node_2_addr = get_address_from_env(env_dict)

    #stop_node_value = stop_node(url_private)
    #print("stop_node_value = ", stop_node_value)

    get_status_value = get_status(url_public)
    print("get_status_value = ", get_status_value)

    #check_ban_value = check_peers_ban(url_public)
    ##print("check_ban_value =", check_ban_value)

    #get_cliques_value = get_cliques(url_public)
    #print("get_cliques = ", get_cliques_value)

    #get_addresses_value = get_addresses(url_public, node_1_addr, node_2_addr)
    #print("get_addresses_value = ", get_addresses_value)

    #node_peers_whitelist_value = node_peers_whitelist(url_private)
    #print("node_peers_whitelist_value = ", node_peers_whitelist_value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main()


# make unit test (std-lib python):
#
#   1. get status sur les nodes
#         - node1 ban pas le 2 et inversement
#         - verif les peers (s'ils sont bien connectés entre eux)
#

#
#   2. transactions entre les noeud :
#       - transfert dargent du noeud 1 vers 2 et inversement
#

#
#   3. transaction invalide (se renseigner)
#       - transaction invalide du node 2 vers le 1 (+ verif que node1 a ban le 2)
#
