import sys
import datetime
import shutil
import argparse


class Info:
    env_file = ".env"
    len_content = 0
    file_content: list[str] = []


def get_current_timestamp(genesis_timestamp_delay):
    current_date = datetime.datetime.now()
    current_ts = current_date + datetime.timedelta(seconds=genesis_timestamp_delay)
    current_ts = round(current_ts.timestamp()) * 1000
    current_ts = '"' + str(current_ts) + '"'
    return current_ts


def get_content_file(info, genesis_timestamp_delay):
    with open(info.env_file, "r") as f:
        info.file_content = f.readlines()
        info.len_content = len(info.file_content)
        for i in range(len(info.file_content)):
            if "GENESIS_TIMESTAMP=" in info.file_content[i]:
                info.file_content[i] = "GENESIS_TIMESTAMP=" + get_current_timestamp(genesis_timestamp_delay)
        f.close()


def gen_new_env(info):
    with open(info.env_file, "w") as n:
        for i in range(info.len_content):
            n.write(info.file_content[i])
        n.close()


def main(args):
    info = Info()
    try:
        get_content_file(info, args.genesis_timestamp_delay)
        shutil.copy(info.env_file, info.env_file + ".old")
        gen_new_env(info)
    except IOError:
        print("ERROR: Cannot open .env file", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--genesis_timestamp_delay", help="Time to wait before starting network", default=45, type=int, required=False)
    args = parser.parse_args()
    main(args)
