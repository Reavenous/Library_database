from src.models.base import BaseModel
from src.database import Database

class Book(BaseModel):
    TABLE_NAME = 'Books'
    PK_FIELD = 'BookID'
    FIELDS = [
        'Title', 
        'PublicationYear', 
        'ISBN', 
        'PurchasePrice', 
        'IsDamaged', 
        'CategoryID'
    ]

    def add_author(self, author_id):
        if not getattr(self, 'BookID'):
            raise ValueError("Kniha nemá ID (nejprve ji ulož pomocí .save())")
        
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        try:
            sql = "INSERT INTO BookAuthors (BookID, AuthorID) VALUES (?, ?)"
            cursor.execute(sql, (self.BookID, author_id))
            conn.commit()
            print(f"   -> Autor ID {author_id} byl přiřazen ke knize '{self.Title}'")
        except Exception as e:
            print(f"Chyba při vazbě autora: {e}")
        finally:
            conn.close()



    def __repr__(self):
        return f"<Book: {self.Title} (ID: {getattr(self, 'BookID', None)})>"