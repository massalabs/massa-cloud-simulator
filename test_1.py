import json
import unittest

import requests

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


class TestStringMethods(unittest.TestCase):
    def test_get_status(self):
        url_private_node_1 = "http://127.0.0.1:33034"
        url_public_node_1 = "http://127.0.0.1:33035"
        url_private_node_2 = "http://127.0.0.1:34034"
        url_public_node_2 = "http://127.0.0.1:34035"

        get_status_value = get_status(url_public_node_1)
        peers_ban = get_status_value["result"]["network_stats"]["banned_peer_count"]
        self.assertEqual(get_status_value, 0)


if __name__ == "__main__":
    unittest.main()
