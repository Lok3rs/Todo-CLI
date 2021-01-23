import sys

from tasks.model.data_manager import finish_task,validate_and_update_task, validate_and_add_task, validate_and_get_list
from tasks.model.util import COMMAND_INDEX, ALLOWED_COMMANDS
from tasks.view.terminal import print_table, print_message, ERROR_MSG


def main():
    args = sys.argv
    cmd = args[COMMAND_INDEX]
    if cmd not in ALLOWED_COMMANDS:
        print_message(ERROR_MSG.get(0))

    elif cmd == "add":
        success, result = validate_and_add_task(args)
        print_message(result) if success else print_message(ERROR_MSG.get(result))

    elif cmd == "list":
        success, result = validate_and_get_list(args)
        print_table(result) if success else print_message(ERROR_MSG.get(result))

    elif cmd == "finish":
        success, result = finish_task(args)
        print_message(result) if success else print_message(ERROR_MSG.get(result))

    elif cmd == "update":
        success, result = validate_and_update_task(args)
        print_message(result) if success else print_message(ERROR_MSG.get(result))
