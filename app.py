from src.models.book import Book
from src.models.member import Member
from src.services import LibraryService
from src.utils import DataImporter
import sys


def print_menu():
    print("\n" + "="*40)
    print("       KNIHOVNÍ SYSTÉM v1.0")
    print("="*40)
    print("1.  Seznam všech knih")
    print("2.  Přidat novou knihu")
    print("3.  Půjčit knihu")
    print("4.  Vrátit knihu (Transakce)")
    print("5.  Generovat Report")
    print("6.  Import dat z CSV")
    print("0.  Konec")
    print("-" * 40)

    def app():
        while True:
            print_menu()
            choice = input("Vyberte možnost (0-6): ")

            try:
                if choice == '1':
                    books = Book.all()
                    print (f"\nNalezeno {len(books)} knih:")
                    for b in books:
                        stav = "POŠKOZENÁ" if b.IsDamaged else "OK"
                        print(f" [ID {b.BookID}] {b.Title} ({b.PublicationYear}) - {stav}")

                elif choice == '2':
                    title = input("Název knihy: ")
                    year = int(input("Rok vydání: "))
                    price = float(input("Cena (kč)): "))
                    new_book = Book(Title=title, PublicationYear=year, PurchasePrice=price, CategoryID=1, IsDamaged=False)
                    new_book.save()
                    print(f"Kniha '{title}' byla uložena s ID {new_book.BookID}.") 

                elif choice == '3':
                    book_id = int(input("Zadejte ID knihy"))
                    members = Member.all()
                    if not members:
                        print(" Nejsou registrováni žádní čtenáři. Nelze půjčit knihu.")
                        continue
                    member_id = members[0].MemberID
                    print(f" Půjčuji čtenáři ID {member_id}...")
                    LibraryService.borrow_book(book_id, member_id)

                elif choice == '4':
                    loan_id = int(input("Zadejte ID výpůjčky: "))
                    damaged_input = input("Je kniha poškozená? (ano/ne): ").lower()
                    is_damaged = (damaged_input == 'ano')
                    LibraryService.return_book_transaction(loan_id, is_damaged)

                elif choice == '5':
                    LibraryService.generate_report()
                elif choice == '6':
                    DataImporter.import_books_from_csv('books_import.csv')
                elif choice == '0':
                    print("Ukončuji aplikaci. Na shledanou!")
                    sys.exit(0)
                else:
                    print(" Neplatná volba. Zkuste to znovu.")  
            except ValueError:
                print(" Chyba: Neplatný vstup. Zadejte číslo.")
            except Exception as e:
                print(f" Nastala chyba: {e}")
    if __name__ == "__main__":
        app()
        
