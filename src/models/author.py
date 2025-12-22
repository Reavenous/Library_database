from src.models.base import BaseModel

class Author(BaseModel):
    TABLE_NAME = 'Authors'
    PK_FIELD = 'AuthorID'
    FIELDS = [
        'FirstName',
        'LastName',
        'BirthDate'
    ]

    def __repr__(self):
        return f"<Author: {self.FirstName} {self.LastName}>"