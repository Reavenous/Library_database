from src.database import Database

class BaseModel:
    TABLE_NAME = None
    PK_FIELD = None
    FIELDS = []

    def __init__(self, **kwargs):
        for field in self.FIELDS:
            setattr(self, field, kwargs.get(field))
        
        setattr(self, self.PK_FIELD, kwargs.get(self.PK_FIELD))

    def save(self):
        conn = Database.get_connection()
        cursor = conn.cursor()

        pk_value = getattr(self, self.PK_FIELD)

        if pk_value is None:
            columns = ', '.join(self.FIELDS)
            placeholders = ', '.join(['?'] * len(self.FIELDS))
            values = [getattr(self, field) for field in self.FIELDS]

            sql = f"INSERT INTO {self.TABLE_NAME} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, values)
            cursor.execute("SELECT @@IDENTITY")
            new_id = cursor.fetchone()[0]
            setattr(self, self.PK_FIELD,int (new_id))
            print(f"[{self.TABLE_NAME}] Vložen nový záznam ID: {new_id}")

        else:
            set_clause = ", ".join([f"{field} = ?" for field in self.FIELDS])
            values = [getattr(self, field) for field in self.FIELDS]
            values.append(pk_value)
            
            sql = f"UPDATE {self.TABLE_NAME} SET {set_clause} WHERE {self.PK_FIELD} = ?"
            cursor.execute(sql, values)
            print(f"[{self.TABLE_NAME}] Aktualizován záznam ID: {pk_value}")
        
        conn.commit()
        cursor.close()

    @classmethod
    def find(cls, pk_value):
        """Najde jeden záznam podle ID a vrátí instanci objektu."""
        conn = Database.get_connection()
        cursor = conn.cursor()
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE {cls.PK_FIELD} = ?"
        row = cursor.execute(sql, (pk_value,)).fetchone()
        conn.close()
        
        if row:
            columns = [column[0] for column in cursor.description]
            data = dict(zip(columns, row))
            return cls(**data) 
        return None

    @classmethod
    def all(cls):
        conn = Database.get_connection()
        cursor = conn.cursor()
        sql = f"SELECT * FROM {cls.TABLE_NAME}"
        cursor.execute(sql)
        
        objects = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            data = dict(zip(columns, row))
            objects.append(cls(**data))
            
        conn.close()
        return objects