# Update config.toml file for Massa node(s) (used in Dockerfile)

import sys
import shutil
from pathlib import Path
import argparse

# Third Part Library
import tomli
import tomli_w


def multi_get(d, *args, **kwargs):
    print("args", args)
    print("kwargs", kwargs)

    current_dict = d
    for k in args:
        current_dict = current_dict[k]

    return current_dict


def dict_multi_set(d, value, *args):

    current_dict = d
    for k in args[:-1]:
        current_dict = current_dict[k]

    current_dict[args[-1]] = value


class Config:
    def __init__(self, config_file, ip, port, address, node_ip, bind_private_ip, bind_private_port, misc_update):
        self.config_file = Path(config_file)
        self.ip = ip
        self.port = port
        self.address = address
        self.node_ip = node_ip
        self.bind_private_ip = bind_private_ip
        self.bind_private_port = bind_private_port
        self.misc_update = misc_update
        self.toml_dict = {}

    def check_file(self):
        if self.config_file.exists() is False:
            raise FileNotFoundError

    def get_file_content(self):
        with open(self.config_file, "rb") as f:  # rb for reading and binary
            self.toml_dict = tomli.load(f)  # load file as dict

    def change_bs_sections(self):  # update the section with right info
        change_bs_sections = self.toml_dict["bootstrap"][
            "bootstrap_list"
        ]  # get the section "bootstrap_list" into section "bootstrap"
        change_bs_sections.append(
            [f"{self.ip}:{self.port}", self.address]
        )  # fill the section

    def change_bind_private_ip(self):
        self.toml_dict["api"]["bind_private"] = f"{self.bind_private_ip}:{self.bind_private_port}"

    def change_routable_ip(self):
        self.toml_dict["network"]["routable_ip"] = self.node_ip

    def clear_bs_sections(self):
        self.toml_dict["bootstrap"]["bootstrap_list"].clear()

    def empty_bs_whitelist(self):
        self.toml_dict["bootstrap"]["bootstrap_whitelist_path"] = ""

    def update_misc(self):
        misc_update = self.misc_update or []
        for item in misc_update:
            print("item:", item)
            keys_, value = item.split("=")
            keys = keys_.split(".")
            print(f"Updating keys: {keys}, value: {value}")
            dict_multi_set(self.toml_dict, value, *keys)

    def gen_config_file(self):  # generate a new config file
        shutil.copy(
            self.config_file, str(self.config_file) + ".old"
        )  # Rename the old config file
        with open(self.config_file, "wb") as f:  # Write new content in a new file
            tomli_w.dump(self.toml_dict, f)


def main(args):
    try:
        cfg = Config(args.config_file, args.ip, args.port, args.address, args.node_ip, args.bind_private_ip, args.bind_private_port, args.update)
        cfg.check_file()
        cfg.get_file_content()
        cfg.clear_bs_sections()
        if args.ip != "" and args.address != "":
            cfg.change_bs_sections()
        if args.empty_bootstrap_whitelist_path:
            cfg.empty_bs_whitelist()
        cfg.change_bind_private_ip()
        cfg.change_routable_ip()
        cfg.update_misc()
        cfg.gen_config_file()
    except FileNotFoundError:
        print("ERROR : File '" + str(args.config_file) + "' not found", file=sys.stderr)
        sys.exit(2)
    except IOError:
        print("ERROR: IO Error", file=sys.stderr)
        sys.exit(2)
    except tomli.TOMLDecodeError:
        print("ERROR: Cannot generate a new file or invalid TOML file", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        # Misc error
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help="configuration file in TOML format")
    parser.add_argument("-i", "--ip", help="ip of the node for the bootstrap", required=True)
    parser.add_argument("-a", "--address", help="wallet address for bootstrapping", required=True)
    parser.add_argument("-n", "--node_ip", help="ip of the node to establish connections between nodes", required=True)
    parser.add_argument("-p", "--port", help="port of the node for the bootstrap", default=31245, type=int,
                        required=False)
    parser.add_argument("-bi", "--bind_private_ip", help="private ip address to listen from", default="0.0.0.0",
                        type=str, required=False)
    parser.add_argument("-bp", "--bind_private_port", help="private port to listen from", default=33034, type=int,
                        required=False)
    parser.add_argument("-e", "--empty_bootstrap_whitelist_path", help="Boolean to make the whitelist empty or not",
                        action="store_true")
    parser.add_argument("--update", type=str, nargs="*",
                        help="example: --update logging.level=3 + can be specified multiple time")
    args = parser.parse_args()
    main(args)

