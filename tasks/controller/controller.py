import sys

from tasks.model.data_manager import (get_column_names, get_task_values,
                                      find_task_by_hash, finish_task, validate_and_update_task, validate_and_add_task)
from tasks.model.util import COMMAND_INDEX, ALLOWED_COMMANDS, validate_listing_arguments
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
        listing_option = validate_listing_arguments(args)
        if listing_option:
            print_table([get_column_names(), *get_task_values(listing_option)])

    elif cmd == "finish":
        success, result = finish_task(args)
        print_message(result) if success else print_message(ERROR_MSG.get(result))

    elif cmd == "update":
        if validate_and_update_task(args):
            print_message("Updating successful")
        else:
            print_message("Something went wrong")
