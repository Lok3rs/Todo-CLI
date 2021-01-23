import re
from datetime import datetime
from typing import List, Union, Dict, Tuple

from tasks.model.util import unpack_args


def validate_add_task_arguments(sys_args: List) -> Union[int, Dict]:
    ARGS_KEYS_ADD = ["--name", "--deadline", "--description"]
    MIN_ARGS_ARR_LENGTH = 4
    MAX_ARGS_ARR_LENGTH = 8
    ARGS_INDEX_FROM = 2
    span = 2

    try:
        args_tmp = sys_args[ARGS_INDEX_FROM:]
        args = [" ".join(args_tmp[i:i + span]) for i in range(0, len(args_tmp), span)]
    except IndexError:
        return 1

    if ARGS_KEYS_ADD[0] not in sys_args or \
            len(sys_args) % 2 != 0 or \
            len(sys_args) < MIN_ARGS_ARR_LENGTH:
        return 1
    elif len(args) > len(ARGS_KEYS_ADD) or len(sys_args) > MAX_ARGS_ARR_LENGTH:
        return 2

    provided_args = unpack_args(args)

    if provided_args and \
            not all(arg in ARGS_KEYS_ADD for arg in provided_args.keys()):
        return 3

    deadline = provided_args.get("--deadline")
    if deadline and \
            not validate_deadline(deadline):
        return 4

    deadline = validate_deadline(deadline)

    description = provided_args.get("--description")
    name = provided_args.get("--name")

    return {"name": name, "deadline": deadline, "description": description}


def validate_update_args(sys_args: List[str]) -> Union[int, Dict]:
    MAX_UPDATE_ARR_LENGTH = 9
    OPTIONAL_ARGS_KEYS_UPDATE = ["--name", "--deadline", "--description"]
    OPT_ARGS_INDEX_FROM = 2
    HASH_INDEX = -1
    span = 2

    try:
        opt_args_tmp = sys_args[OPT_ARGS_INDEX_FROM:HASH_INDEX]
        optional_args = [" ".join(opt_args_tmp[i:i + span]) for i in range(0, len(opt_args_tmp), span)]
    except IndexError:
        return 1

    if len(sys_args) > MAX_UPDATE_ARR_LENGTH \
            or len(sys_args) - len(optional_args) * 2 != 3:
        return 1

    provided_args = unpack_args(optional_args)

    if not provided_args \
            or not all(arg in OPTIONAL_ARGS_KEYS_UPDATE for arg in provided_args.keys()):
        return 3

    deadline = provided_args.get("--deadline")
    if deadline and not validate_deadline(deadline):
        return 4

    deadline = validate_deadline(deadline)

    description = provided_args.get("--description")
    name = provided_args.get("--name")

    return {"name": name, "deadline": deadline, "description": description}


def validate_deadline(date: str) -> Union[datetime.date, bool]:
    if date:
        try:
            date = datetime(*[int(el) for el in re.split("[-:.]", date)]).date()
        except (ValueError, TypeError):
            return False
        if date < datetime.today().date():
            return False
        return date


def validate_listing_arguments(sys_args: List[str]) -> Union[str, int]:
    OPTIONAL_ARGS = ["--all", "--today", "--week", "--missed", "--done"]
    MAX_OPT_ARGS_AMOUNT = 1
    MIN_ARGS_ARR_LENGTH = 2
    MAX_ARGS_ARR_LENGTH = 3
    OPT_ARGS_INDEX_FROM = 2
    span = 2

    if len(sys_args) == MIN_ARGS_ARR_LENGTH:
        return OPTIONAL_ARGS[0]

    try:
        opt_args_tmp = sys_args[OPT_ARGS_INDEX_FROM:]
        provided_args = [" ".join(opt_args_tmp[i:i + span]) for i in range(0, len(opt_args_tmp), span)]
        if provided_args[0] not in OPTIONAL_ARGS:
            return 1
    except IndexError:
        return 1

    if len(provided_args) > MAX_OPT_ARGS_AMOUNT \
            or len(sys_args) > MAX_ARGS_ARR_LENGTH:
        return 2

    return provided_args[0]


def validate_help(sys_args: List[str]) -> Tuple[bool, int]:
    OPTIONAL_ARGS = {"add": 1, "update": 2, "remove": 3, "finish": 4, "list": 5}
    MAX_ARGS_ARR_LENGTH = 3
    MIN_ARGS_ARR_LENGTH = 2
    OPTIONAL_ARG_INDEX = 2

    if (len(sys_args) == MAX_ARGS_ARR_LENGTH and sys_args[OPTIONAL_ARG_INDEX] not in OPTIONAL_ARGS) \
            or len(sys_args) > MAX_ARGS_ARR_LENGTH:
        return False, 1

    if len(sys_args) == MIN_ARGS_ARR_LENGTH:
        return True, 0

    optional_arg = sys_args[OPTIONAL_ARG_INDEX]

    return True, OPTIONAL_ARGS.get(optional_arg)
