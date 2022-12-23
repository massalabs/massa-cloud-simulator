import os
import sys

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


    def print_args(self):
        print("self.config_file =", self.config_file)
        print("self.ip =", self.ip)
        print("self.address =", self.address)


    def check_file(self):
        if os.path.isfile(self.config_file) == False:
            raise FileNotFoundError
        if not os.access(self.config_file, os.R_OK):
            print("ERROR: Cannot read the file %s", self.config_file, file=sys.stderr)
            raise OSError
        files_size = os.path.getsize(self.config_file)
        if files_size <= 0:
            raise FileNotFoundError


    def fill_bs_list(self):
        for i in range(2, self.len_args):
            self.list_bs_node.append(self.args[i])
        return self.list_bs_node


    def get_file_content(self):
        try:
            with open(self.config_file, "rb") as f:#rb for reading and binary
                self.toml_dict = tomli.load(f)#load file as dict
        except tomli.TOMLDecodeError:
            print("ERROR: Invalid TOML file %s", self.config_file, file=sys.stderr)
            sys.exit(-1)


    def change_bs_sections(self):#update the section with right info
        change_bs_sections = self.toml_dict["bootstrap"]["bootstrap_list"]#get the section "bootstrap_list" into section "bootstrap"
        change_bs_sections.clear()#clear the section
        change_bs_sections.append(self.fill_bs_list())#fill the section
        #toml_dict_json = json.dumps(self.toml_dict, indent=4)#json format
        #print(self.toml_dict)
        #print(toml_dict_json)


    def gen_config_file(self):#generate a new config file
        try:
            #Rename the old config file
            if os.path.exists(self.config_file):
                os.rename(self.config_file, self.config_file + ".old")
                new_config_file = self.config_file
                self.config_file = self.config_file + ".old"
            else:
                raise OSError
            #Write new content in a new file
            with open(new_config_file, "wb") as f:
                tomli_w.dump(self.toml_dict, f)
        except tomli.TOMLDecodeError:
            print("ERROR: Cannot generate a new file", file=sys.stderr)
            sys.exit(-1)


def usage(status):
    print("USAGE :\n"
        "\tpython config.py [file] [ip] [adress]\n"
        "\nDESCRIPTION :\n"
        "\tfile\t\tconfiguration file\n"
        "\tip\t\tip of the node for the bootstrap\n"
        "\taddress\t\twallet address"
    )
    if status == True:
        sys.exit(0)
    elif status == False:
        sys.exit(-1)


def main(argv):
    try:
        cfg = Config(argv)
        if len(argv) == 2 and argv[1] == "--help":
            usage(True)
        elif len(argv) != 4:
            raise TypeError
        cfg.check_file()
        #cfg.print_args()
        cfg.get_file_content()
        cfg.change_bs_sections()
        cfg.gen_config_file()
    except FileNotFoundError:
        print("ERROR : File '" + str(argv[1]) + "' not found or is empty", file=sys.stderr)
        sys.exit(-1)
    except IOError:
        print("ERROR: IO Error", file=sys.stderr)
        sys.exit(-1)
    except OSError:
        print("ERROR: OS Error", file=sys.stderr)
        sys.exit(-1)
    except TypeError:
        print("ERROR: Invalid number of arguments. See the usage bellow.\n", file=sys.stderr)
        usage(False)


if __name__ == "__main__":
    main(sys.argv)
