import sys

from tasks.model.data_manager import (finish_task, validate_and_update_task, validate_and_add_task,
                                      validate_and_get_list, validate_and_remove_task, undo_task)
from tasks.model.util import COMMAND_INDEX, ALLOWED_COMMANDS
from tasks.model.validators import validate_help
from tasks.view.terminal import print_message


controller_options = {
    "add": validate_and_add_task,
    "list": validate_and_get_list,
    "finish": finish_task,
    "update": validate_and_update_task,
    "remove": validate_and_remove_task,
    "help": validate_help,
    "undo": undo_task
}


def main_controller():
    sys_args = sys.argv
    cmd = sys_args[COMMAND_INDEX]
    if cmd not in ALLOWED_COMMANDS:
        print_message(success=False, result=0)
        return
    try:
        func = controller_options.get(cmd)
        success, result = func(sys_args)
        print_message(success, result,
                      print_help=func == validate_help,
                      listing=func == validate_and_get_list)
    except TypeError:
        print_message(success=False, result=0)
