# Read .env file keys & address and update the following files
# config/initial_ledger.json
# config/initial_rolls.json
# config/node_1_privkey.key
# config/node_1_privkey.key
# Warning: This script is for dev only (developing on massa-cloud-simulator)

import argparse
import json
from pathlib import Path

# third party lib
from dotenv import dotenv_values


def main(args):

    indent_spaces_count = 4

    # read .env
    env = dotenv_values(args.env_file)
    # Update initial ledger

    ledger_filepath = args.ledger_filepath
    with open(ledger_filepath) as fp:
        content = json.load(fp)

    content_has_changed = False
    content_new = {}
    for i, (key, value) in enumerate(content.items()):
        new_key = env[f"NODE_{i+1}_ADDRESS"]
        if new_key != key:
            content_has_changed = True
        content_new[new_key] = value

    if content_has_changed:
        with open(ledger_filepath, "w+") as fp:
            json.dump(content_new, fp, indent=indent_spaces_count)

        print(f"Updated {ledger_filepath}")
    else:
        print(f"Nothing to change in {ledger_filepath}")

    # Update initial_rolls.json

    rolls_filepath = args.rolls_filepath
    with open(rolls_filepath) as fp:
        content = json.load(fp)

    content_has_changed = False
    content_new = {}
    for i, (key, value) in enumerate(content.items()):
        new_key = env[f"NODE_{i+1}_ADDRESS"]
        if new_key != key:
            content_has_changed = True
        content_new[new_key] = value

    if content_has_changed:
        with open(rolls_filepath, "w+") as fp:
            json.dump(content_new, fp, indent=indent_spaces_count)

        print(f"Updated {rolls_filepath}")
    else:
        print(f"Nothing to change in {rolls_filepath}")

    # Update node_X_privkey.key

    done = False
    i = 0
    while not done:
        p = Path(f"config/node_{i+1}_privkey.key")
        if p.is_file():
            with open(p) as fp:
                content = json.load(fp)

            node_secret_key_new = env[f"NODE_{i+1}_SECRET_KEY"]
            node_public_key_new = env[f"NODE_{i+1}_PUBLIC_KEY"]

            if node_secret_key_new != content["secret_key"] or node_public_key_new != content["public_key"]:
                content["secret_key"] = node_secret_key_new
                content["public_key"] = node_public_key_new

                with open(p, "w+") as fp:
                    json.dump(content, fp, indent=indent_spaces_count)

                print(f"Updated {p}")
            else:
                print(f"Nothing to change in {p}")

            i += 1

        else:
            done = True

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--env_file", help="Env file to get the good values", default=".env",
                    type=str, required=False)
    parser.add_argument("-l", "--ledger_filepath", help="Filepath to the initial_ledger file", default="base_config/initial_ledger.json",
                    type=str, required=False)
    parser.add_argument("-r", "--rolls_filepath", help="Filepath to the initial_rolls file", default="base_config/initial_rolls.json",
                    type=str, required=False)
    args = parser.parse_args()
    main(args)
