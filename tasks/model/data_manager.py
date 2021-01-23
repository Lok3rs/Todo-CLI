from datetime import datetime, timedelta

from tasks import session
from tasks.model.model import Task
from tasks.model.validators import validate_add_task_arguments, validate_update_args, validate_listing_arguments


def validate_and_add_task(args):
    task_validation = validate_add_task_arguments(args)
    if type(task_validation) == dict:
        new_task = add_task(name=task_validation.get("name"),
                            deadline=task_validation.get("deadline"),
                            description=task_validation.get("description"))
        return True, f"Successfully created task: {new_task.name}!"
    else:
        return False, task_validation


def add_task(name, deadline=None, description=None):
    new_task = Task(name=name, deadline=deadline, description=description)
    session.add(new_task)
    session.commit()
    return new_task


def get_tasks(option):
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


def get_column_names():
    return Task.__table__.columns.keys()[1:-1]


def get_task_values(option):
    return [[task.name,
             task.deadline.strftime("%Y-%m-%d") if task.deadline else "No hurry",
             task.description,
             task.creation_date,
             task.task_hash]
            for task in get_tasks(option)]


def get_table(option):
    return [get_column_names(), *get_task_values(option)]


def find_task_by_hash(args, hash_index):
    task = session.query(Task).filter(Task.task_hash == args[hash_index]).first()
    return task


def finish_task(args):
    task = find_task_by_hash(args, 2)
    if task:
        task.done = True
        session.commit()
        return True, f"Task {task.name} marked as done!"
    return False, 5


def validate_and_update_task(args):
    task = find_task_by_hash(args, -1)
    if not task:
        print("Wrong hash")
        return False, f"Can not find task with hash of {args[-1]}"
    new_values_validator = validate_update_args(args)
    if type(new_values_validator) != dict:
        return False, new_values_validator
    task.name = new_values_validator.get("name") if new_values_validator.get("name") else task.name
    task.deadline = new_values_validator.get("deadline") if new_values_validator.get("deadline") else task.deadline
    task.description = new_values_validator.get("description") if new_values_validator.get("description") else task.description
    session.commit()
    return True, "Task successfully updated!"


def validate_and_get_list(args):
    list_option = validate_listing_arguments(args)
    if type(list_option) != str:
        return False, list_option
    return True, get_table(list_option)
