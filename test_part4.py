from src.services import LibraryService
from src.models.book import Book
from src.models.loan import Loan
from src.models.member import Member
from src.database import Database

def run_test_part4():
    print("--- START TESTU ČÁST 4 (TRANSAKCE & REPORTY) ---")

    
    kniha = Book.all()[0] 
    ctenar = Member.all()[0] 
    
    print(f"TEST DATA: Kniha='{kniha.Title}' (ID {kniha.BookID}), Čtenář='{ctenar.FullName}' (ID {ctenar.MemberID})")

    print("\n1. Akce: Vypůjčení knihy...")
    try:
        LibraryService.borrow_book(kniha.BookID, ctenar.MemberID)
    except Exception as e:
        print(f"INFO: Možná už je půjčená? ({e})")

    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 LoanID FROM Loans WHERE BookID = ? AND Status='Active' ORDER BY LoanID DESC", (kniha.BookID,))
    loan_id = cursor.fetchone()[0]
    conn.close()
    
    print(f"   -> Vytvořena výpůjčka ID: {loan_id}")

    print("\n2. Akce: Vrácení knihy (Poškozená!) - Spouštím transakci...")
    LibraryService.return_book_transaction(loan_id, is_damaged=True)

    print("\n3. Kontrola konzistence dat:")
    
    kniha_po_vraceni = Book.find(kniha.BookID)
    print(f"   Stav knihy v DB (IsDamaged): {kniha_po_vraceni.IsDamaged}")
    
    if kniha_po_vraceni.IsDamaged:
        print("    ÚSPĚCH: Transakce zapsala poškození do tabulky Books.")
    else:
        print("    CHYBA: Kniha není označena jako poškozená!")

    LibraryService.generate_report()

    print("\n--- KONEC TESTU ČÁST 4 ---")

if __name__ == "__main__":
    run_test_part4()