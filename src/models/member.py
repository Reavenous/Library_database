from src.models.base import BaseModel

class Member(BaseModel):
    TABLE_NAME = 'Members'
    PK_FIELD = 'MemberID'
    FIELDS = [
        'FullName',
        'Email',
        'JoinedDate',
        'IsActive'
    ]

    def __repr__(self):
        return f"<Member: {self.FullName}>"