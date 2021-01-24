import os
from typing import Union, List, Dict

table_for_not_found_data = ["#", "NO", "DATA", "FOUND", "#"]


def generate_hash(obj: Union[str, int]) -> int:
    """
    :param obj: string or integer to be hashed
    :return: randomly hashed value for provided object
    """
    return hash(obj) % (10 ** 8)


def unpack_args(args: List) -> Union[Dict, bool]:
    """
    Divides the list values by the first occurrence of a space and creates the dictionary key and value from the
    divided values

    :param args: list of arguments provided in command line
    :return: dictionary made of provided values or False if division failed
    """
    try:
        args_dict = dict(arg.split(" ", 1) for arg in args)
        return args_dict
    except ValueError:
        return False


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def wait():
    input("Type ENTER to continue...")