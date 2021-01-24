import sys

import tasks.model.data_manager as dm
import tasks.view.terminal as view

from tasks.controller.lazy_controller import lazy_controller
from tasks.model.validators import validate_help, COMMAND_INDEX, ALLOWED_COMMANDS

controller_options = {
    "add": dm.validate_and_add_task,
    "list": dm.validate_and_get_list,
    "finish": dm.finish_task,
    "update": dm.validate_and_update_task,
    "remove": dm.validate_and_remove_task,
    "help": validate_help,
    "undo": dm.undo_task,
    "find": dm.find_task_for_table
}


def main_controller():
    try:
        sys_args = sys.argv
        cmd = sys_args[COMMAND_INDEX]
        if cmd not in ALLOWED_COMMANDS:
            view.print_message(success=False, msg_index=0)
            return
        elif cmd == "lazy":
            lazy_controller()
            return
        try:
            func = controller_options.get(cmd)
            success, msg_index = func(sys_args)
            view.print_message(success, msg_index,
                               print_help=func == validate_help,
                               listing=(func == dm.validate_and_get_list or func == dm.find_task_for_table))
        except TypeError:
            view.print_message(success=False, msg_index=0)

    except KeyboardInterrupt:
        view.show_info("\nWell, you could finish it more elegant... :)")

    except IndexError:
        view.show_info("You should provide some arguments after calling a program")
