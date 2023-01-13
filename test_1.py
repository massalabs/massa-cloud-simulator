import json
import argparse
import unittest

import requests

#class JsonApi:
#    def __init__(self) -> None:
#
#class Api:
#    def __init__(self) -> None:
#

# fonction generique pour Api

class Data:
    def __init__(self):
        # url nodes
        self.url_private_node_1 = "http://127.0.0.1:33034"
        self.url_public_node_1 = "http://127.0.0.1:33035"
        self.url_private_node_2 = "http://127.0.0.1:34034"
        self.url_public_node_2 = "http://127.0.0.1:34035"

        # get data content for nodes from get_status
        self.status_content_1 = self.get_status(self.url_public_node_1)
        self.status_content_2 = self.get_status(self.url_public_node_2)
        self.node_1_id = self.status_content_1["result"]["node_id"]#same as pubkey
        self.node_2_id = self.status_content_2["result"]["node_id"]#same as pubkey

        # env values
        self.env_dict = self.get_env_data(".env")
        self.node_1_ip = self.env_dict["NODE_1_IP"]
        self.node_1_secret_key = self.env_dict["NODE_1_SECRET_KEY"]
        self.node_1_public_key = self.env_dict["NODE_1_PUBLIC_KEY"]
        self.node_1_address = self.env_dict["NODE_1_ADDRESS"]
        self.node_2_ip = self.env_dict["NODE_2_IP"]
        self.node_2_secret_key = self.env_dict["NODE_2_SECRET_KEY"]
        self.node_2_public_key = self.env_dict["NODE_2_PUBLIC_KEY"]
        self.node_2_address = self.env_dict["NODE_2_ADDRESS"]
        self.genesis_timestamp = self.env_dict["GENESIS_TIMESTAMP"]
    

    def get_env_data(self, env_path: str) -> dict:
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
            if '"' in value:
                value = value.replace('"', '')
            env_dict[key] = value
        return env_dict

    def get_status(self, url_public: str):
        headers = {'Content-type': 'application/json'}
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "get_status",
            "id": 0,
            "params": []
        })
        response = requests.post(url_public, data=payload, headers=headers)
        return response.json()# -> requests
        #return headers, payload -> json
        # to make api independ

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.data = Data()
        #self.env = # read dict env
        #ip host (127.0.0.1)

    def test_status_nodes(self):
        # test_node_1_ban_count
        ban_count_1 = self.data.status_content_1["result"]["network_stats"]["banned_peer_count"]
        self.assertEqual(ban_count_1, 0)
        # test_node_2_ban_count
        ban_count_2 = self.data.status_content_2["result"]["network_stats"]["banned_peer_count"]
        self.assertEqual(ban_count_2, 0)
        # test_node_1_ip
        node_1_ip = self.data.status_content_1["result"]["node_ip"]
        self.assertEqual(node_1_ip, self.data.node_1_ip)
        # test_node_2_ip
        node_2_ip = self.data.status_content_2["result"]["node_ip"]
        self.assertEqual(node_2_ip, self.data.node_2_ip)
        # test_node_1_peers_by_id
        connected_node_1_id = list(self.data.status_content_1["result"]["connected_nodes"].keys())[0]
        self.assertEqual(self.data.node_2_id, connected_node_1_id)
        # test_node_2_peers_by_id
        connected_node_2_id = list(self.data.status_content_2["result"]["connected_nodes"].keys())[0]
        self.assertEqual(self.data.node_1_id, str(connected_node_2_id))
        # test_node_1_peers_by_ip
        connected_node_1_id = list(self.data.status_content_1["result"]["connected_nodes"].keys())[0]
        connected_node_1_ip = self.data.status_content_1["result"]["connected_nodes"].get(connected_node_1_id)[0]
        self.assertEqual(self.data.node_2_ip, connected_node_1_ip)
        # test_node_2_peers_by_ip
        connected_node_2_id = list(self.data.status_content_2["result"]["connected_nodes"].keys())[0]
        connected_node_2_ip = self.data.status_content_2["result"]["connected_nodes"].get(connected_node_2_id)[0]
        self.assertEqual(self.data.node_1_ip, connected_node_2_ip)
    # use assertIn


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    unittest.main()
