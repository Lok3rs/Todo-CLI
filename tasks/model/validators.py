import re
from datetime import datetime
from typing import List, Union, Dict, Tuple

from tasks.model.util import unpack_args

COMMAND_INDEX = 1
ALLOWED_COMMANDS = ["add", "update", "remove", "list", "finish", "help", "undo", "find", "lazy"]


class Validator:

    def validate_add_task_arguments(self, sys_args: List) -> Union[int, Dict]:
        """
        The function validating the correctness of the entered data to create a new task

        :param sys_args: list of arguments provided in command line
        :return: Dictionary with validate arguments or index of error message if validation failed.
        """
        ARGS_KEYS_ADD = ["--name", "--deadline", "--description"]
        MIN_ARGS_ARR_LENGTH = 4
        MAX_ARGS_ARR_LENGTH = 8
        ARGS_INDEX_FROM = 2
        span = 2

        try:
            # Try to join optional command with it's value to be in same element of list
            args_tmp = sys_args[ARGS_INDEX_FROM:]
            args = [" ".join(args_tmp[i:i + span]) for i in range(len(args_tmp), span)]
        except IndexError:
            return 1

        # Checks if there is required argument in sys_args, then if args are divisible by 2 (every argument needs
        # to have exactly 1 value, then if enough arguments was provided.
        if ARGS_KEYS_ADD[0] not in sys_args or \
                len(sys_args) % 2 != 0 or \
                len(sys_args) < MIN_ARGS_ARR_LENGTH:
            return 1
        # Checks if too many arguments have been entered
        elif len(args) > len(ARGS_KEYS_ADD) or len(sys_args) > MAX_ARGS_ARR_LENGTH:
            return 2

        provided_args = unpack_args(args)

        # Checks if unpacking arguments was successful and then if all provided arguments are allowed
        if provided_args and \
                not all(arg in ARGS_KEYS_ADD for arg in provided_args.keys()):
            return 3

        deadline = provided_args.get("--deadline")

        # Checks if a deadline has been entered to see if it is correct
        if deadline and \
                not self.validate_deadline(deadline):
            return 4

        deadline = self.validate_deadline(deadline)

        description = provided_args.get("--description")
        name = provided_args.get("--name")

        return {"name": name, "deadline": deadline, "description": description}

    def validate_update_args(self, sys_args: List[str]) -> Union[int, Dict]:
        """
        The function validating the correctness of the entered data to update existing task.

        :param sys_args: list of arguments provided in command line
        :return: Dictionary with validate arguments or index of error message if validation failed.
        """
        MAX_UPDATE_ARR_LENGTH = 9
        OPTIONAL_ARGS_KEYS_UPDATE = ["--name", "--deadline", "--description"]
        OPT_ARGS_INDEX_FROM = 2
        HASH_INDEX = -1
        span = 2

        try:
            # Try to join optional command with it's value to be in same element of list
            opt_args_tmp = sys_args[OPT_ARGS_INDEX_FROM:HASH_INDEX]
            optional_args = [" ".join(opt_args_tmp[i:i + span]) for i in range(len(opt_args_tmp), span)]
        except IndexError:
            return 1

        # Checks if too many arguments have been entered
        if len(sys_args) > MAX_UPDATE_ARR_LENGTH \
                or len(sys_args) - len(optional_args) * 2 != 3:
            return 1

        provided_args = unpack_args(optional_args)

        # Checks if not enough arguments have been entered or if provided ones are not allowed
        if not provided_args \
                or not all(arg in OPTIONAL_ARGS_KEYS_UPDATE for arg in provided_args.keys()):
            return 3

        deadline = provided_args.get("--deadline")

        # Checks if a deadline has been entered to see if it is correct.
        if deadline and not self.validate_deadline(deadline) and deadline != "remove":
            return 4

        deadline = self.validate_deadline(deadline) if deadline != "remove" else "remove"
        description = provided_args.get("--description")
        name = provided_args.get("--name")

        return {"name": name, "deadline": deadline, "description": description}

    @staticmethod
    def validate_deadline(date: str) -> Union[datetime.date, bool]:
        """
        Function checks if the date entered by the user is in the correct format

        :param date: string with date to be checked
        :return: date in datetime or False if checking failed
        """
        if date:
            try:
                date = datetime(*[int(el) for el in re.split("[-:.]", date)]).date()
            except (ValueError, TypeError):
                return False
            if date < datetime.today().date():
                return False
            return date

    @staticmethod
    def validate_listing_arguments(sys_args: List[str]) -> Union[str, int]:
        """
        Function that checks if optional arguments for a list function have been entered correctly

        :param sys_args: list of arguments provided in command line
        :return: optional argument (--all by default, if not provided) or error message index if validation failed.
        """
        OPTIONAL_ARGS = ["--all", "--today", "--week", "--missed", "--done"]
        MAX_OPT_ARGS_AMOUNT = 1
        MIN_ARGS_ARR_LENGTH = 2
        MAX_ARGS_ARR_LENGTH = 3
        OPT_ARGS_INDEX_FROM = 2
        ARG_INDEX = 0

        # If not optional argument provided returns default argument
        if len(sys_args) == MIN_ARGS_ARR_LENGTH:
            return OPTIONAL_ARGS[ARG_INDEX]

        # try to validate if user insert valid argument for listing and if he inputs only 1 arg
        try:
            provided_args = sys_args[OPT_ARGS_INDEX_FROM:]
            if provided_args[ARG_INDEX] not in OPTIONAL_ARGS:
                return 1
            elif len(provided_args) > MAX_OPT_ARGS_AMOUNT \
                    or len(sys_args) > MAX_ARGS_ARR_LENGTH:
                return 2
        except IndexError:
            return 1

        return provided_args[ARG_INDEX]

    @staticmethod
    def validate_help(sys_args: List[str]) -> Tuple[bool, int]:
        """
        Function that validates arguments provided for printing help messages.

        :param sys_args: list of arguments provided in command line
        :return: tuple with boolean value meaning success of validation and index of help or error message
        """
        OPTIONAL_ARGS = {"add": 1, "update": 2, "remove": 3, "finish": 4, "list": 5, "undo": 6, "find": 7}
        MAX_ARGS_ARR_LENGTH = 3
        MIN_ARGS_ARR_LENGTH = 2
        OPTIONAL_ARG_INDEX = 2

        if (len(sys_args) == MAX_ARGS_ARR_LENGTH and sys_args[OPTIONAL_ARG_INDEX] not in OPTIONAL_ARGS) \
                or len(sys_args) > MAX_ARGS_ARR_LENGTH:
            return False, 8

        if len(sys_args) == MIN_ARGS_ARR_LENGTH:
            return True, 0

        optional_arg = sys_args[OPTIONAL_ARG_INDEX]

        return True, OPTIONAL_ARGS.get(optional_arg)
