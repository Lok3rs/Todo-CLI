from typing import Union, List, Dict

COMMAND_INDEX = 1
ALLOWED_COMMANDS = ["add", "update", "remove", "list", "finish", "help", "undo"]


def generate_hash(obj: Union[str, int]) -> int:
    return hash(obj) % (10 ** 8)


def unpack_args(args: List) -> Union[Dict, bool]:
    try:
        args_dict = dict(arg.split(" ", 1) for arg in args)
        return args_dict
    except ValueError:
        return False
