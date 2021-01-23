import sys

from tasks.controller.lazy_controller import lazy_controller
from tasks.model.data_manager import (finish_task, validate_and_update_task, validate_and_add_task,
                                      validate_and_get_list, validate_and_remove_task, undo_task, find_task_for_table)
from tasks.model.validators import validate_help, COMMAND_INDEX, ALLOWED_COMMANDS
from tasks.view.terminal import print_message, show_info

controller_options = {
    "add": validate_and_add_task,
    "list": validate_and_get_list,
    "finish": finish_task,
    "update": validate_and_update_task,
    "remove": validate_and_remove_task,
    "help": validate_help,
    "undo": undo_task,
    "find": find_task_for_table
}


def main_controller():
    try:
        sys_args = sys.argv
        cmd = sys_args[COMMAND_INDEX]
        if cmd not in ALLOWED_COMMANDS:
            print_message(success=False, msg_index=0)
            return
        elif cmd == "lazy":
            lazy_controller()
            return
        try:
            func = controller_options.get(cmd)
            success, msg_index = func(sys_args)
            print_message(success, msg_index,
                          print_help=func == validate_help,
                          listing=(func == validate_and_get_list or func == find_task_for_table))
        except TypeError:
            print_message(success=False, msg_index=0)
    except KeyboardInterrupt:
        show_info("\nWell, you could finish it more elegant... :)")





