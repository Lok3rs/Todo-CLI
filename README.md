# Simple Todo CLI App

Simple application that allows the user to manage the task list and save it in SQL database.


## Depedencies
Most important thing is `python` installed in version 3 or above.
All required packages are stored in `requirements.txt` file.

I recommend to use virtual environment -> https://docs.python.org/3/tutorial/venv.html
```
$ pip install -r requirements.txt
```

## Setting up environment
Inside of `__init__.py` file you can find configuration of database connection.

```python
engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
    os.environ.get("MYSQL_USERNAME"),
    os.environ.get("MYSQL_PASSWORD"),
    os.environ.get("MYSQL_HOST"),
    os.environ.get("MYSQL_DB")
))
```
By default it is set to MySQL database, but thanks to SQLAlchemy you can change it do any SQL db.

If you want to used app with any other SQL check https://docs.sqlalchemy.org/en/14/core/engines.html to see proper connection strings and change it inside of ```create_engine()```

Next step is to set environment variables used by `create_engine()`

**Linux/Mac**
```
$ export MYSQL_USERNAME=your_sql_username (root is default username)
$ export MYSQL_PASSWORD=your_password
$ export MYSQL_HOST=host (localhost if you do that locally)
$ export MYSQL_DB=your_db_name (if doesn't exists app will create it)
```

**Windows**
```
$ SET MYSQL_USERNAME=your_sql_username (root is default username)
$ SET MYSQL_PASSWORD=your_password
$ SET MYSQL_HOST=host (localhost if you do that locally)
$ SET MYSQL_DB=your_db_name (if doesn't exists app will create it)
```



**Calling python scripts without `python` keyword in command line**

>> **Linux/Mac**
>- https://superuser.com/questions/828737/run-python-scripts-without-explicitly-invoking-python
>> **Windows**
>- https://stackoverflow.com/questions/11472843/set-up-python-on-windows-to-not-type-python-in-cmd


## Usage

You can find all needed informations by typing `tasks.py help` in command line

```
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

    Lazy mode:
        tasks.py lazy

        Launches the program with a user-visible menu for managing the task list
```
