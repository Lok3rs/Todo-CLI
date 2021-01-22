ERROR_MSG = {
    1: "Invalid argument. Type tasks.py add --help to see some tips",
    2: "Wrong arguments provided. Check task.py add --help to see proper structure.",
    3: "Invalid argument for 'add' method. Use tasks.py add --help to see possible options.",
    4: "Too many arguments provided. Check --help to see proper structure",
    5: "Some error occurred while unpacking your optional arguments. Type tasks.py add --help to see proper structure",
    6: "Wrong argument provided. Check --help to see proper structure.",
    7: "Wrong date provided. Date should be in format YYYY-MM-DD.",
    8: "Deadline date cannot be settled in past."
}


def print_message(message):
    print(message)


def print_table(tables):
    table_with_strings = [[str(element) for element in table] for table in tables]
    space_around = 2
    column_separator = "|"
    row_separator = "-"
    corner_ac = "/"
    corner_bd = "\\"
    max_column_width = [0 for element in range(len(table_with_strings[0]))]

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
