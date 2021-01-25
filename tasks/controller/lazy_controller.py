from tasks import view, validator
from tasks.model.util import clear_screen, wait
from tasks.view.terminal import main_menu_options, list_menu_options
from tasks.model.data_manager import LazyDataManager

lazy_dm = LazyDataManager()


def lazy_controller():
    option = 1
    cls_mode = False
    while option != "0":
        view.print_menu(main_menu_options)
        option = view.get_user_input()
        while not option.isnumeric() or int(option) not in range(len(main_menu_options)):
            option = view.get_user_input("Invalid option, try again: ")
        option = lazy_controller_options.get(int(option))
        if option == "cls_change":
            cls_mode = not cls_mode
        else:
            option()
        if cls_mode:
            clear_screen()


def listing_controller():
    view.print_menu(list_menu_options, header="Listing menu")
    option = view.get_user_input()
    if option == "0":
        return
    while not option.isnumeric() or int(option) not in range(len(list_menu_options)):
        option = view.get_user_input("Invalid option, try again: ")
    listing_option = listing_controller_options.get(int(option))
    view.print_table(lazy_dm.get_table(listing_option))
    wait()


def new_task_controller():
    name = view.get_user_input("Task name (required, 1-30 characters): ")
    while len(name) > 30 or len(name) == 0:
        name = view.get_user_input("Name needs to be 1-30 characters long, try again: ")

    description = view.get_user_input("Task description (optional, press ENTER to skip. Max 100 characters): ")
    while len(description) > 100:
        description = view.get_user_input("Description is too long, try again: ")
    if len(description.strip()) == 0:
        description = None

    deadline = view.get_user_input(
        "Task deadline (optional, type ENTER to skip. In format YYYY-MM-DD, can't be in past): ")

    while len(deadline.strip()) != 0 and not validator.validate_deadline(deadline):
        deadline = view.get_user_input("Invalid date, try again or press ENTER to skip: ")

    deadline = validator.validate_deadline(deadline) if len(deadline.strip()) != 0 else None

    lazy_dm.add_task(name=name, deadline=deadline, description=description)
    view.print_message(success=True, msg_index=1)
    wait()


def remove_task_controller():
    task_hash = view.get_user_input("Provide a hash of task to delete (press ENTER to cancel): ")
    if len(task_hash.strip()) == 0:
        view.print_message(success=False, msg_index=11)
    else:
        success, msg_index = lazy_dm.lazy_find_and_remove_task(task_hash)
        view.print_message(success, msg_index)
    wait()


def update_task_controller():
    task_hash = view.get_user_input("Provide a hash of task you want to delete (press ENTER to cancel): ")
    if len(task_hash.strip()) == 0:
        view.print_message(success=False, msg_index=11)
        wait()
        return
    task = lazy_dm.lazy_find_task(task_hash)
    if not task:
        view.print_message(success=False, msg_index=5)
        wait()
        return

    view.show_info(f"Current task name '{task.name}'")
    new_name = view.get_user_input("New task name (max 30 characters, press ENTER to keep current name): ")
    while len(new_name.strip()) > 30:
        new_name = view.get_user_input("Name is too long, try again: ")
    if len(new_name.strip()) == 0:
        new_name = None

    view.show_info(f"Current description: '{task.description}'" if task.description
                   else "No description for this task")
    new_description = view.get_user_input("New task description (optional, press ENTER to skip. Max 100 characters): ")
    while len(new_description) > 100:
        new_description = view.get_user_input("Description is too long, try again: ")
    if len(new_description.strip()) == 0:
        new_description = None

    view.show_info(f"Current deadline: {task.deadline.strftime('%Y-%m-%d')}" if task.deadline
                   else "No deadline settled for this task.")
    new_deadline = view.get_user_input("Task deadline (optional, press ENTER to skip. "
                                       "In format YYYY-MM-DD, can't be in past): ")

    while len(new_deadline.strip()) != 0 and not validator.validate_deadline(new_deadline):
        new_deadline = view.get_user_input("Invalid date, try again: ")

    new_deadline = validator.validate_deadline(new_deadline) if len(new_deadline.strip()) != 0 else None

    success, msg_index = lazy_dm.lazy_update_task(task=task, name=new_name,
                                                  description=new_description, deadline=new_deadline)
    view.print_message(success, msg_index)
    wait()


def finish_or_undo_task_controller():
    task_hash = view.get_user_input(
        "Provide a hash of task you want to finish or mark as undone (press ENTER to cancel): ")
    if len(task_hash.strip()) == 0:
        view.print_message(success=False, msg_index=11)
        wait()
        return
    task = lazy_dm.lazy_find_task(task_hash)
    if not task:
        view.print_message(success=False, msg_index=5)
        wait()
        return
    success, msg_index = lazy_dm.lazy_finish_or_undo_task(task)
    view.print_message(success, msg_index)
    wait()


def find_task_controller():
    task_hash = view.get_user_input("Provide a hash of task to find (press ENTER to cancel): ")
    if len(task_hash.strip()) == 0:
        view.print_message(success=False, msg_index=11)
        wait()
        return
    task = lazy_dm.lazy_find_task(task_hash)
    if not task:
        view.print_message(success=False, msg_index=5)
        wait()
        return
    view.print_table(lazy_dm.get_table_with_one_record(task))
    wait()


lazy_controller_options = {
    1: new_task_controller,
    2: listing_controller,
    3: remove_task_controller,
    4: update_task_controller,
    5: finish_or_undo_task_controller,
    6: find_task_controller,
    7: "cls_change",
    0: exit
}

listing_controller_options = {
    1: "--all",
    2: "--today",
    3: "--week",
    4: "--missed",
    5: "--done"
}
