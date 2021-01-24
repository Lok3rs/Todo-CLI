import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.ddl import CreateTable
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import OperationalError

from tasks.model.model import Task

engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
    os.environ.get("MYSQL_USERNAME"),
    os.environ.get("MYSQL_PASSWORD"),
    os.environ.get("MYSQL_HOST"),
    os.environ.get("MYSQL_DB")
))

meta = MetaData()
meta.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

tasks_table = Task.__table__

try:
    if not database_exists(engine.url):
        create_database(engine.url)
        meta.create_all()
        engine.connect().execute(CreateTable(tasks_table))
        print(f"Database named {os.environ.get('MYSQL_DB')} created successfully.")
    else:
        engine.connect()
except OperationalError as err:
    print(err)
