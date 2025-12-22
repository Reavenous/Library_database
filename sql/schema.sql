
DROP VIEW IF EXISTS View_OverdueLoans;
DROP VIEW IF EXISTS View_BookDetails;
DROP TABLE IF EXISTS Loans;
DROP TABLE IF EXISTS BookAuthors;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Members;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS Categories;

GO

-- 1. Tabulka Autorů
CREATE TABLE Authors (
    AuthorID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(100) NOT NULL,
    LastName NVARCHAR(100) NOT NULL,
    BirthDate DATE NULL
);

-- 2. Tabulka Kategorií
CREATE TABLE Categories (
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(50) NOT NULL UNIQUE,
    Description NVARCHAR(255) NULL
);

-- 3. Tabulka Knih
CREATE TABLE Books (
    BookID INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(200) NOT NULL,
    PublicationYear INT NULL,
    ISBN NVARCHAR(20) NULL,
    PurchasePrice FLOAT NOT NULL,
    IsDamaged BIT DEFAULT 0,
    CategoryID INT NOT NULL,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

-- 4. Vazební tabulka M:N (Kniha <-> Autor)
CREATE TABLE BookAuthors (
    BookID INT NOT NULL,
    AuthorID INT NOT NULL,
    PRIMARY KEY (BookID, AuthorID),
    FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE,
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID) ON DELETE CASCADE
);

-- 5. Tabulka Čtenářů
CREATE TABLE Members (
    MemberID INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(150) NOT NULL,
    Email NVARCHAR(100) NOT NULL UNIQUE,
    JoinedDate DATETIME DEFAULT GETDATE(),
    IsActive BIT DEFAULT 1
);

-- 6. Tabulka Výpůjček
CREATE TABLE Loans (
    LoanID INT IDENTITY(1,1) PRIMARY KEY,
    BookID INT NOT NULL,
    MemberID INT NOT NULL,
    LoanDate DATETIME DEFAULT GETDATE(),
    ReturnDate DATETIME NULL,
    Status NVARCHAR(20) NOT NULL,
    CONSTRAINT CHK_Status CHECK (Status IN ('Active', 'Returned', 'Overdue', 'Lost')),
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

GO

-- VIEW 1: Detail knihy
CREATE VIEW View_BookDetails AS
SELECT 
    b.BookID,
    b.Title,
    c.Name AS Category,
    STRING_AGG(a.FirstName + ' ' + a.LastName, ', ') AS Authors
FROM Books b
JOIN Categories c ON b.CategoryID = c.CategoryID
LEFT JOIN BookAuthors ba ON b.BookID = ba.BookID
LEFT JOIN Authors a ON ba.AuthorID = a.AuthorID
GROUP BY b.BookID, b.Title, c.Name;

GO

-- VIEW 2: Aktivní výpůjčky po splatnosti
CREATE VIEW View_OverdueLoans AS
SELECT 
    l.LoanID,
    m.FullName AS Member,
    b.Title AS Book,
    l.LoanDate,
    DATEDIFF(day, l.LoanDate, GETDATE()) AS DaysBorrowed
FROM Loans l
JOIN Members m ON l.MemberID = m.MemberID
JOIN Books b ON l.BookID = b.BookID
WHERE l.Status = 'Active' AND DATEDIFF(day, l.LoanDate, GETDATE()) > 30;
GO