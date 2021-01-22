import re
from datetime import datetime

from tasks.view.terminal import print_message, ERROR_MSG

COMMAND_INDEX = 1
ALLOWED_COMMANDS = ["add", "update", "remove", "list", "finish"]



def generate_hash(obj):
    return hash(obj) % (10 ** 8)


def validate_listing_arguments(args):
    OPTIONAL_ARGS = ["--all", "--today", "--week", "--missed", "--done"]
    MAX_OPT_ARGS_AMOUNT = 1
    MAX_ARGS_ARR_LENGTH = 3
    ARG_INDEX = 2

    try:
        optional_args = re.findall(r"\[([^]]+)\]", " ".join(args))
        if optional_args[0] not in OPTIONAL_ARGS:
            print_message("Wrong arguments for listing")
            return False
    except IndexError:
        print_message("Wrong arguments for listing")
        return False

    if len(optional_args) > MAX_OPT_ARGS_AMOUNT or len(args) > MAX_ARGS_ARR_LENGTH:
        print_message("Too many arguments provided")
        return False

    return optional_args[0]


def unpack_args(args):
    try:
        args_dict = dict(arg.split(" ", 1) for arg in args)
        return args_dict
    except ValueError:
        return False



