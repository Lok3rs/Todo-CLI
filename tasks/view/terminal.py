ERROR_MSG = {
    0: "Unknown command provided. Check help to see possible options",
    1: "Invalid arguments provided. Check help to see proper structure.",
    2: "Too many arguments provided. Check help to see proper structure.",
    3: "Invalid optional arguments provided. Check help to see proper structure.",
    4: "Wrong date provided. Date should be in format YYYY-MM-DD and can not be settled in past.",
    5: "No task with provided hash in database. Check it and try again.",
    6: "Some error occurred while adding tasks. Check your query and try again",
    7: "Too long value provided for some argument, check help to see requirements"
}

SUCCESS_MSG = {
    1: "Task created successfully.",
    2: "Task updated successfully",
    3: "Task marked as done.",
    4: "Task deleted successfully"
}

HELP_MSG = {
    0: """
    All required parameters are without square brackets, like --name.
    Strings longer than 1 word should be placed inside quotes, eq. "New Task Name"
    Parameter inside square brackets are optional, like [--deadline DATETIME].
    You should provided them without brackets, eq.: 
        tasks.py add --name "New Task" --deadline 2022-02-03 --description "Description for new task"
    
    Add new tasks:
        tasks.py add --name TASK_NAME [--deadline DATETIME(%Y-%m-%d)] [--description DESCRIPTION]
        
        >>> tasks.py help add <<< to see more detailed help
        
    Listing tasks:
        tasks.py list [--all | --today | --missed | --week | --done] 
        --all by default, only 1 parameter allowed.
        
        >>> tasks.py help list <<< to see more detailed help
    
    Update existing task:
        tasks.py update [--name NEW_NAME] [--deadline NEW_DATETIME(%Y-%m-%d)] [--description NEW_DESCRIPTION] TASK_HASH
        
        >>> tasks.py help update <<< to see more detailed help
        
    Mark task as done:
        tasks.py finish TASK_HASH
        
        >>> tasks.py help finish <<< to see more detailed help
        
    Remove existing task:
        tasks.py remove TASK_HASH 
        
        >>> tasks.py help remove <<< to see more detailed help
    """,
    1: """
    Add task parameters:
        tasks.py add --name TASK_NAME [--deadline DATETIME(%Y-%m-%d)] [--description DESCRIPTION]
    
    REQUIRED:
    --name: String with name of your task. Should be short and simple, eq. "Clean your room". Max. 30 characters allowed
    
    OPTIONAL:
    --deadline: Datetime with deadline of your task. Should be provided in format YYYY-MM-DD. Can't be settled in past.
    --description: String with more detailed description of your task. Max 100 characters allowed.
    
    EXAMPLES:
    >>>tasks.py add --name "Clean room" --deadline 2021-01-26 --description "Grab all clothes from the floor"
    >>>tasks.py add --name "Wash dishes"
    >>>tasks.py add --name "Correct the exam" --deadline 2021-02-02
    >>>tasks.py add --name "Format the computer" --description "REMEMBER TO SAVE YOUR DATA ON EXTERNAL DISC"
    """,
    2: """
    Update task parameters:
        tasks.py update [--name NEW_NAME] [--deadline NEW_DATETIME(%Y-%m-%d)] [--description NEW_DESCRIPTION] TASK_HASH
    
    REQUIRED:
    TASK_HASH: randomly generated hash value for task. You can get it from tasks.py list, last column. Needs to be 
               provided as last argument of query.
    
    OPTIONAL:
    --name: String with new name of your task. Max. 50 characters.
    --deadline: Datetime with new deadline of your task. Should be in format YYYY-MM-DD and can't be settled in past.
                You can type --deadline remove to delete deadline from your task.
    --description: String with new description of your task. Max. 50 characters.
                   You can type --description remove to delete description from your task.
                   
    Non entered options will not be changed.
    """
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
