import json
import argparse
import unittest
from functools import partial

import requests
from dotenv import dotenv_values


class JsonApi():
    def get_status(self) -> tuple[dict[str, str], str]:
        headers = {'Content-type': 'application/json'}
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "get_status",
            "id": 0,
            "params": []
        })
        return headers, payload


class Api():
    def __init__(self, url_public) -> None:
        self.url_public = url_public
        self._api = JsonApi()

    def make_request(self, url_public: str, headers, payload):
        response = requests.post(url_public, headers=headers, data=payload)
        return response.json()

    def __getattr__(self, item):
        # Call function from json api
        f = getattr(self._api, item)
        headers, payload = f()
        return partial(self.make_request, self.url_public, headers, payload)


class TestStringMethods(unittest.TestCase):
    def setUp(self, env_filepath=".env") -> None:
        self.env_dict = dotenv_values(env_filepath)
        self.api_public_1 = Api(self.env_dict["URL_PUBLIC_NODE_1"])
        self.api_public_2 = Api(self.env_dict["URL_PUBLIC_NODE_2"])

    def test_status_nodes(self):
        content_get_status_1 = self.api_public_1.get_status()
        content_get_status_2 = self.api_public_2.get_status()

        # Test node_1_ban_count
        self.assertEqual(content_get_status_1["result"]["network_stats"]["banned_peer_count"], 0)
        # Test node_2_ban_count
        self.assertEqual(content_get_status_2["result"]["network_stats"]["banned_peer_count"], 0)
        # Test node_1_ip
        self.assertEqual(content_get_status_1["result"]["node_ip"], self.env_dict["NODE_1_IP"])
        # Test node_2_ip
        self.assertEqual(content_get_status_2["result"]["node_ip"], self.env_dict["NODE_2_IP"])
        # Test node_1_peers_by_id
        self.assertIn(content_get_status_2["result"]["node_id"], content_get_status_1["result"]["connected_nodes"])
        # Test node_2_peers_by_id
        self.assertIn(content_get_status_1["result"]["node_id"], content_get_status_2["result"]["connected_nodes"])
        # Test node_1_peers_by_ip
        self.assertIn(self.env_dict["NODE_2_IP"], str(content_get_status_1["result"]["connected_nodes"]))
        # Test node_2_peers_by_ip
        self.assertIn(self.env_dict["NODE_1_IP"], str(content_get_status_2["result"]["connected_nodes"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    unittest.main()
