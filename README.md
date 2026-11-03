# SQLite Database Management System

A Python project that lets users create and manage SQLite databases through an interactive command-line menu.

## Features

- **Database management:** Create, open, and delete `.db` files.
- **Table management:** Create tables with custom field names and data types, rename tables, and delete tables.
- **Record management:** Insert new records, update existing records, and delete records.
- **View records:** Display all records or select particular fields to view.
- **Search with conditions:** Filter records using field conditions combined with `AND` or `OR`.
- **Input validation:** Check user inputs, field data types, and database file extensions.
- **Formatted output:** Display database records in aligned columns for easier reading.

## Supported Data Types

When creating a table, you can choose from the following data types:

- `TEXT`
- `INTEGER`
- `REAL`
- `BLOB`
- `NULL`

## Requirements

- Python 3
- Tkinter, used for database file selection dialogs

The project uses Python's built-in `sqlite3` module, so no additional SQLite package is needed.

## How to Run

1. Make sure `front_end.py` and `back_end.py` are saved in the same folder.
2. Open a terminal or command prompt in that folder.
3. Run:

   ```bash
   python front_end.py
   ```

   Depending on your system, you may need to use `python3 front_end.py` instead.

4. Follow the menu prompts to manage your database.

## Project Files

| File | Description |
|---|---|
| `front_end.py` | Provides the interactive menu, prompts for user input, validates entries, and manages the user-facing database operations. |
| `back_end.py` | Handles SQLite connections and performs database, table, and record operations. |

## Using the Application

When you run the program, a menu appears with options to:

1. Create a database
2. Open a database
3. Delete a database
4. Create a table
5. Rename a table
6. Delete a table
7. Insert a record
8. Update a record
9. Delete a record
10. View all records
11. View specific records

For table and record operations, open a database first. The application displays the currently connected database and table as you use the menu.

When viewing or modifying records, you can select fields and specify conditions. Conditions currently use equality checks and can be joined with `AND` or `OR`.

## Technologies Used

- **Python** — application logic and interactive command-line interface.
- **SQLite** — local database storage.
- **Tkinter** — file dialogs for creating and selecting database files.
