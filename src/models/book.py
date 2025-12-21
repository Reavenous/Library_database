from src.models.base import BaseModel

class Book(BaseModel):
    TABLE_NAME = 'books'
    PK_FIELD = 'id'
    FIELDS = ['title', 'author', 'published_year', 'isbn', 'PurchasePrice', 'IsDamaged', 'CategoryID']

    def __repr__(self):
        return f"<Book: {self.title} (ID: {self.id})>"
    