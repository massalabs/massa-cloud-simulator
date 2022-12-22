from config import *
from manage_file import *

import sys


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
        cfg = Config()
        fle = File(cfg)

        if len(argv) == 2 and argv[1] == "--help":
            usage(True)
        elif len(argv) != 4:
            raise TypeError
        cfg.set_args(argv)
        fle.check_file()
        print("cfg.config_file =", cfg.config_file)
        print("cfg.ip =", cfg.ip)
        print("cfg.address =", cfg.address)
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
