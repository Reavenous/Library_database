import csv
import os
from src.models.book import Book
from src.models.author import Author
from src.database import Database

class DataImporter:
    def import_books_from_csv(filename):
        file_path = os.path.join('data', filename)

        if not os.path.exists(file_path):
            print(f" Chyba: Soubor {file_path} neexistuje.")
            return
        
        print(f" Importuji knihy ze souboru: {filename}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')

            count = 0
            for row in reader:
                author_name_parts = row['Author'].split(' ')
                last_name = author_name_parts[-1]
                first_name = " ".join(author_name_parts[:-1]) 
                author = Author(FirstName=first_name, LastName=last_name)
                author.save()
                
                book = Book(
                    Title=row['Title'],
                    PublicationYear=int(row['Year']),
                    PurchasePrice=float(row['Price']),
                    ISBN=row['ISBN'],
                    IsDamaged=False,
                    CategoryID=1
                )
                book.save()
                book.add_author(author.AuthorID)
                print(f"   -> Importováno: {book.Title} (Autor: {last_name})")
                count += 1

                print(f" Import dokončen. Přidáno {count} knih.")
        except Exception as e:  
            print(f" Chyba při importu knih: {e}")