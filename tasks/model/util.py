import os
from typing import Union, List, Dict


def generate_hash(obj: Union[str, int]) -> int:
    return hash(obj) % (10 ** 8)


def unpack_args(args: List) -> Union[Dict, bool]:
    try:
        args_dict = dict(arg.split(" ", 1) for arg in args)
        return args_dict
    except ValueError:
        return False


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def wait():
    input("Type ENTER to continue...")