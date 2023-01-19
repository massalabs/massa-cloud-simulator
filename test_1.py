import json
import argparse
import unittest

import requests


class JsonApi():
    def get_status(self, url_public: str):
        headers = {'Content-type': 'application/json'}
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "get_status",
            "id": 0,
            "params": []
        })
        response = requests.post(url_public, data=payload, headers=headers)
        return response.json()


class Api(JsonApi):
    def __init__(self) -> None:
        #JsonApi.__init__(self)
        self.env_dict = self.get_env_data(".env")
        self.status_content_1 = self.get_status(self.env_dict["URL_PUBLIC_NODE_1"])
        self.status_content_2 = self.get_status(self.env_dict["URL_PUBLIC_NODE_2"])

    def get_env_data(self, env_path: str) -> dict:
        env_dict = {}
        with open(env_path) as f:
            lines = f.read().splitlines()
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


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.api_data = Api()

    def test_status_nodes(self):
        # test_node_1_ban_count
        ban_count_1 = self.api_data.status_content_1["result"]["network_stats"]["banned_peer_count"]
        self.assertEqual(ban_count_1, 0)
        # test_node_2_ban_count
        ban_count_2 = self.api_data.status_content_2["result"]["network_stats"]["banned_peer_count"]
        self.assertEqual(ban_count_2, 0)
        # test_node_1_ip
        node_1_ip = self.api_data.status_content_1["result"]["node_ip"]
        self.assertEqual(node_1_ip, self.api_data.env_dict["NODE_1_IP"])
        # test_node_2_ip
        node_2_ip = self.api_data.status_content_2["result"]["node_ip"]
        self.assertEqual(node_2_ip, self.api_data.env_dict["NODE_2_IP"])

        # test_node_1_peers_by_id
        connected_node_1_id = list(self.api_data.status_content_1["result"]["connected_nodes"].keys())[0]
        self.assertEqual(self.api_data.status_content_2["result"]["node_id"], connected_node_1_id)
        # test_node_2_peers_by_id
        connected_node_2_id = list(self.api_data.status_content_2["result"]["connected_nodes"].keys())[0]
        self.assertEqual(self.api_data.status_content_1["result"]["node_id"], str(connected_node_2_id))
        # test_node_1_peers_by_ip
        connected_node_1_id = list(self.api_data.status_content_1["result"]["connected_nodes"].keys())[0]
        connected_node_1_ip = self.api_data.status_content_1["result"]["connected_nodes"].get(connected_node_1_id)[0]
        self.assertEqual(self.api_data.env_dict["NODE_2_IP"], connected_node_1_ip)
        # test_node_2_peers_by_ip
        connected_node_2_id = list(self.api_data.status_content_2["result"]["connected_nodes"].keys())[0]
        connected_node_2_ip = self.api_data.status_content_2["result"]["connected_nodes"].get(connected_node_2_id)[0]
        self.assertEqual(self.api_data.env_dict["NODE_1_IP"], connected_node_2_ip)
        # use assertIn


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    unittest.main()
