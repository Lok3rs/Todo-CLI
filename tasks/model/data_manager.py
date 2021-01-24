from datetime import datetime, timedelta
from typing import List, Union, Tuple

from tasks import session
from tasks.model.model import Task
from tasks.model.util import table_for_not_found_data
from tasks.model.validators import validate_add_task_arguments, validate_update_args, validate_listing_arguments
from sqlalchemy.exc import DataError

"""
UNIVERSAL FUNCTIONS
"""


def add_task(name: str, deadline: datetime.date = None, description: str = None) -> Task:
    """
    Function that adds a new task to database.

    :param name: Task.name, string(max 30 chars long). Required
    :param deadline: Task.deadline, datetime.date object. Optional.
    :param description: Task.description, string(max 150 chars long). Optional
    :return: Task object with given properties.
    """
    new_task = Task(name=name, deadline=deadline, description=description)
    session.add(new_task)
    session.commit()
    return new_task


def get_column_names() -> List[str]:
    """
    :return: list of database column names declared in Task object, without 'ID' and 'Done' columns.
    """
    id_index = 1
    done_index = -1
    return Task.__table__.columns.keys()[id_index:done_index]


def get_tasks(option: str) -> List[Task]:
    """
    Function which returns a list of Task objects with given criteria.

    :param option: filtering option for dictionary declared in a function. Possible: --all, --today, --missed,
                    --week, --done
    :return: list of Task objects filtered by given option. If wrong option provided, return all objects.
    """
    today = datetime.date(datetime.utcnow()).strftime("%Y-%m-%d")
    week_later = (datetime.date(datetime.utcnow()) + timedelta(days=7)).strftime("%Y-%m-%d")
    option_dict = {
        "--all": session.query(Task)
                        .filter(Task.done.is_(False))
                        .order_by(Task.deadline.is_(None), Task.deadline)
                        .all(),
        "--today": session.query(Task)
                          .filter(Task.deadline == today, Task.done.is_(False))
                          .all(),
        "--missed": session.query(Task)
                           .filter(Task.deadline < today, Task.done.is_(False))
                           .all(),
        "--week": session.query(Task)
                         .filter(Task.deadline < week_later, Task.done.is_(False))
                         .all(),
        "--done": session.query(Task)
                         .filter(Task.done)
                         .all()
    }
    if option not in option_dict.keys():
        return option_dict.get("--all")
    return option_dict.get(option)


def get_task_values(option: str) -> List[List]:
    """
    A function that uses the get_tasks function with an option selected, and returns the data prepared for printing

    :param option: a filtering option to be used in the get_tasks function. Possible: --all, --today, --missed,
                    --week, --done
    :return: list containing lists of tasks values with an option selected, prepared to be printed for the user.
    """
    return [[task.name,
             task.deadline.strftime("%Y-%m-%d") if task.deadline else "No hurry",
             task.description if task.description else "---",
             task.creation_date.strftime("%Y-%m-%d %H:%M"),
             task.task_hash]
            for task in get_tasks(option)]


def get_table(option: str) -> List[List]:
    """
    A function that prepares tables for printing, database column names with the values of the selected option
    (option passed to the get_task_values function).

    :param option: a filtering option to be used in the get_task_values function. Possible: --all, --today,
                 --missed, --week, --done
    :return: list containing lists of column names and tasks values with an option selected, prepared to be printed
                for the user.
    """
    return [get_column_names(), *get_task_values(option)] if get_task_values(option) \
        else [get_column_names(), table_for_not_found_data]


def get_table_with_one_record(task: Task):
    """
    A function that prepares table for printing, database column names with the values of provided Task object.

    :param task: Task class object
    :return: list containing lists of column names and task values, prepared to be printed for the user.
    """
    return [get_column_names(),
            [task.name,
             task.deadline.strftime("%Y-%m-%d") if task.deadline else "No hurry",
             task.description if task.description else "---",
             task.creation_date.strftime("%Y-%m-%d %h:%M"),
             task.task_hash]]


"""
FUNCTIONS FOR COMMAND LINE MODE
"""


def validate_and_add_task(sys_args: List[str]) -> Tuple[bool, int]:
    """
    Validate and, if validated, fires add_task function, which creates a new Task class object

    :param sys_args: List of arguments received from the command line
    :return: Tuple of boolean and integer. Boolean means if it was successful, integer is index of message from
             messages.py
    """
    try:
        task_validation = validate_add_task_arguments(sys_args)
        if type(task_validation) == dict:
            new_task = add_task(name=task_validation.get("name"),
                                deadline=task_validation.get("deadline"),
                                description=task_validation.get("description"))
            return True, 1 if new_task else (False, 6)
        else:
            return False, task_validation
    except DataError:
        return False, 7


def find_task_by_hash(sys_args: List[str], hash_index: int) -> Task:
    """
    Finds the "Task" object by passing it a list of system arguments and indicating on which index the hash value of
    the searched element is located.

    :param sys_args: list of arguments provided in command line
    :param hash_index: integer which points to the index under which the hash value is
    :return: Task class object
    """
    task = session.query(Task).filter(Task.task_hash == sys_args[hash_index]).first()
    return task


def find_task_for_table(sys_args: List[str]) -> Union[Tuple[bool, List], Tuple[bool, int]]:
    """
    Function returning True or False value, indicating its success and tables with the found "Task" object or message
    index in case of its failure. Used for listing one record for rind or remove tasks functionality.

    :param sys_args: list of arguments provided in command line
    :return: tuple of boolean value meaning if it was successful and table with found Task or error message
    """
    hash_index = 2
    task = find_task_by_hash(sys_args, hash_index)
    if task:
        return True, get_table_with_one_record(task)
    return False, 5


def finish_task(sys_args: List[str]) -> Tuple[bool, int]:
    """
    Function that changes Task's "Done" column value to True, if it is not.

    :param sys_args: list of arguments provided in command line
    :return: tuple with boolean value meaning if it was successful and index of message
    """
    hash_index = 2
    task = find_task_by_hash(sys_args, hash_index)
    if task and task.done:
        return False, 9
    elif task:
        task.done = True
        session.commit()
        return True, 3
    return False, 5


def undo_task(sys_args: List[str]) -> Tuple[bool, int]:
    """
    Function that changes Task's "Done" column value to False, if it is not.

    :param sys_args: list of arguments provided in command line
    :return: tuple with boolean value meaning if it was successful and index of message
    """
    task = find_task_by_hash(sys_args, 2)
    if task and not task.done:
        return False, 10
    elif task:
        task.done = False
        session.commit()
        return True, 5
    return False, 5


def validate_and_update_task(sys_args: List[str]) -> Tuple[bool, int]:
    """
    A function that validates entered system arguments for updating a job and changes or removes them depending on the
    options selected.

    :param sys_args: list of arguments provided in command line
    :return: tuple with boolean value meaning if it was successful and index of message
    """

    try:
        task = find_task_by_hash(sys_args, -1)
        if not task:
            return False, 5
        new_values_validator = validate_update_args(sys_args)
        if type(new_values_validator) != dict:
            return False, new_values_validator

        new_name = new_values_validator.get("name")
        new_deadline = new_values_validator.get("deadline")
        new_description = new_values_validator.get("description")

        task.name = new_name \
            if new_name else task.name

        task.deadline = None if new_deadline == "remove" \
            else (new_deadline if new_deadline
                  else task.deadline)

        task.description = None if new_description == "remove" \
            else (new_description if new_description
                  else task.description)

        session.commit()
        return True, 2
    except DataError:
        return False, 7


def validate_and_get_list(sys_args: List[str]) -> Union[Tuple[bool, List], Tuple[bool, int]]:
    """
    Function that validates arguments provided in command line for listing records a and return table with chosen
    option, if was valid.

    :param sys_args: list of arguments provided in command line
    :return: tuple with boolean value meaning if it was successful and table, if validated, or wrong option which
            was provided
    """
    list_option = validate_listing_arguments(sys_args)
    if type(list_option) != str:
        return False, list_option
    return True, get_table(list_option)


def validate_and_remove_task(sys_args: List[str]) -> Tuple[bool, int]:
    """
    A function that validates whether a task with a hash specified on the command line exists and, if it exists,
    removes it.

    :param sys_args: list of arguments provided in command line
    :return: tuple with boolean value meaning if it was successful and index of message
    """
    hash_index = 2
    task = find_task_by_hash(sys_args, hash_index)
    if not task:
        return False, 5
    session.delete(task)
    session.commit()
    return True, 4


"""
LAZY MODE FUNCTIONS
"""


def lazy_find_task(task_hash: Union[str, int]) -> Task:
    """
    Function for lazy mode. Look for task with provided task_hash and returns it.

    :param task_hash: hash value of the searched object
    :return: Task class object with provided hash value, if found
    """
    return session.query(Task).filter(Task.task_hash == task_hash).first()


def lazy_find_and_remove_task(task_hash: str) -> Tuple[bool, int]:
    """
    Function for lazy mode. Look for task with provided task_hash and removes it from database

    :param task_hash: hash value for the object to be deleted
    :return: tuple with boolean value meaning if it was successful and index of message
    """
    task = lazy_find_task(task_hash)
    if task:
        session.delete(task)
        session.commit()
        return True, 4
    return False, 5


def lazy_update_task(task: Task, name: str, deadline: datetime.date, description: str) -> Tuple[bool, int]:
    """
    Lazy mode function. Updates, removes or keep current values of provided task.

    :param task: Task class object to be updated
    :param name: New name for provided task. Keeps current if None.
    :param deadline: New deadline for provided task. Keeps current if None or removes it if "remove" provided.
    :param description: New description for provided task. Keeps current if None or removes it if "remove" provided.
    :return: tuple with boolean value meaning if it was successful and index of message
    """
    if not lazy_find_task(task.task_hash):
        return False, 5
    task.name = name if name else task.name

    task.deadline = deadline if deadline == "remove" else \
        (deadline if deadline else task.deadline)

    task.description = description if description == "remove" else \
        (description if description else task.description)

    session.commit()
    return True, 2


def lazy_finish_or_undo_task(task: Task) -> Tuple[bool, int]:
    """
    Lazy mode function. Changes task's "Done" column to opposite value.

    :param task: Task class object.
    :return: tuple with boolean value meaning if it was successful and index of message
    """
    if not lazy_find_task(task.task_hash):
        return False, 5
    if task.done:
        ret_val = (True, 5)
    else:
        ret_val = (True, 3)
    task.done = not task.done
    return ret_val
