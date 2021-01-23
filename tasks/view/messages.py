ERROR_MSG = {
    0: "Unknown command provided. Check >>> tasks.py help <<< to see possible options",
    1: "Invalid arguments provided. Check >>> tasks.py help <<< to see proper structure.",
    2: "Too many arguments provided. Check >>> tasks.py help <<< to see proper structure.",
    3: "Invalid optional arguments provided. Check >>> tasks.py help <<< to see proper structure.",
    4: "Wrong date provided. Date should be in format YYYY-MM-DD and can not be settled in past.",
    5: "No task with provided hash in database. Check it and try again.",
    6: "Some error occurred while adding tasks. Check your query and try again",
    7: "Too long value provided for some argument, check >>> tasks.py help <<< to see requirements",
    8: "Invalid argument for help command.",
    9: "This task is already marked as done.",
    10: "This task isn't done yet."
}

SUCCESS_MSG = {
    1: "Task created successfully.",
    2: "Task updated successfully",
    3: "Task marked as done.",
    4: "Task deleted successfully",
    5: "Task marked as undone."
}

HELP_MSG = {
    0: """
    All required parameters are without square brackets, like --name TASK_NAME or TASK_HASH.
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

    Find existing task:
        tasks.py find TASK_HASH 

        >>> tasks.py help find <<< to see more detailed help

    Mark task as done:
        tasks.py finish TASK_HASH

        >>> tasks.py help finish <<< to see more detailed help

    Mark task as undone:
        tasks.py undo TASK_HASH

        >>> tasks.py help undone <<< to see more detailed help    

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
    TASK_HASH: randomly generated hash value for task. You can get it from >>> tasks.py list <<<, last column. 
               Needs to be provided as last argument of query.

    OPTIONAL:
    --name: String with new name of your task. Max. 50 characters.
    --deadline: Datetime with new deadline of your task. Should be in format YYYY-MM-DD and can't be settled in past.
                You can type --deadline remove to delete deadline from your task.
    --description: String with new description of your task. Max. 50 characters.
                   You can type --description remove to delete description from your task.

    Non entered options will not be changed. You can provide all optional parameters at once.

    EXAMPLES:
    >>>tasks.py update --name "Remove something" 12345678
    >>>tasks.py update --description "Don't remove plug from bathtub" 1234567
    >>>tasks.py update --deadline remove --description "Don't hurry with that" 12345678
    """,
    3: """
    Remove task parameters:
        tasks.py remove TASK_HASH 

    REQUIRED:
    TASK_HASH: randomly generated hash value for task. You can get it from >>> tasks.py list <<<, last column.

    No optional arguments needed.
    Be careful, deleted data can not be restored.
    """,
    4: """
    Finish task parameters:
        tasks.py finish TASK_HASH

    REQUIRED:
        TASK_HASH: randomly generated hash value for task. You can get it from >>> tasks.py list <<<, last column.

    Mark chosen task as done. All finished tasks can be seen at >> tasks.py list --done <<<
    You can undo task by >>> task.py undo TASK_HASH <<<
    """,
    5: """
    List tasks parameters:
        tasks.py list [--all | --today | --missed | --week | --done] 

    OPTIONAL:
        --all: Default option, list all undone tasks.
        --today: List all tasks where deadline is settled for today.
        --missed: List all tasks where deadline is in the past.
        --week: List all tasks where the deadline expires within the next 7 days.
        --done: List all tasks marked as done.

    You can provide only 1 optional parameter. 
    All tasks are ordered by deadline.
    """,
    6: """
    Finish task parameters:
        tasks.py undo TASK_HASH

    REQUIRED:
        TASK_HASH: randomly generated hash value for task. You can get it from >>> tasks.py list <<<, last column.

    Mark chosen task as undone. All finished tasks can be seen at >> tasks.py list --done <<< and they can be 
    marked as undone again.
    """,
    7: """
    Find task parameters:
        tasks.py find TASK_HASH

    REQUIRED:
        TASK_HASH: randomly generated hash value for task. You can get it from >>> tasks.py list <<<, last column.

    Print all found tasks properties.    
    """
}