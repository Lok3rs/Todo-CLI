from datetime import datetime, timedelta

from tasks import session
from tasks.model.model import Task


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
             task.deadline if task.deadline else "No hurry",
             task.description,
             task.creation_date,
             task.task_hash]
            for task in get_tasks(option)]


def find_task_by_hash(args, hash_index):
    task = session.query(Task).filter(Task.task_hash == args[hash_index]).first()
    return task


def finish_task(task):
    task.done = True
    session.commit()
