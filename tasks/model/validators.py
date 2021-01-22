import re
from datetime import datetime

from tasks.model.util import unpack_args


def validate_add_task_arguments(args):
    OPTIONAL_ARGS_KEYS_ADD = ["--deadline", "--description"]
    CMD_INDEX = 2
    NAME_INDEX = 3
    MIN_ARGS_ARR_LENGTH = 4
    MAX_ARGS_ARR_LENGTH = 8
    VALID_NAME_COMMAND = "--name"

    optional_args = re.findall(r"\[([^]]+)\]", " ".join(args))

    if args[CMD_INDEX] != VALID_NAME_COMMAND or \
            len(args) % 2 != 0 or \
            len(args) < MIN_ARGS_ARR_LENGTH or \
            re.match(r"\[([^]]+)\]", args[NAME_INDEX]):
        return 1
    elif len(optional_args) > len(OPTIONAL_ARGS_KEYS_ADD) or len(args) > MAX_ARGS_ARR_LENGTH:
        return 2

    provided_args = unpack_args(optional_args)

    if not provided_args or not all(arg in OPTIONAL_ARGS_KEYS_ADD for arg in provided_args.keys()):
        return 3

    deadline = provided_args.get("--deadline")
    if deadline and not validate_deadline(deadline):
        return 4

    deadline = validate_deadline(deadline)

    description = provided_args.get("--description")

    return {"name": args[NAME_INDEX], "deadline": deadline, "description": description}


def validate_update_args(args):
    MAX_UPDATE_ARR_LENGTH = 9
    OPTIONAL_ARGS_KEYS_UPDATE = ["--name", "--deadline", "--description"]
    optional_args = re.findall(r"\[([^]]+)\]", " ".join(args))

    if len(args) > MAX_UPDATE_ARR_LENGTH or len(args) - len(optional_args) * 2 != 3:
        return 1

    provided_args = unpack_args(optional_args)

    if not provided_args or not all(arg in OPTIONAL_ARGS_KEYS_UPDATE for arg in provided_args.keys()):
        return 3

    deadline = provided_args.get("--deadline")
    if deadline and not validate_deadline(deadline):
        return 4

    deadline = validate_deadline(deadline)

    description = provided_args.get("--description")
    name = provided_args.get("--name")

    return {"name": name, "deadline": deadline, "description": description}


def validate_deadline(date):
    if date:
        try:
            date = datetime(*[int(el) for el in re.split("[-:.]", date)]).date()
        except (ValueError, TypeError):
            return False
        if date < datetime.today().date():
            return False
        return date
