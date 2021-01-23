from typing import Dict

from tasks.view.messages import HELP_MSG, SUCCESS_MSG, ERROR_MSG

main_menu_options = {1: "Add new task",
                     2: "List tasks",
                     3: "Remove task",
                     4: "Update existing task",
                     5: "Finish/undo task",
                     6: "Find task",
                     7: "Turn on/off cleaning screen",
                     0: "Exit"}

list_menu_options = {1: "List not finished tasks",
                     2: "List tasks where deadline is today",
                     3: "List tasks where deadline is within 1 week",
                     4: "List tasks where deadline is already in past",
                     5: "List finished tasks",
                     0: "Back to main menu"}


def print_menu(options: Dict, header: str = "Main Menu"):
    print(header)
    for k, v in options.items():
        print(f"{k} - {v}")


def get_user_input(label="Your choice: "):
    return input(label)


def print_message(success, msg_index, print_help=False, listing=False):
    if success and listing:
        print_table(msg_index)
    elif success and print_help:
        print(HELP_MSG.get(msg_index))
    elif success:
        print(SUCCESS_MSG.get(msg_index))
    else:
        print(ERROR_MSG.get(msg_index))


def print_table(tables):
    table_with_strings = [[str(element) for element in table] for table in tables]
    space_around = 2
    column_separator = "|"
    row_separator = "-"
    corner_ac = "/"
    corner_bd = "\\"
    max_column_width = [0 for _ in range(len(table_with_strings[0]))]

    for row in table_with_strings:
        for result_index in range(len(row)):
            max_column_width[result_index] = len(row[result_index]) + space_around \
                if max_column_width[result_index] - space_around < len(row[result_index]) \
                else max_column_width[result_index]

    break_line = column_separator + column_separator.join(
        [(row_separator * max_width) for max_width in max_column_width]) + column_separator
    start_line = corner_ac + row_separator.join(
        [(row_separator * max_width) for max_width in max_column_width]) + corner_bd
    end_line = corner_bd + row_separator.join(
        [(row_separator * max_width) for max_width in max_column_width]) + corner_ac

    print(start_line)
    for row in table_with_strings:
        printable_row = []
        for each_result in row:
            white_spaces = max_column_width[row.index(each_result)] - len(each_result)
            printable_row.append((white_spaces // 2 * " " if white_spaces % 2 == 0
                                  else (white_spaces // 2 + 1) * " ") + each_result +
                                 (white_spaces // 2) * " ")
        print(column_separator + column_separator.join(printable_row) + column_separator)
        print(break_line if row != table_with_strings[-1] else end_line)


def show_info(info):
    print(info)
