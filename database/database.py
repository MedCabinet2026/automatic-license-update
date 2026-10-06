import pyodbc
from database.connection import create_connection_strign

def connect_to_database(database_name):
    connection_string = create_connection_strign(database_name)
    return pyodbc.connect(connection_string)

def execute_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()