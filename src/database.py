import pyodbc
import configparser
import os

class Database:
    _connection_string = None

    @staticmethod
    def _load_config():
        config = configparser.ConfigParser()
        
        
        current_file_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file_path) # jsme v .../src
        
        
        project_root = os.path.dirname(current_dir)
        
        config_path = os.path.join(project_root, 'config', 'db_config.ini')
        
       
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Konfigurační soubor nenalezen na cestě: {config_path}")
            
        config.read(config_path)
        
        try:
            db_props = config['mssql']
        except KeyError:
            raise KeyError(f"Soubor {config_path} byl nalezen, ale chybí v něm sekce [mssql].")
        
        return (
            f"DRIVER={{{db_props['driver']}}};"
            f"SERVER={db_props['server']},{db_props['port']};"
            f"DATABASE={db_props['database']};"
            f"UID={db_props['user']};"
            f"PWD={db_props['password']};"
            "TrustServerCertificate=yes;"
        )

    @classmethod
    def get_connection(cls):
        if cls._connection_string is None:
            cls._connection_string = cls._load_config()
        return pyodbc.connect(cls._connection_string)