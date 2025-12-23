from src.models.base import BaseModel

class Loan(BaseModel):
    TABLE_NAME = 'Loans'
    PK_FIELD = 'LoanID'
    FIELDS = [
        'BookID', 
        'MemberID', 
        'LoanDate', 
        'ReturnDate', 
        'Status'

    ]

    def __repr__(self):
        return f"<Loan ID: {getattr(self, 'LoanID', '?')} - Status: {getattr(self, 'Status', 'Unknown')}>"