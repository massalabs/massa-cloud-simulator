from manage_file import *

class Config:
    def __init__(self):
        self.config_file=""
        self.ip=""
        self.address=""

    def set_args(self, argv):
        self.config_file = argv[1]
        self.ip = argv[2]
        self.address = argv[3]
