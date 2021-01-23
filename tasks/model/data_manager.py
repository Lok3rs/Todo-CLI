from datetime import datetime, timedelta
from typing import List, Union, Tuple, Dict

from tasks import session
from tasks.model.model import Task
from tasks.model.validators import validate_add_task_arguments, validate_update_args, validate_listing_arguments


def validate_and_add_task(sys_args: List[str]):
    task_validation = validate_add_task_arguments(sys_args)
    if type(task_validation) == dict:
        new_task = add_task(name=task_validation.get("name"),
                            deadline=task_validation.get("deadline"),
                            description=task_validation.get("description"))
        return True, 1 if new_task else False, 6
    else:
        return False, task_validation


def add_task(name: str, deadline: datetime = None, description: str = None) -> Task:
    new_task = Task(name=name, deadline=deadline, description=description)
    session.add(new_task)
    session.commit()
    return new_task


def get_tasks(option: str) -> List[Task]:
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
    return option_dict.get(option)


def get_column_names() -> List[str]:
    return Task.__table__.columns.keys()[1:-1]


def get_task_values(option: str) -> List[List]:
    return [[task.name,
             task.deadline.strftime("%Y-%m-%d") if task.deadline else "No hurry",
             task.description,
             task.creation_date,
             task.task_hash]
            for task in get_tasks(option)]


def get_table(option: str) -> List[List]:
    return [get_column_names(), *get_task_values(option)]


def find_task_by_hash(sys_args: List[str], hash_index: int) -> Task:
    task = session.query(Task).filter(Task.task_hash == sys_args[hash_index]).first()
    return task


def finish_task(sys_args: List[str]) -> Union[Tuple[bool, str], Tuple[bool, int]]:
    task = find_task_by_hash(sys_args, 2)
    if task:
        task.done = True
        session.commit()
        return True, 3
    return False, 5


def validate_and_update_task(sys_args: List[str]) -> Tuple[bool, int]:
    task = find_task_by_hash(sys_args, -1)
    if not task:
        return False, 5
    new_values_validator = validate_update_args(sys_args)
    if type(new_values_validator) != dict:
        return False, new_values_validator
    task.name = new_values_validator.get("name") \
        if new_values_validator.get("name") else task.name
    task.deadline = new_values_validator.get("deadline") \
        if new_values_validator.get("deadline") else task.deadline
    task.description = new_values_validator.get("description") \
        if new_values_validator.get("description") else task.description
    session.commit()
    return True, 2


def validate_and_get_list(sys_args: List[str]) -> Union[Tuple[bool, List], Tuple[bool, int]]:
    list_option = validate_listing_arguments(sys_args)
    if type(list_option) != str:
        return False, list_option
    return True, get_table(list_option)


def validate_and_remove_task(sys_args: List[str]) -> Tuple[bool, int]:
    task = find_task_by_hash(sys_args, 2)
    if not task:
        return False, 5
    session.delete(task)
    session.commit()
    return True, 4
