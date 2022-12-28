import sys
import shutil
from pathlib import Path

# Third Part Library
import tomli
import tomli_w

class Config():
    def __init__(self, argv):
        self.len_args = len(argv)
        self.args = argv
        self.config_file = self.args[1]
        self.ip = self.args[2]
        self.address = self.args[3]
        self.toml_dict = {}
        self.bs_list_section_dict = {}
        self.list_bs_node = []


    def check_file(self):
        #home_path = Path.home() # Cannot do that -> venv get "/root" instead of "/home/user"
        #configfile_path = Path(home_path, "massa_exec_files", "massa-node", "base_config", "config.toml") # same as above
        configfile_path = Path("/", "home", "user", "massa_exec_files", "massa-node", "base_config", "config.toml")
        if configfile_path.exists() == False:
            print("ERROR : File '" + str(configfile_path) + "' not found", file=sys.stderr)
            sys.exit(-1)


    def fill_bs_list(self):
        for i in range(2, self.len_args):
            if self.args[i]:
                self.list_bs_node.append(self.args[i])
        return self.list_bs_node


    def get_file_content(self):
        with open(self.config_file, "rb") as f:#rb for reading and binary
            self.toml_dict = tomli.load(f)#load file as dict


    def change_bs_sections(self):#update the section with right info
        change_bs_sections = self.toml_dict["bootstrap"]["bootstrap_list"]#get the section "bootstrap_list" into section "bootstrap"
        change_bs_sections.clear()#clear the section
        change_bs_sections.append(self.fill_bs_list())#fill the section
        #toml_dict_json = json.dumps(self.toml_dict, indent=4)#json format
        #print(self.toml_dict)
        #print(toml_dict_json)


    def gen_config_file(self):#generate a new config file
        #Rename the old config file
        shutil.copy(self.config_file, self.config_file + ".old")
        new_config_file = self.config_file
        self.config_file = self.config_file + ".old"
        #Write new content in a new file
        with open(new_config_file, "wb") as f:
            tomli_w.dump(self.toml_dict, f)



def usage(status):
    print("USAGE :\n"
        "\tpython config.py [file] [ip] [adress]\n"
        "\nDESCRIPTION :\n"
        "\tfile\t\tconfiguration file\n"
        "\tip\t\tip of the node for the bootstrap\n"
        "\taddress\t\twallet address"
    )


def main(argv):
    try:
        if len(argv) == 2 and argv[1] == "--help":
            usage()
            sys.exit(0)
        elif len(argv) != 4:
            usage()
            sys.exit(-1)
        cfg = Config(argv)
        cfg.check_file()
        cfg.get_file_content()
        cfg.change_bs_sections()
        cfg.gen_config_file()
    except FileNotFoundError:
        print("ERROR : File '" + str(argv[1]) + "' not found", file=sys.stderr)
        sys.exit(-1)
    except IOError:
        print("ERROR: IO Error", file=sys.stderr)
        sys.exit(-1)
    except TypeError:
        print("ERROR: Invalid number of arguments. See the usage bellow.\n", file=sys.stderr)
        usage()
        sys.exit(-1)
    except tomli.TOMLDecodeError:
        print("ERROR: Cannot generate a new file or invalid TOML file", file=sys.stderr)
        sys.exit(-1)


if __name__ == "__main__":
    main(sys.argv)
