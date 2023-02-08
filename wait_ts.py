import time
import subprocess
import sys

if __name__ == "__main__":

    # TODO: get Genesis ts and wait for it...
    delay = 60
    print(f"Sleeping for {delay} seconds...")
    time.sleep(delay)

    # Debug
    # print(sys.argv)
    # print(sys.argv[1:])

    to_launch = sys.argv[1:]
    print(f"Launching: {to_launch}")
    return_code = subprocess.call(to_launch)
    # Debug
    # print(f"p return code: {return_code}")
