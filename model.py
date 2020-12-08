import os
from peewee import Model, CharField, DateTimeField, TextField, ForeignKeyField
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))


class User(Model):
    username = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)

    class Meta:
        database = db


class Task(Model):
    taskname = CharField(max_length=255)
    # description = TextField()
    completed = DateTimeField(null=True)
    completed_by = ForeignKeyField(model=User, null=True)

    class Meta:
        database = db
