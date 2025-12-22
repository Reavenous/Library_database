from src.models.book import Book
from src.models.author import Author
from src.models.member import Member
from src.database import Database

def prepare_category():
    conn = Database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET IDENTITY_INSERT Categories ON")
        cursor.execute("INSERT INTO Categories (CategoryID, Name, Description) VALUES (1, 'Sci-Fi', 'Vědecko-fantastické')")
        cursor.execute("SET IDENTITY_INSERT Categories OFF")
        conn.commit()
        print("   -> Kategorie 'Sci-Fi' (ID 1) byla obnovena.")
    except Exception:
        pass
    finally:
        conn.close()

def run_test_relations():
    print("--- START TESTU ČÁST 3 (RELACE) ---")

    prepare_category()

    print("1. Vytvářím autora...")
    autor = Author(FirstName="Frank", LastName="Herbert", BirthDate="1920-10-08")
    autor.save()
    print(f"   Autor uložen: {autor}")

    print("2. Vytvářím knihu...")
    kniha = Book(
        Title="Spasitel Duny", 
        PublicationYear=1969, 
        ISBN="999-000", 
        PurchasePrice=350.0,
        IsDamaged=False, 
        CategoryID=1 
    )
    kniha.save()
    print(f"   Kniha uložena: {kniha}")

    print("3. Propojuji autora s knihou...")
    kniha.add_author(autor.AuthorID)

    print("4. Vytvářím čtenáře...")
    ctenar = Member(
        FullName="Hrot Bagr", 
        Email="hrot.bagr@example.com", 
        IsActive=True
    )
    ctenar.save()
    print(f"   Čtenář uložen: {ctenar}")

    print("--- KONEC TESTU ČÁST 3 (ÚSPĚCH) ---")

if __name__ == "__main__":
    run_test_relations()