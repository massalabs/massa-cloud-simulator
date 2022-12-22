from config import *
import os
import sys

class File():
    def __init__(self, config):
        self.cfg = config

    def check_file(self):
        if os.path.isfile(self.cfg.config_file) == False:
            raise FileNotFoundError
        if not os.access(self.cfg.config_file, os.R_OK):
            print("ERROR: Cannot read the file %s", self.cfg.config_file, file=sys.stderr)
            raise OSError
        file = open(self.cfg.config_file)
        files_size = os.path.getsize(self.cfg.config_file)
        if files_size <= 0:
            raise FileNotFoundError
