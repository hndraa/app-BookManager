# Bookwise — Book Management App

**SOFTWARE** | **DESKTOP APPLICATION** | **PYTHON ‧ SQLITE**

Bookwise is a desktop application for managing a personal book collection. It supports adding, searching, editing, and deleting book records, with persistent storage in SQLite and CSV export for spreadsheet applications.

## 01. Project Overview

### Description

Bookwise provides a workspace for maintaining book records. Users can save a book title, author, and publication year, browse their collection in a table, search by title or author, edit existing records, delete selected records, and export the library to CSV.

### Objectives

- Practice desktop GUI development with PyQt5.
- Store and manage structured records using SQLite.
- Provide a searchable, table-based interface.
- Export records to a portable CSV format.

### Problem Statement

Book details can become difficult to track when records are scattered across notes or spreadsheets. Users need a single interface for maintaining book information and retrieving it quickly.

### Solution

Bookwise combines a book-entry form, a searchable collection table, SQLite persistence, and CSV export in one desktop application.

### Key Features

- Add book records with title, author, and publication year.
- Validate required fields and four-digit publication years.
- Search books by title or author.
- Edit a record by double-clicking its row.
- Delete a selected record after confirmation.
- Store records persistently in SQLite.
- Export all records to CSV.
- Display collection counts and operation status.
- Use a modern dark interface with a warm terracotta gradient primary button theme.

## 02. Tech Stack

| Category                | Technology            |
| ----------------------- | --------------------- |
| Language                | Python                |
| GUI Framework           | PyQt5                 |
| Database                | SQLite (`sqlite3`)  |
| Data Export             | Python `csv` module |
| Interface Styling       | Qt Style Sheets       |
| Development Environment | Python 3              |

## 03. Screenshots / Results

### Main Library Interface

Shows the book-entry form, search field, book table, and delete action.

<img width="900" height="630" alt="image" src="https://github.com/user-attachments/assets/54403f86-8085-4438-8985-9075fc96da07" />


### Adding a Book

Shows form validation and adding a new book record.

<img width="901" height="606" alt="image" src="https://github.com/user-attachments/assets/be05aa67-0c11-4227-85f0-4eac67c06763" />


### Searching the Collection

Shows the table filtered by a title or author keyword.

<img width="897" height="600" alt="image" src="https://github.com/user-attachments/assets/89b6a6bc-06aa-4c0d-a4b6-df5fd0eec189" />


### Editing a Book

Double-click a row to edit the title, author, and publication year.

<img width="895" height="604" alt="image" src="https://github.com/user-attachments/assets/98d54713-898c-4246-b89f-112bde968620" />

### Deleting a Book

Shows the selected-record deletion flow and confirmation dialog.

<img width="902" height="600" alt="image" src="https://github.com/user-attachments/assets/120133d3-a1a0-4de6-979a-7d831b9641a8" />


### CSV Export

Shows the export page and save-file dialog.

<img width="903" height="599" alt="image" src="https://github.com/user-attachments/assets/7c73ed23-d9d2-4e2e-beda-066cf512636e" />


## 04. Installation & Usage

### Prerequisites

- Python 3.10 or later recommended.
- pip package manager.
- PyQt5.

### Project Structure

```text
app-BookManager/
├── main.py
├── database.db          # Created automatically on first run
├── my_book_collection.csv
├── screenshots/
│   ├── 01-library-interface.png
│   ├── 02-add-book.png
│   ├── 03-search-books.png
│   ├── 04-edit-book.png
│   ├── 05-delete-book.png
│   └── 06-csv-export.png
└── README.md
```

### Installation

Clone the repository:

```bash
git clone https://github.com/hndraa/app-BookManager.git
cd app-BookManager
```

Install the dependency:

```bash
python -m pip install PyQt5
```

### Run the Application

```bash
python main.py
```

The application creates `database.db` in the project directory automatically if it does not already exist.

### Usage Instructions

1. Launch the application.
2. Enter the book title, author, and four-digit publication year.
3. Select **Add Book** to save the record.
4. Use the search field to filter records by title or author.
5. Double-click a table row to edit the record.
6. Select a row and click **Delete Selected** to remove it after confirmation.
7. Open the **Export** tab and select **Export to CSV**.
8. Choose a destination and save the CSV file.

### Data Storage

Book records are stored in a local SQLite database named `database.db`. Keep this file to preserve the collection between application sessions.

### Limitations

- The application manages basic book metadata only.
- Search matches book titles and author names.
- CSV export includes all stored records, not only the currently visible search results.
- The application is designed for local, single-user use.
