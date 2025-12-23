from src.database import Database
from datetime import datetime

class LibraryService:
    @staticmethod
    def  borrow_book(book_id,member_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Loans WHERE BookID = ? AND Status = 'Active'", (book_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                raise ValueError(f"Kniha ID {book_id} je již vypůjčena!")
            
            sql = """INSERT INTO Loans (BookID, MemberID, LoanDate, Status)
                VALUES (?, ?, ?, 'Active')"""
            
            cursor.execute(sql, (book_id, member_id, datetime.now()))
            conn.commit()
            print(f"Kniha ID {book_id} byla úspěšně vypůjčena čtenářem ID {member_id}.")

        except Exception as e:
            conn.rollback()
            print(f"Chyba při vypůjčení knihy: {e}")
            raise e
        finally:
            conn.close()

    @staticmethod
    def return_book_transaction(loan_id, is_damaged=False):
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            print(f"Zahajuji transakci vrácení (Loan ID: {loan_id})...")
            cursor.execute("SELECT BookID FROM Loans WHERE LoanID = ?", (loan_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Nenalezena výpůjčka ")
            book_id = row[0]

            sql_loan = """UPDATE Loans
                SET ReturnDate = ?, Status = 'Returned'
                WHERE LoanID = ?"""
            
            cursor.execute(sql_loan, (datetime.now(), loan_id))
            
            
            if is_damaged:
                print(f"   -> Kniha je hlášena jako poškozená. Aktualizuji tabulku Books...")
                sql_book = "UPDATE Books SET IsDamaged = 1 WHERE BookID = ?"
                cursor.execute(sql_book, (book_id,))

            conn.commit()
            print(" Transakce úspěšná: Kniha vrácena.")
        except Exception as e:
            conn.rollback()
            print(f"Chyba transakce! Změny byly vráceny zpět. Důvod: {e}")
            raise e
        finally:
            conn.autocommit = True
            conn.close()

    @staticmethod
    def generate_report():
        conn = Database.get_connection()
        cursor = conn.cursor()

        print("\n--- REPORT: Detaily knih a autoři ---")
        cursor.execute("SELECT * FROM View_BookDetails")
        rows = cursor.fetchall()

        print(f"{'Kniha':<30} | {'Kategorie':<15} | {'Autoři'}")
        print("-" * 70)
        for row in rows:
            # row[1]=Title, row[2]=Category, row[3]=Authors
            print(f"{str(row[1])[:30]:<30} | {str(row[2])[:15]:<15} | {row[3]}")
            
        conn.close()

            

        