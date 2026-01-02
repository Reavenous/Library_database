

# Library Management System

A Python console application for managing a library database. This project implements a custom **Active Record Pattern** (without external ORM libraries) and handles transactions, M:N relationships, and data reporting using **MSSQL**.

**Author:** Alexandre Basseville C4b
**Course Project:** PV

---

##  Features
This project fulfills the **D2 Assignment** (Row Gateway / Active Record) and includes:

* **Custom ORM:** Implemented base `ActiveRecord` class for CRUD operations.
* **Database Structure:** 5 Tables (Books, Authors, Members, Loans, Categories), M:N relationships, and SQL Views.
* **Transactions:** Safe "Return Book" operation updating multiple tables atomically.
* **Reporting:** Aggregated data generation from SQL Views.
* **Data Import:** Functionality to import books/authors from CSV files.
* **Configuration:** External `db_config.ini` for database connection settings.

##  Technology Stack
* **Language:** Python 3.10+
* **Database:** Microsoft SQL Server (MSSQL)
* **Driver:** PyODBC (ODBC Driver 17 for SQL Server)
* **Environment:** Docker (for local development)

---

##  Installation Guide

### 1. Prerequisite
Ensure you have **Python** and **Git** installed.
You also need the **ODBC Driver 17 for SQL Server**.

### 2. Clone Repository
```bash
git clone [https://github.com/Reavenous/Library_database.git](https://github.com/Reavenous/Library_database.git)
cd Library_database
```
### 3. Setup Virtual Environment
It is recommended to use a virtual environment:

```Bash

# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```Bash

pip install -r requirements.txt
```

## Database Configuration
You have two options to run the database:

### Option A: Local Docker (Recommended for testing)
If you have Docker installed, you can spin up a local MSSQL instance instantly:

```Bash

docker-compose up -d
```
Note: Wait approx. 20 seconds for the server to fully start.


### Option B: External / School Server
If you cannot use Docker (e.g., on a school PC), connect to an existing MSSQL server:

1. Open `config/db_config.ini`.
2. Update the `[mssql]` section with your credentials:

```ini
[mssql]
server = YOUR_SCHOOL_SERVER_ADDRESS
port = 1433
database = YOUR_DATABASE_NAME
user = YOUR_USERNAME
password = YOUR_PASSWORD
```

## How to Run

### 1. Initialize Database
Before the first run, create tables and views:

```bash
python init_db.py
```
Output should say: Database initialized successfully!

### 2. Start Application
Launch the console interface:

```Bash

python app.py
```
### 3. Usage
Follow the on-screen menu:

- Option 6: Import data from CSV (Recommended first step).

- Option 1: List all books.

- Option 3: Borrow a book.

- Option 4: Return a book (Triggers Transaction).

## Project Structure
* `src/` - Source code.
    * `models/` - Active Record classes (Book, Author, Member...).
    * `services.py` - Business logic (Transactions, Reports).
* `sql/` - SQL DDL scripts for schema creation.
* `config/` - Database connection configuration.
* `data/` - CSV files for import.
* `tests/` - Unit tests (if applicable).
