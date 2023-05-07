import pyodbc
import os

def execute_sql_script(sql_script):
    global connection_string
    connection = pyodbc.connect(connection_string)

    try:
        cursor = connection.cursor()

        cursor.execute(sql_script)

        connection.commit()

    except Exception as e:
        print(f"Error executing SQL script: {e}")
    finally:
        connection.close()

connection_string = '' + os.environ.get('JUNI_MEMORY_CONNECTION_STRING')