import sys

from sqlalchemy.exc import OperationalError

from tasks import view, validator
from tasks.model.data_manager import CMDDataManager
from tasks.controller.lazy_controller import lazy_controller
from tasks.model.validators import COMMAND_INDEX, ALLOWED_COMMANDS

cmd_dm = CMDDataManager()


controller_options = {
    "add": cmd_dm.validate_and_add_task,
    "list": cmd_dm.validate_and_get_list,
    "finish": cmd_dm.finish_task,
    "update": cmd_dm.validate_and_update_task,
    "remove": cmd_dm.validate_and_remove_task,
    "help": validator.validate_help,
    "undo": cmd_dm.undo_task,
    "find": cmd_dm.find_task_for_table
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

        func = controller_options.get(cmd)
        success, msg_index = func(sys_args)
        view.print_message(success, msg_index,
                           print_help=func == validator.validate_help,
                           listing=(func == cmd_dm.validate_and_get_list or func == cmd_dm.find_task_for_table))

    except KeyboardInterrupt:
        view.show_info("\nWell, you could finish it more elegant... :)")

    except IndexError:
        view.show_info("You should provide some arguments after calling a program")

    except OperationalError:
        view.show_info("Problem with connection to database. Check if all your environment "
                       "variables are settled properly")

    except TypeError:
        view.print_message(success=False, msg_index=0)
