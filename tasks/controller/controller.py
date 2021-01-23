import sys
from typing import List

from tasks.model.data_manager import finish_task, validate_and_update_task, validate_and_add_task, \
    validate_and_get_list, validate_and_remove_task
from tasks.model.util import COMMAND_INDEX, ALLOWED_COMMANDS
from tasks.view.terminal import print_table, print_message, ERROR_MSG, SUCCESS_MSG


def add_task_controller(sys_args: List[str]):
    success, result = validate_and_add_task(sys_args)
    print_message(SUCCESS_MSG.get(result)) if success else print_message(ERROR_MSG.get(result))


def list_tasks_controller(sys_args: List[str]):
    success, result = validate_and_get_list(sys_args)
    print_table(result) if success else print_message(ERROR_MSG.get(result))


def finish_task_controller(sys_args: List[str]):
    success, result = finish_task(sys_args)
    print_message(SUCCESS_MSG.get(result)) if success else print_message(ERROR_MSG.get(result))


def update_task_controller(sys_args: List[str]):
    success, result = validate_and_update_task(sys_args)
    print_message(SUCCESS_MSG.get(result)) if success else print_message(ERROR_MSG.get(result))


def remove_task_controller(sys_args: List[str]):
    success, result = validate_and_remove_task(sys_args)
    print_message(SUCCESS_MSG.get(result)) if success else print_message(ERROR_MSG.get(result))


controller_options = {
    "add": add_task_controller,
    "list": list_tasks_controller,
    "finish": finish_task_controller,
    "update": update_task_controller,
    "remove": remove_task_controller
}


def main():
    sys_args = sys.argv
    cmd = sys_args[COMMAND_INDEX]
    if cmd not in ALLOWED_COMMANDS:
        print_message(ERROR_MSG.get(0))
    controller_options.get(cmd)(sys_args)
