from tasks.model.data_manager import get_table, add_task, lazy_find_and_remove_task, lazy_find_task, lazy_update_task, \
    lazy_finish_or_undo_task, get_table_with_one_record
from tasks.model.util import clear_screen, wait
from tasks.model.validators import validate_deadline
from tasks.view.terminal import print_menu, main_menu_options, get_user_input, list_menu_options, print_table, \
    print_message, show_info


def lazy_controller():
    option = 1
    cls_mode = False
    while option != "0":
        print_menu(main_menu_options)
        option = get_user_input()
        while not option.isnumeric() or int(option) not in range(len(main_menu_options)):
            option = get_user_input("Invalid option, try again: ")
        option = lazy_controller_options.get(int(option))
        if option == "cls_change":
            cls_mode = not cls_mode
        else:
            option()
        if cls_mode:
            clear_screen()


def listing_controller():
    print_menu(list_menu_options, header="Listing menu")
    option = get_user_input()
    if option == "0":
        return
    while not option.isnumeric() or int(option) not in range(len(list_menu_options)):
        option = get_user_input("Invalid option, try again: ")
    listing_option = listing_controller_options.get(int(option))
    print_table(get_table(listing_option))
    wait()


def new_task_controller():
    name = get_user_input("Task name (max 30 characters): ")
    while len(name) > 30:
        name = get_user_input("Name is too long, try again: ")

    description = get_user_input("Task description (optional, type ENTER to skip. Max 150 characters): ")
    while len(description) > 150:
        description = get_user_input("Description is too long, try again: ")
    if len(description.strip()) == 0:
        description = None

    deadline = get_user_input("Task deadline (optional, type ENTER to skip. In format YYYY-MM-DD, can't be in past")

    while len(deadline.strip()) != 0 and not validate_deadline(deadline):
        deadline = get_user_input("Invalid date, try again: ")

    deadline = validate_deadline(deadline) if len(deadline.strip()) != 0 else None

    add_task(name=name, deadline=deadline, description=description)
    print_message(success=True, msg_index=1)
    wait()


def remove_task_controller():
    task_hash = get_user_input("Provide a hash of task to delete (type ENTER to cancel")
    if len(task_hash.strip()) == 0:
        print_message(success=False, msg_index=11)
    else:
        success, msg_index = lazy_find_and_remove_task(task_hash)
        print_message(success, msg_index)
    wait()


def update_task_controller():
    task_hash = get_user_input("Provide a hash of task you want to delete (type ENTER to cancel): ")
    if len(task_hash.strip()) == 0:
        print_message(success=False, msg_index=11)
        wait()
        return
    task = lazy_find_task(task_hash)
    if not task:
        print_message(success=False, msg_index=5)
        wait()
        return

    show_info(f"Current task name '{task.name}'")
    new_name = get_user_input("New task name (max 30 characters, type ENTER to keep current name): ")
    while len(new_name.strip()) > 30:
        new_name = get_user_input("Name is too long, try again: ")
    if len(new_name.strip()) == 0:
        new_name = None

    show_info(f"Current description: '{task.description}'") if task.description \
        else show_info("No description for this task")
    new_description = get_user_input("New task description (optional, type ENTER to skip. Max 150 characters): ")
    while len(new_description) > 150:
        new_description = get_user_input("Description is too long, try again: ")
    if len(new_description.strip()) == 0:
        new_description = None

    show_info(f"Current deadline: {task.deadline.strftime('%Y-%m-%d')}") if task.deadline \
        else show_info("No deadline settled for this task.")
    new_deadline = get_user_input("Task deadline (optional, type ENTER to skip. "
                                  "In format YYYY-MM-DD, can't be in past): ")

    while len(new_deadline.strip()) != 0 or not validate_deadline(new_deadline):
        new_deadline = get_user_input("Invalid date, try again: ")

    new_deadline = validate_deadline(new_deadline) if len(new_deadline.strip()) != 0 else None

    success, msg_index = lazy_update_task(task=task, name=new_name, description=new_description, deadline=new_deadline)
    print_message(success, msg_index)
    wait()


def finish_or_undo_task_controller():
    task_hash = get_user_input("Provide a hash of task you want to finish or mark as undone (type ENTER to cancel): ")
    if len(task_hash.strip()) == 0:
        print_message(success=False, msg_index=11)
        wait()
        return
    task = lazy_find_task(task_hash)
    if not task:
        print_message(success=False, msg_index=5)
        wait()
        return
    success, msg_index = lazy_finish_or_undo_task(task)
    print_message(success, msg_index)
    wait()


def find_task_controller():
    task_hash = get_user_input("Provide a hash of task to find (type ENTER to cancel): ")
    if len(task_hash.strip()) == 0:
        print_message(success=False, msg_index=11)
        wait()
        return
    task = lazy_find_task(task_hash)
    if not task:
        print_message(success=False, msg_index=5)
        wait()
        return
    print_table(get_table_with_one_record(task))
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
