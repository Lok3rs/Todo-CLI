import re
from datetime import datetime

from view.terminal import print_message, ERROR_MSG

COMMAND_INDEX = 1
ALLOWED_COMMANDS = ["add", "update", "remove", "list", "finish"]


def validate_task_arguments(args):
    OPTIONAL_ARGS_KEYS = ["--deadline", "--description"]
    CMD_INDEX = 2
    NAME_INDEX = 3
    MIN_ARGS_ARR_LENGTH = 4
    MAX_ARGS_ARR_LENGTH = 8
    VALID_NAME_COMMAND = "--name"

    optional_args = re.findall(r"\[([^]]+)\]", " ".join(args))
    if args[CMD_INDEX] != VALID_NAME_COMMAND:
        print_message(ERROR_MSG.get(1))
        return False
    elif len(args) % 2 != 0 or len(args) < MIN_ARGS_ARR_LENGTH:
        print_message((ERROR_MSG.get(2)))
        return False
    elif re.match(r"\[([^]]+)\]", args[NAME_INDEX]):
        print_message(ERROR_MSG.get(3))
        return False
    elif len(optional_args) > len(OPTIONAL_ARGS_KEYS) or len(args) > MAX_ARGS_ARR_LENGTH:
        print_message(ERROR_MSG.get(4))
        return False

    try:
        provided_args = dict(arg.split(" ", 1) for arg in optional_args)
    except ValueError:
        print_message(ERROR_MSG.get(5))
        return False

    if not all(arg in OPTIONAL_ARGS_KEYS for arg in provided_args.keys()):
        print_message(ERROR_MSG.get(6))
        return False

    deadline = provided_args.get("--deadline")
    if deadline:
        try:
            deadline = datetime(*[int(el) for el in re.split("[-:.]", deadline)]).date()
        except (ValueError, TypeError):
            print_message((ERROR_MSG.get(7)))
            return False

        if deadline < datetime.today().date():
            print_message(ERROR_MSG.get(8))
            return False
        elif deadline == datetime.today().date():
            print_message("YOU HAVE TO DO THAT TODAY!")

    description = provided_args.get("--description")

    return {"name": args[NAME_INDEX], "deadline": deadline, "description": description}


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

