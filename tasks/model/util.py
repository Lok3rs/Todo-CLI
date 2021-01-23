import re
from datetime import datetime

from tasks.view.terminal import print_message, ERROR_MSG

COMMAND_INDEX = 1
ALLOWED_COMMANDS = ["add", "update", "remove", "list", "finish"]


def generate_hash(obj):
    return hash(obj) % (10 ** 8)





def unpack_args(args):
    try:
        args_dict = dict(arg.split(" ", 1) for arg in args)
        return args_dict
    except ValueError:
        return False



