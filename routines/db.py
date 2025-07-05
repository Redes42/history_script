import os
import sqlite3

from .consts import *


cursor = None
connection = None


def establish_connection(path: str):
    global cursor
    global connection
    if not os.path.exists(f'{path}{HISTORY}'):
        os.mkdir(f'{path}{HISTORY}')
    connection = sqlite3.connect(f'{path}{HISTORY}history.db')
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = OFF")
    cursor = connection.cursor()


def exec_sql(query: str, data: tuple=None):
    global cursor
    global connection
    if data:
        return cursor.execute(query, data)
    else:
        return cursor.execute(query)
    

def commit():
    global connection
    connection.commit()


def disconnect():
    global connection
    connection.close()