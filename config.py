import sys
import shutil
from pathlib import Path
import argparse

# Third Part Library
import tomli
import tomli_w


class Config:
    def __init__(self, config_file, ip, port, address):
        self.config_file = Path(args.config_file)
        self.ip = args.ip
        self.port = args.port
        self.address = args.address
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
        self.toml_dict["api"]["bind_private"]= "0.0.0.0:33034"

    def clear_bs_sections(self):
        self.toml_dict["bootstrap"]["bootstrap_list"].clear()

    def empty_bs_whitelist(self):
        self.toml_dict["bootstrap"]["bootstrap_whitelist_path"] = ""

    def gen_config_file(self):  # generate a new config file
        shutil.copy(
            self.config_file, str(self.config_file) + ".old"
        )  # Rename the old config file
        with open(self.config_file, "wb") as f:  # Write new content in a new file
            tomli_w.dump(self.toml_dict, f)


def main(args):
    try:
        cfg = Config(args.config_file, args.ip, args.port, args.address)
        cfg.check_file()
        cfg.get_file_content()
        cfg.clear_bs_sections()
        if args.ip != "" and args.address != "":
            cfg.change_bs_sections()
        if args.empty_bootstrap_whitelist_path:
            cfg.empty_bs_whitelist()
        cfg.change_bind_private_ip()
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help="configuration file in TOML format")
    parser.add_argument("-i", "--ip", help="ip of the node for the bootstrap")
    parser.add_argument("-a", "--address", help="wallet address")
    parser.add_argument("-p", "--port", help="port of the node for the bootstrap", default=31245, type=int, required=False)
    parser.add_argument("-e", "--empty_bootstrap_whitelist_path", help="Boolean to make the whitelist empty or not", action="store_true")
    args = parser.parse_args()
    main(args)
