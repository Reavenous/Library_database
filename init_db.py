import pyodbc
import configparser
import os

def get_db_connection():
    config = configparser.ConfigParser()
    config.read('config/db_config.ini')
    
    db_props = config['mssql']


    conn_str = (
        f"DRIVER={{{db_props['driver']}}};"
        f"SERVER={db_props['server']},{db_props['port']};"
        f"DATABASE={db_props['database']};"
        f"UID={db_props['user']};"
        f"PWD={db_props['password']};"
        "TrustServerCertificate=yes;"
    )
    
    return pyodbc.connect(conn_str)

def init_database():
    print("connection to db....")
    try:
        conn = get_db_connection
        conn.autocommit = True
        cursor = conn.cursor()

        print("Reading SQL schema")
        with open('sql/schema.sql', 'r', encoding= 'utf-8') as f:
            sql_script = f.read()
        
        commands = sql_script.split('GO\n')
        print("Executing SQL commands...")
        for command in commands:
            if command.strip():
                try:
                    cursor.execute(command)
                except pyodbc.Error as e:
                    print(f"Error executing command: {e}")


        print("Database initialized successfully.")
        conn.close()
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    init_database()