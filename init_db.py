import pyodbc
import os
import sys
import re

# Přidáme aktuální složku do cesty
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.database import Database

def init_database():
    print("Connecting to database...")
    try:
        conn = Database.get_connection()
        conn.autocommit = True
        cursor = conn.cursor()
        print("Connection successful!")
        
        print("Reading SQL schema...")
        schema_path = os.path.join('sql', 'schema.sql')
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
   
        commands = re.split(r'\bGO\b', sql_script, flags=re.IGNORECASE)
        
        print(f"Found {len(commands)} blocks to execute.")
        
        for i, command in enumerate(commands):
            command = command.strip()
            if command:
                try:
                    print(f"Executing block {i+1}...")
                    cursor.execute(command)
                except pyodbc.Error as e:
                    if "There is already an object" in str(e):
                        print(f" -> Object already exists (skipping).")
                    else:
                        print(f" Error executing block {i+1}: {e}")
                    
        print("\nDatabase initialized successfully! Tabulky jsou vytvořeny.")
        conn.close()
        
    except Exception as e:
        print(f" Critical Error: {e}")

if __name__ == "__main__":
    init_database()