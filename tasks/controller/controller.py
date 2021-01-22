import sys

from tasks.model.data_manager import (add_task, get_column_names, get_task_values,
                                      find_task_by_hash, finish_task, validate_and_update_task)
from tasks.model.util import COMMAND_INDEX, ALLOWED_COMMANDS, validate_add_task_arguments, validate_listing_arguments
from tasks.view.terminal import print_table, print_message


def main():
    args = sys.argv
    if args[COMMAND_INDEX] not in ALLOWED_COMMANDS:
        print("Wrong command provided. Type --help to see possible options")

    elif args[COMMAND_INDEX] == "add":
        task = validate_add_task_arguments(args)
        if task:
            add_task(name=task.get("name"),
                     deadline=task.get("deadline"),
                     description=task.get("description"))

    elif args[COMMAND_INDEX] == "list":
        listing_option = validate_listing_arguments(args)
        if listing_option:
            print_table([get_column_names(), *get_task_values(listing_option)])

    elif args[COMMAND_INDEX] == "finish":
        task = find_task_by_hash(args, hash_index=2)
        if task:
            finish_task(task)

    elif args[COMMAND_INDEX] == "update":
        if validate_and_update_task(args):
            print_message("Updating successfull")
        else:
            print_message("Something went wrong")
