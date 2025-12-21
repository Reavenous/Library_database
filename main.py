import pyodbc 
from src.database import Database
from src.models.book import Book

def prepare_category():
    conn = Database.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SET IDENTITY_INSERT Categories ON")
        cursor.execute("INSERT INTO Categories (CategoryID, Name, Description) VALUES (1, 'Sci-Fi', 'Vědecko-fantastické')")
        cursor.execute("SET IDENTITY_INSERT Categories OFF")
        conn.commit()
    except:
        pass
    conn.close()


def run_test():
    print("--- Start Testu 2 ---")
    prepare_category()
    moje_kniha = Book(
        Title="Duna",
        PublicationYear=1965,
        ISBN="978-0441172719",
        PurchasePrice=499.0,
        IsDamaged=False,
        CategoryID=1
    )
    print("ukládám novou knihu...")
    moje_kniha.save()
    print(f"Kniha uložena, nové ID je: {moje_kniha.BookID}")

    print("Měním cenu...")
    moje_kniha.PurchasePrice = 299.0
    moje_kniha.save() 

    print("Načítám knihu z DB...")
    kniha_z_db = Book.find(moje_kniha.BookID)
    print(f"Načteno: {kniha_z_db.Title}, Cena: {kniha_z_db.PurchasePrice}")

    print("Všechny knihy v DB:")
    vsechny = Book.all()
    for k in vsechny:
        print(f" - {k.Title}")

    # 5. Smazání (Active Record: DELETE)
    # print("Mažu knihu...")
    # moje_kniha.delete()

    print("--- Konec Testu 2 ---")


if __name__ == "__main__":
    run_test()
    