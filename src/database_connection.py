import sqlite3

from config import DATABASE_FILE
from initialize_file_structure import init_file_structure

init_file_structure()

connection = sqlite3.connect(DATABASE_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON")
cursor.close()


def get_database_connection() -> sqlite3.Connection:
    """Returns the database connection"""
    return connection
