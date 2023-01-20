import json
import argparse
import unittest

import requests


def get_env_data(env_path: str) -> dict:
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


class JsonApi():
    #def __init__(self) -> None:
    #    self.headers, self.payload = self.get_status()

    def get_status(self):
        headers = {'Content-type': 'application/json'}
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "get_status",
            "id": 0,
            "params": []
        })
        return headers, payload


class Api(JsonApi):
    def __init__(self) -> None:
        self.headers, self.payload = getattr(JsonApi, 'get_status')('self')

    def make_request(self, url_public: str):
        response = requests.post(url_public, data=self.payload, headers=self.headers)
        return response.json()


class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.env_dict = get_env_data(".env")
        self.api_data = Api()

    def test_status_nodes(self):
        req_node_1_public = getattr(self.api_data, 'make_request')(self.env_dict["URL_PUBLIC_NODE_1"])
        req_node_2_public = getattr(self.api_data, 'make_request')(self.env_dict["URL_PUBLIC_NODE_2"])
        
        # Test node_1_ban_count
        self.assertEqual(req_node_1_public["result"]["network_stats"]["banned_peer_count"], 0)
        # Test node_2_ban_count
        self.assertEqual(req_node_2_public["result"]["network_stats"]["banned_peer_count"], 0)
        # Test node_1_ip
        self.assertEqual(req_node_1_public["result"]["node_ip"], self.env_dict["NODE_1_IP"])
        # Test node_2_ip
        self.assertEqual(req_node_2_public["result"]["node_ip"], self.env_dict["NODE_2_IP"])
        # Test node_1_peers_by_id
        self.assertIn(req_node_2_public["result"]["node_id"], req_node_1_public["result"]["connected_nodes"])
        # Test node_2_peers_by_id
        self.assertIn(req_node_1_public["result"]["node_id"], req_node_2_public["result"]["connected_nodes"])
        # Test node_1_peers_by_ip
        self.assertIn(self.env_dict["NODE_2_IP"], str(req_node_1_public["result"]["connected_nodes"]))
        # Test node_2_peers_by_ip
        self.assertIn(self.env_dict["NODE_1_IP"], str(req_node_2_public["result"]["connected_nodes"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    unittest.main()
